from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Pedido, Produto, ItemPedido, Transacao


@login_required
def criar_pedido(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)

    # cria pedido e item
    pedido = Pedido.objects.create(cliente=request.user)
    ItemPedido.objects.create(pedido=pedido, produto=produto, quantidade=1)

    # cria transação pendente
    Transacao.objects.create(pedido=pedido, valor=pedido.total)

    return JsonResponse({"mensagem": "Pedido criado", "pedido_id": pedido.id})


@login_required
def detalhes_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)

    return JsonResponse({
        "pedido_id": pedido.id,
        "itens": [
            {
                "produto": item.produto.nome,
                "quantidade": item.quantidade,
                "subtotal": float(item.subtotal),
            }
            for item in pedido.itens.all()
        ],
        "total": float(pedido.total),
        "status": pedido.transacao.status,
        "pago": pedido.pago,
    })


@login_required
def pagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, cliente=request.user)
    transacao = pedido.transacao

    # simulação de pagamento (aprova automaticamente)
    transacao.status = "aprovado"
    transacao.save()

    pedido.pago = True
    pedido.save()

    return JsonResponse({"mensagem": "Pagamento aprovado", "pedido_id": pedido.id})
