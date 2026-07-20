DROP DATABASE IF EXISTS transparencia;
CREATE DATABASE transparencia
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;

USE transparencia;


-- CRIANDO AS TABELAS RAW

CREATE TABLE raw_viagem (
    identificador_processo_viagem VARCHAR(99),
    numero_proposta_pcdp VARCHAR(99),
    situacao VARCHAR(99),
    viagem_urgente VARCHAR(99),
    justificativa_urgencia_viagem TEXT,
    codigo_orgao_superior VARCHAR(99),
    nome_orgao_superior VARCHAR(99),
    codigo_orgao_solicitante VARCHAR(99),
    nome_orgao_solicitante VARCHAR(99),
    cpf_viajante VARCHAR(99),
    nome VARCHAR(99),
    cargo VARCHAR(99),
    funcao VARCHAR(99),
    descricao_funcao TEXT,
    periodo_data_inicio VARCHAR(99),
    periodo_data_fim VARCHAR(99),
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias VARCHAR(99),
    valor_passagens VARCHAR(99),
    valor_devolucao VARCHAR(99),
    valor_outros_gastos VARCHAR(99)
)
ENGINE=InnoDB
ROW_FORMAT=DYNAMIC;

CREATE TABLE raw_trecho (
    identificador_processo_viagem VARCHAR(99),
    numero_proposta_pcdp VARCHAR(99),
    sequencia_trecho VARCHAR(99),
    origem_data VARCHAR(99),
    origem_pais VARCHAR(99),
    origem_uf VARCHAR(99),
    origem_cidade VARCHAR(99),
    destino_data VARCHAR(99),
    destino_pais VARCHAR(99),
    destino_uf VARCHAR(99),
    destino_cidade VARCHAR(99),
    meio_transporte VARCHAR(99),
    numero_diarias VARCHAR(99),
    missao VARCHAR(99)
)
ENGINE=InnoDB;

CREATE TABLE raw_passagem (
    identificador_processo_viagem VARCHAR(99),
    numero_proposta_pcdp VARCHAR(99),
    meio_transporte VARCHAR(99),
    pais_origem_ida VARCHAR(99),
    uf_origem_ida VARCHAR(99),
    cidade_origem_ida VARCHAR(99),
    pais_destino_ida VARCHAR(99),
    uf_destino_ida VARCHAR(99),
    cidade_destino_ida VARCHAR(99),
    pais_origem_volta VARCHAR(99),
    uf_origem_volta VARCHAR(99),
    cidade_origem_volta VARCHAR(99),
    pais_destino_volta VARCHAR(99),
    uf_destino_volta VARCHAR(99),
    cidade_destino_volta VARCHAR(99),
    valor_da_passagem VARCHAR(99),
    taxa_de_servico VARCHAR(99),
    data_da_emissao_compra VARCHAR(99),
    hora_da_emissao_compra VARCHAR(99)
)
ENGINE=InnoDB;

CREATE TABLE raw_pagamento (
  identificador_processo_viagem VARCHAR(99),
  numero_proposta_pcdp VARCHAR(99),
  codigo_do_orgao_superior VARCHAR(99),
  nome_do_orgao_superior VARCHAR(99),
  codigo_do_orgao_pagador VARCHAR(99),
  nome_do_orgao_pagador VARCHAR(99),
  codigo_da_unidade_gestora_pagadora VARCHAR(99),
  nome_da_unidade_gestora_pagadora VARCHAR(99),
  tipo_de_pagamento VARCHAR(99),
  valor VARCHAR(99)
)
ENGINE=InnoDB;


-- CRIANDO AS TABELAS SILVER

CREATE TABLE silver_viagem (
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    situacao VARCHAR(50),
    viagem_urgente VARCHAR(5),
    cod_orgao_superior VARCHAR(20),
    nome_orgao_superior VARCHAR(255) NOT NULL,
    nome_viajante VARCHAR(255),
    cargo VARCHAR(255),
    data_inicio DATE,
    data_fim DATE,
    destinos VARCHAR(4000),
    motivo VARCHAR(4000),
    valor_diarias DECIMAL(10,2),
    valor_passagens DECIMAL(10,2),
    valor_devolucao DECIMAL(10,2),
    valor_outros_gastos DECIMAL(10,2),
    valor_total DECIMAL(12,2),
    duracao_dias INT,

    PRIMARY KEY (id_viagem),

    CONSTRAINT chk_valor_diarias
        CHECK (valor_diarias >= 0)

);

CREATE TABLE silver_trecho (
    id_trecho INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(20) NOT NULL,
    sequencia_trecho INT,
    origem_data DATE,
    origem_uf VARCHAR(40),
    origem_cidade VARCHAR(80),
    destino_data DATE,
    destino_uf VARCHAR(40),
    destino_cidade VARCHAR(80),
    meio_transporte VARCHAR(50),
    numero_diarias DECIMAL(10,2),

    PRIMARY KEY (id_trecho),
    CONSTRAINT fk_trecho_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_numero_diarias
        CHECK (numero_diarias >= 0),
    CONSTRAINT uk_trecho_sequencia
        UNIQUE (id_viagem, sequencia_trecho)
);

CREATE TABLE silver_passagem (
    id_passagem INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(20) NOT NULL,
    meio_transporte VARCHAR(50),
    pais_origem_ida VARCHAR(60),
    uf_origem_ida VARCHAR(40),
    cidade_origem_ida VARCHAR(80),
    pais_destino_ida VARCHAR(60),
    uf_destino_ida VARCHAR(40),
    cidade_destino_ida VARCHAR(80),
    valor_passagem DECIMAL(10,2),
    taxa_servico DECIMAL(10,2),
    data_emissao DATE,

    PRIMARY KEY (id_passagem),
    CONSTRAINT fk_passagem_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor_passagem
        CHECK (valor_passagem >= 0),
    CONSTRAINT chk_taxa_servico
        CHECK (taxa_servico >= 0)
);

CREATE TABLE silver_pagamento (
    id_pagamento INT NOT NULL AUTO_INCREMENT,
    id_viagem VARCHAR(20) NOT NULL,
    num_proposta VARCHAR(20),
    nome_orgao_pagador VARCHAR(255),
    nome_ug_pagadora VARCHAR(255),
    tipo_pagamento VARCHAR(50) NOT NULL,
    valor DECIMAL(10,2),

    PRIMARY KEY (id_pagamento),
    CONSTRAINT fk_pagamento_viagem
        FOREIGN KEY (id_viagem)
        REFERENCES silver_viagem(id_viagem),
    CONSTRAINT chk_valor_pagamento
        CHECK (valor >= 0)
);
