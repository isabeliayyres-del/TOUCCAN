-- DROP database loja_virtual;
CREATE DATABASE loja_virtual;
USE loja_virtual;
CREATE TABLE tbl_usuarios (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    cpf CHAR(11) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    foto_perfil VARCHAR(255),
    telefone VARCHAR(15),
    ativo BOOLEAN DEFAULT TRUE,
    ip VARCHAR(50) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
);

CREATE TABLE tbl_enderecos (
    id_endereco INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    padrao BOOLEAN DEFAULT FALSE,
    cep VARCHAR(9) NOT NULL,
    rua VARCHAR(150) NOT NULL,
    numero VARCHAR(10),
    complemento VARCHAR(100),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado VARCHAR(2),
    pais VARCHAR(50) DEFAULT 'Brasil',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE tbl_categorias (
    id_categoria INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    icon VARCHAR(255) NOT NULL,
    descricao TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
);

CREATE TABLE tbl_produtos (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    id_categoria INT NOT NULL,
    foto VARCHAR(255) NOT NULL,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL,
    desconto DECIMAL(10,2),
    estoque INT DEFAULT 0,
    tem_desconto BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_categoria) REFERENCES tbl_categorias(id_categoria) ON DELETE CASCADE
);

CREATE TABLE tbl_comentarios (
    id_comentario INT PRIMARY KEY AUTO_INCREMENT,
    id_produto INT NOT NULL,
    id_usuario INT NOT NULL,
    comentario TEXT NOT NULL,
    nota TINYINT CHECK (nota BETWEEN 1 AND 5),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_produto) REFERENCES tbl_produtos(id_produto) ON DELETE CASCADE,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE tbl_formas_pagamento (
    id_forma_pagamento INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
);

CREATE TABLE tbl_pedidos (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_endereco INT NOT NULL,
    id_forma_pagamento INT NOT NULL,
    status ENUM('pendente', 'pago', 'enviado', 'concluido', 'cancelado') DEFAULT 'pendente',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario),
--     FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos(id_endereco),
--     FOREIGN KEY (id_forma_pagamento) REFERENCES tbl_formas_pagamento(id_forma)
);

CREATE TABLE tbl_itens_pedido (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos(id_pedido) ON DELETE CASCADE,
--     FOREIGN KEY (id_produto) REFERENCES tbl_produtos(id_produto)
);

CREATE TABLE tbl_transacoes (
    id_transacao INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    status ENUM('aguardando', 'aprovado', 'recusado', 'estornado') DEFAULT 'aguardando',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos(id_pedido) ON DELETE CASCADE
);

CREATE TABLE tbl_cupons (
    id_cupom INT PRIMARY KEY AUTO_INCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT,
    desconto_percentual DECIMAL(5,2),
    desconto_valor DECIMAL(10,2),
    valido_ate DATE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
);

CREATE TABLE tbl_favoritos (
    id_favorito INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    id_produto INT NOT NULL,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL,
    UNIQUE (id_usuario, id_produto)
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE CASCADE,
--     FOREIGN KEY (id_produto) REFERENCES tbl_produtos(id_produto) ON DELETE CASCADE
);

CREATE TABLE tbl_notificacoes (
    id_notificacao INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    tipo ENUM('email','push') NOT NULL,
    titulo VARCHAR(150) NOT NULL,
    mensagem TEXT NOT NULL,
    lida BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deletado_em TIMESTAMP NULL
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE CASCADE
);

CREATE TABLE tbl_logs (
    id_log INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NULL,
    acao VARCHAR(100) NOT NULL,
    detalhes TEXT,
    ip VARCHAR(50),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE SET NULL
);
CREATE TABLE tbl_logs_api_erros (
    id_erro INT PRIMARY KEY AUTO_INCREMENT,
    endpoint VARCHAR(255) NULL,
    tabela VARCHAR(255) NOT NULL,
    `query` VARCHAR(255) NOT NULL,
    metodo_http ENUM('GET', 'POST', 'PUT', 'DELETE', 'PATCH') NULL,
    status_http INT DEFAULT 500,
    mensagem_erro TEXT NOT NULL,
    backtrace TEXT,
    payload JSON,
    retorno JSON,
    headers JSON,
    id_usuario INT NULL,
    ip VARCHAR(50),
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--     ,
--     FOREIGN KEY (id_usuario) REFERENCES tbl_usuarios(id_usuario) ON DELETE SET NULL
);