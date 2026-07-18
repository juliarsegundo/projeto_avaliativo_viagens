# Projeto Avaliativo – Transparência de Viagens Públicas

Projeto desenvolvido para a disciplina de Manipulação de Dados com Python e SQL (SENAI).

O objetivo é aplicar o processo ETL utilizando a arquitetura Medallion (Raw → Silver → Gold), realizando a extração, transformação e análise de dados públicos de viagens governamentais.

---

## Ferramentas utilizadas

- Python 3
- MySQL
- Pandas
- Matplotlib
- SQL
- Git e GitHub
- Jupyter Notebook

---

## Estrutura do projeto

```
projeto_avaliativo_viagens/
│
├── data/
│   └── viagens.zip
├── .env.example
├── .gitignore
│
├── 0_criar_banco.sql
├── 1_extrair.py
├── 2_transformar.py
├── 3_analise.ipynb
│
├── banco.py
├── config.py
└── README.md
```

---


## Arquitetura Medallion

### Camada Raw

Armazena os dados exatamente como foram obtidos da fonte oficial, sem qualquer tratamento.

Tabelas:

- raw_viagem
- raw_trecho
- raw_passagem
- raw_pagamento

---

### Camada Silver

Responsável pela limpeza, padronização e tipagem dos dados.

Nesta etapa foram realizados:

- Conversão de datas;
- Conversão de valores monetários;
- Tratamento de valores nulos;
- Definição de chaves primárias (PK);
- Definição de chaves estrangeiras (FK);
- Criação de constraints;
- Garantia da integridade referencial.

Tabelas:

- silver_viagem
- silver_trecho
- silver_passagem
- silver_pagamento

---

### Camada Gold

Camada destinada às análises de negócio.

Foi criada:

- tabela `gold_viagens`
- view `vw_gold_viagens`

Essa camada reúne informações das viagens, pagamentos e trechos através de JOINs e agregações (GROUP BY), facilitando a geração de indicadores.

---

## Perguntas de negócio respondidas

1. Quais são os 5 órgãos com maior custo total?
2. Quais são os 3 destinos com maior custo médio por viagem?
3. Qual foi a viagem de maior duração e seu custo total?
4. Qual é o tipo de pagamento com maior valor médio?
5. Qual é o meio de transporte mais utilizado?
6. Qual UF de destino aparece em mais trechos?
7. Qual órgão pagou mais no total?

Todas as perguntas foram respondidas utilizando consultas SQL, tabelas e gráficos desenvolvidos em Python.

---

## Como executar

### 1. Clone o projeto

```bash
git clone <url-do-repositorio>
```

---

### 2. Crie um ambiente virtual

```bash
python -m venv venv
```

---

### 3. Ative o ambiente

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

---

### 4. Instale as dependências

```bash
pip install pandas matplotlib mysql-connector-python python-dotenv gdown
```

---

### 5. Configure o arquivo `.env`

Utilize o arquivo `.env.example` como modelo.

Exemplo:

```env
HOST=localhost
USER=root
PASSWORD=sua_senha
DATABASE=transparencia
```

---

### 6. Execute os arquivos

Criação do banco:

```bash
0_criar_banco.sql
```

Extração:

```bash
python 1_extrair.py
```

Transformação:

```bash
python 2_transformar.py
```

Análise:

```bash
3_analise.ipynb
```

---

## Autor

Julia Segundo

Projeto desenvolvido como atividade avaliativa do curso de Análise de Dados com Python – SENAI.
