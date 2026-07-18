# Projeto Avaliativo – Transparência de Viagens Públicas

Projeto desenvolvido para a disciplina de Manipulação de Dados com Python e SQL (SENAI).

Este projeto tem como objetivo aplicar, na prática, o processo de ETL (Extração, Transformação e Carga) utilizando a arquitetura Medallion (Raw --> Silver --> Gold).
A partir de dados públicos de viagens governamentais disponibilizados pelo Portal da Transparência, foram realizadas as etapas de extração, limpeza, padronização, modelagem e análise dos dados, transformando informações brutas em uma base estruturada e confiável para geração de indicadores e apoio à tomada de decisão.


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

## Aprendizados

Durante o desenvolvimento deste projeto, foram aplicados conceitos fundamentais de Engenharia e Análise de Dados, permitindo consolidar o conteúdo abordado no curso Análise de Dados com Python (Módulo 1 - Manipulação de Dados com Python e SQL):

- Arquitetura Medallion (camadas Raw, Silver e Gold);
- Processo ETL (Extração, Transformação e Carga);
- Integração entre Python e MySQL;
- Modelagem relacional de bancos de dados;
- Criação de chaves primárias (PK), chaves estrangeiras (FK) e constraints;
- Limpeza, padronização e tipagem de dados utilizando SQL;
- Tratamento de valores nulos, conversão de datas e valores monetários;
- Consultas SQL com JOIN, GROUP BY e funções de agregação;
- Construção de tabelas e views para a camada Gold;
- Desenvolvimento de análises orientadas a perguntas de negócio;
- Criação de visualizações de dados com Pandas e Matplotlib;
- Organização de projetos seguindo boas práticas de modularização e PEP 8;
- Versionamento e documentação do projeto usando Git e Github.
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

## Conclusão

Este projeto permitiu compreender como dados brutos podem ser transformados em informações úteis para o negócio por meio de uma arquitetura de dados bem estruturada, reforçando a importância da qualidade dos dados, da modelagem relacional e da análise baseada em evidências reais.

---

## Autor

Julia Segundo

Projeto desenvolvido como atividade avaliativa do curso de Análise de Dados com Python – SENAI.
