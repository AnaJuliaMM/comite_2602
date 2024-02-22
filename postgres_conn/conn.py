import psycopg2
import json

try:
    # Conectar com o banco de dados
    conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="12345678",
                database="playlist"
            )
    cursor = conn.cursor()

   # Abre o arquivo 'dados.json' para leitura
    with open('./output.json', 'r', encoding='utf-8') as arquivo:
    # Carrega os dados JSON do arquivo em um dicionário Python
        dados = json.load(arquivo)

    # cursor.execute(
    #        f"INSERT INTO Musica ( nome, duracao_ms, artistas, nome_album, data_lancamento, total_musicas_album) VALUES "
    #         f"('{dados['tracks']['items'][0]['track']['name']}', "
    #         f"{dados['tracks']['items'][0]['track']['duration_ms']}, '{dados['tracks']['items'][0]['track']['artists'][0]['name']}', "
    #         f"'{dados['tracks']['items'][0]['track']['album']['name']}', '{dados['tracks']['items'][0]['track']['album']['release_date']}', "
    #         f"{dados['tracks']['items'][0]['track']['album']['total_tracks']})"
    #     )



    for track in dados["tracks"]["items"]['track']:
        try:

            # Extrair os nomes dos artistas
            nomes_artistas = [artista['name'] for artista in track['album']['artists']]

            # Juntar os nomes dos artistas em uma única string separada por vírgulas
            artistas_str = ', '.join(nomes_artistas)


            cursor.execute(
            f"INSERT INTO Musica ( nome, duracao_ms, artistas, nome_album, data_lancamento, total_musicas_album) VALUES "
                f"('{track['name']}', "
                f"{ track['duration_ms']}, '{artistas_str}', "
                f"'{track['album']['name']}', '{track['album']['release_date']}', "
                f"{track['album']['total_tracks']})"
            )
        except psycopg2.Error as e:
            print("Erro ao inserir dados no PostgreSQL:", e)



    conn.commit()
    result = cursor.fetchall()
    print(result)
    cursor.close()
    conn.close()


except Exception as e:
    print(e)
finally:
    if conn is not None:
        cursor.close()
        conn.close()
        print('PostgreSQL connection is closed')

