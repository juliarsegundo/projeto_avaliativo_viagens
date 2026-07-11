import zipfile
import pandas as pd
import gdown

import config
import banco


""" Baixa o arquivo do Google Drive """

def baixar_zip():
 
  config.PASTA_DADOS.mkdir(exist_ok=True)
  destino = config.PASTA_DADOS / "viagens.zip"

  if destino.exists():
      print("O arquivo ja foi baixado antes, pulando o download.")
  else:
      print("Baixando o arquivo do Google Drive...")
      gdown.download(id=config.DRIVE_FILE_ID, output=str(destino))
  return destino

def carregar_csv(conexao, zip_aberto, nome_csv, tabela):
   
   """Le um CSV de dentro do zip e insere todas as linhas na tabela do MySQL.
As colunas do CSV estao na MESMA ordem das colunas da tabela
(definidas no 0_criar_banco.sql). Por isso conseguimos inserir "na ordem"
sem precisar escrever o nome de cada coluna. """

   print("   Carregando", tabela, "...")

   #esvazia a tabela antes de carregar (assim, rodar de novo nao duplica dados)
   banco.executar (conexao, f"TRUNCATE TABLE {tabela}")
  
   total = 0
   with zip_aberto.open(nome_csv) as arquivo:
      #le o CSV em pedacos de 50 mil linhas (nao encher a memoria do PC)
      pedacos = pd.read_csv(
        arquivo,
        sep=";",                             # as colunas sao separadas por ponto-e-virgula
        encoding="latin-1",                  # acentuacao dos arquivos do governo
        dtype=str,                           # tudo como texto (camada RAW)
        keep_default_na=False,               # campo vazio continua (nao vira "NaN")
        chunksize=config.TAMANHO_BLOCO,
      )
      for pedaco in pedacos:
          linhas = pedaco.values.tolist()
          #um "%s" para cada coluna do CSV
          marcadores = ", ".join(["%s"] * len(pedaco.columns))
          comando = f"INSERT INTO {tabela} VALUES ({marcadores})"
          banco.inserir_em_lote(conexao, comando, linhas)
          total += len(linhas)

      print("      ->", total, "linhas em", tabela)
   


def main():
    print("=== FASE 1: EXTRACAO + CAMADA RAW ===")
    try:
        conexao = banco.conectar()

        caminho_zip = baixar_zip()
        print("[2/3] Abrindo o arquivo zip...")
        print("[3/3] Carregando as 4 tabelas RAW...")
        with zipfile.ZipFile(caminho_zip) as zip_aberto:
            for arquivo in config.ARQUIVOS.values():
                carregar_csv(conexao, zip_aberto, arquivo["csv"], arquivo["tabela_raw"])

        conexao.close()
        print("=== Camada RAW concluida com sucesso! ===")
    except Exception as erro:
        print("[ERRO] Algo deu errado:", erro)
        raise

if __name__ == "__main__":
    main()