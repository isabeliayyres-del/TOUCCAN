from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Users
import re


class UserSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Users
        fields = [
            'id_usuario', 'nome', 'email', 'cpf', 'senha',
            'data_nascimento', 'foto_perfil', 'telefone', 'ativo',
            'ip', 'criado_em', 'atualizado_em'
        ]
        read_only_fields = ['id_usuario', 'criado_em', 'atualizado_em']
        extra_kwargs = {'senha': {'write_only': True}, 'ip': {'required': False}}

    def validate_cpf(self, value):
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("CPF deve conter exatamente 11 dígitos.")
        return value

    def validate_telefone(self, value):
        if value and not re.match(r'^\d{10,15}$', value):
            raise serializers.ValidationError("Telefone deve conter entre 10 e 15 dígitos.")
        return value

    def create(self, validated_data):
        senha = validated_data.pop('senha')
        user = Users(**validated_data)
        user.set_password(senha)
        user.save()
        return user

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.set_password(senha)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id_usuario', 'nome', 'email', 'ativo', 'criado_em']


class UserRegistrationSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True, min_length=8)
    confirmar_senha = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['nome', 'email', 'cpf', 'senha', 'confirmar_senha', 'data_nascimento', 'telefone']

    def validate(self, attrs):
        if attrs['senha'] != attrs['confirmar_senha']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return attrs

    def validate_cpf(self, value):
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("CPF deve conter exatamente 11 dígitos.")
        return value

    def create(self, validated_data):
        validated_data.pop('confirmar_senha')
        request = self.context.get('request')
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR', '127.0.0.1')
            validated_data['ip'] = ip
        else:
            validated_data['ip'] = '127.0.0.1'
        senha = validated_data.pop('senha')
        user = Users(**validated_data)
        user.set_password(senha)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        senha = attrs.get('senha')
        if email and senha:
            try:
                user = Users.objects.get(email=email, ativo=True)
                if not user.check_password(senha):
                    raise serializers.ValidationError('Credenciais inválidas.')
                attrs['user'] = user
            except Users.DoesNotExist:
                raise serializers.ValidationError('Credenciais inválidas.')
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id_usuario', 'nome', 'email', 'cpf', 'data_nascimento', 'foto_perfil', 'telefone', 'criado_em', 'atualizado_em']
        read_only_fields = ['id_usuario', 'email', 'cpf', 'criado_em', 'atualizado_em']


class ChangePasswordSerializer(serializers.Serializer):
    senha_atual = serializers.CharField(write_only=True)
    nova_senha = serializers.CharField(write_only=True, min_length=8)
    confirmar_nova_senha = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['nova_senha'] != attrs['confirmar_nova_senha']:
            raise serializers.ValidationError("As novas senhas não coincidem.")
        return attrs

    def validate_senha_atual(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Senha atual incorreta.")
        return value
