from banco import conectar
import banco

# Esvaziar as tabelas SILVER (idempotencia)
LIMPAR_SILVER = [
    "DELETE FROM silver_trecho",
    "DELETE FROM silver_passagem",
    "DELETE FROM silver_pagamento",
    "DELETE FROM silver_viagem",
]

# Copiar RAW -> SILVER convertendo os tipos
SQL_VIAGEM = """
INSERT INTO silver_viagem (
    id_viagem,
    num_proposta,
    situacao,
    viagem_urgente,
    cod_orgao_superior,
    nome_orgao_superior,
    nome_viajante,
    cargo,
    data_inicio,
    data_fim,
    destinos,
    motivo,
    valor_diarias,
    valor_passagens,
    valor_devolucao,
    valor_outros_gastos
)
SELECT
    identificador_processo_viagem,
    numero_proposta_pcdp,
    situacao,
    viagem_urgente,
    codigo_orgao_superior,
    nome_orgao_superior,
    NULLIF(TRIM(nome), ''),
    NULLIF(TRIM(cargo), ''),
    STR_TO_DATE(NULLIF(TRIM(periodo_data_inicio), ''), '%d/%m/%Y'),
    STR_TO_DATE(NULLIF(TRIM(periodo_data_fim), ''), '%d/%m/%Y'),
    NULLIF(TRIM(destinos), ''),
    NULLIF(TRIM(motivo), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_diarias), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_passagens), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_devolucao), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_outros_gastos), ''), '.', ''), ',', '.') AS DECIMAL(10,2))
FROM raw_viagem
"""

SQL_TRECHO = """
INSERT INTO silver_trecho (
    id_viagem,
    sequencia_trecho,
    origem_data,
    origem_uf,
    origem_cidade,
    destino_data,
    destino_uf,
    destino_cidade,
    meio_transporte,
    numero_diarias
)
SELECT
    identificador_processo_viagem,
    CAST(NULLIF(TRIM(sequencia_trecho), '') AS UNSIGNED),
    STR_TO_DATE(NULLIF(TRIM(origem_data), ''), '%d/%m/%Y'),
    NULLIF(TRIM(origem_uf), ''),
    NULLIF(TRIM(origem_cidade), ''),
    STR_TO_DATE(NULLIF(TRIM(destino_data), ''), '%d/%m/%Y'),
    NULLIF(TRIM(destino_uf), ''),
    NULLIF(TRIM(destino_cidade), ''),
    NULLIF(TRIM(meio_transporte), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(numero_diarias), ''), '.', ''), ',', '.') AS DECIMAL(10,2))
FROM raw_trecho
WHERE identificador_processo_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

SQL_PASSAGEM = """
INSERT INTO silver_passagem (
    id_viagem,
    meio_transporte,
    pais_origem_ida,
    uf_origem_ida,
    cidade_origem_ida,
    pais_destino_ida,
    uf_destino_ida,
    cidade_destino_ida,
    valor_passagem,
    taxa_servico,
    data_emissao
)
SELECT
    identificador_processo_viagem,
    NULLIF(TRIM(meio_transporte), ''),
    NULLIF(TRIM(pais_origem_ida), ''),
    NULLIF(TRIM(uf_origem_ida), ''),
    NULLIF(TRIM(cidade_origem_ida), ''),
    NULLIF(TRIM(pais_destino_ida), ''),
    NULLIF(TRIM(uf_destino_ida), ''),
    NULLIF(TRIM(cidade_destino_ida), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor_da_passagem), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(taxa_de_servico), ''), '.', ''), ',', '.') AS DECIMAL(10,2)),
    STR_TO_DATE(NULLIF(TRIM(data_da_emissao_compra), ''), '%d/%m/%Y')
FROM raw_passagem
WHERE identificador_processo_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

SQL_PAGAMENTO = """
INSERT INTO silver_pagamento (
    id_viagem,
    num_proposta,
    nome_orgao_pagador,
    nome_ug_pagadora,
    tipo_pagamento,
    valor
)
SELECT
    identificador_processo_viagem,
    numero_proposta_pcdp,
    NULLIF(TRIM(nome_do_orgao_pagador), ''),
    NULLIF(TRIM(nome_da_unidade_gestora_pagadora), ''),
    NULLIF(TRIM(tipo_de_pagamento), ''),
    CAST(REPLACE(REPLACE(NULLIF(TRIM(valor), ''), '.', ''), ',', '.') AS DECIMAL(10,2))
FROM raw_pagamento
WHERE identificador_processo_viagem IN (
    SELECT id_viagem
    FROM silver_viagem
)
"""

SQL_CALC_VIAGEM = """
UPDATE silver_viagem sv
LEFT JOIN (
    SELECT
        id_viagem,
        SUM(valor) AS valor_total
    FROM silver_pagamento
    GROUP BY id_viagem
) sp
ON sv.id_viagem = sp.id_viagem
SET
    sv.valor_total = COALESCE(sp.valor_total, 0),
    sv.duracao_dias = DATEDIFF(sv.data_fim, sv.data_inicio);
"""


def main():
    print("=== FASE 2: TRANSFORMAÇÃO + CAMADA SILVER ===")

    try:
        conexao = banco.conectar()

        print("[1/3] Limpando tabelas silver...")
        for comando in LIMPAR_SILVER:
            banco.executar(conexao, comando)

        print("[2/3] Copiando RAW -> SILVER...")
        banco.executar(conexao, SQL_VIAGEM)
        banco.executar(conexao, SQL_TRECHO)
        banco.executar(conexao, SQL_PASSAGEM)
        banco.executar(conexao, SQL_PAGAMENTO)

        print("[3/3] Calculando as outras colunas...")
        banco.executar(conexao, SQL_CALC_VIAGEM)

        conexao.close()

        print("=== Camada SILVER concluída com sucesso! ===")

    except Exception as erro:
        print(f"[ERRO] {erro}")
        raise


if __name__ == "__main__":
    main()