
from pytube import YouTube, Playlist
from pathlib import Path
import sqlite3
import time
import os

class yd:
    """Classe para baixar vídeos do youtube"""

    def __init__(self, url):
        self.url = url

    def baixar_video(self, window=None, pasta='videos'):

        #cria o banco de dados caso não exista
        banco = models()

        # Busca as informações de músicas e vídeos baixadas
        try:
            consulta = banco.consultar_pasta()['pasta']
            pasta = os.path.join(consulta, 'videos')
        except KeyError:
            pasta = 'videos'

        try:
            if self.url:
                # Verifica se não se trata de uma PlayList
                if 'list' not in self.url:

                    yt = YouTube(self.url)
                    video = yt.streams.get_highest_resolution()
                    window['-MENSAGEM-'].update(f'Baixando,{video.title}', text_color='red')
                    window.finalize()
                    video.download(pasta)

                # Dowload de playlists
                else:
                    playlist = Playlist(self.url)
                    total = len(playlist) # total de links na playlist
                    contador = 0

                    # Torna visível os itens do progess bar
                    window['-MENSAGEM-'].update(visible=True)
                    window['-TOTAL_BAIXADO-'].update(visible=True)
                    window['-PROGRESS BAR-'].update(visible=True)
                    window.finalize()
                    
                    for url_p in playlist:
                        try:
                            video = YouTube(url_p)
                            stream = video.streams.get_highest_resolution()
                            window['-MENSAGEM-'].update(f'Baixando,{stream.title}', text_color='red')
                            window.finalize()
                            time.sleep(1)
                            stream.download(output_path=pasta)
                            contador += 1
                            # Atualiza a barra de progresso e a porcentagem
                            window['-PROGRESS BAR-'].UpdateBar((contador + 1) * (100 / total))
                            window['-MENSAGEM-'].update(f'baixado,{stream.title} restam {total - contador}', text_color='green')
                            window['-TOTAL_BAIXADO-'].update(f'{int((contador + 1) * (100 / total))}%')
                            window.finalize()

                        # Caso ocorra alguma erro desconhecido.
                        except Exception as e:

                            window['-MENSAGEM-'].update(f'erro - {e}')
                            window.finalize()
                            time.sleep(2)
                            window['-MENSAGEM-'].update('')
                            window.finalize()
                            contador += 1
                            window['-PROGRESS BAR-'].UpdateBar((contador + 1) * (100 / total))
                            window['-TOTAL_BAIXADO-'].update(f'{int((contador + 1) * (100 / total))}%')
                            window.finalize()

        except Exception as e:
            
            window['-MENSAGEM-'].update(f'erro - {e}')
            window.finalize()
            time.sleep(2)
            window['-MENSAGEM-'].update('')
            window.finalize()

    def baixar_musica(self, window=None, pasta='musicas'):

        #cria o banco de dados caso não exista
        banco = models()

        # Busca as informações de músicas e vídeos baixadas
        try:
            consulta = banco.consultar_pasta()['pasta']
            pasta = os.path.join(consulta, 'musicas')
        except KeyError:
            pasta = 'musicas'

        try:
            if self.url:
                # Verifica se não se trata de uma PlayList
                if 'list' not in self.url:
                    yt = YouTube(self.url)
                    audio = yt.streams.filter(only_audio=True)[0]
                    window['-MENSAGEM-'].update(f'Baixando - {audio.title}', text_color='red')
                    window.finalize()
                    audio.download(pasta)

                else:
                    playlist = Playlist(self.url)
                    total = len(playlist)
                    contador = 0

                    # Torna visível os itens do progess bar
                    window['-PROGRESS BAR-'].update(visible=True)
                    window['-TOTAL_BAIXADO-'].update(visible=True)
                    window['-MENSAGEM-'].update(visible=True)
                    for url_p in playlist:
                        try:
                            window.finalize()
                            musica = YouTube(url_p)
                            stream = musica.streams.filter(only_audio=True)[0]
                            window['-MENSAGEM-'].update(f'Baixando,{stream.title}', text_color='red')
                            window.finalize()
                            time.sleep(1)
                            stream.download(output_path=pasta)
                            contador += 1
                            # Atualiza a barra de progresso e a porcentagem
                            window['-PROGRESS BAR-'].UpdateBar((contador + 1) * (100 / total))
                            window['-MENSAGEM-'].update(f'baixado,{stream.title} restam {total - contador}', text_color='green')
                            window['-TOTAL_BAIXADO-'].update(f'{int((contador + 1) * (100 / total))}%')
                            window.finalize()

                        except Exception as e:

                            window['-MENSAGEM-'].update(f'erro - {e}')
                            window.finalize()
                            time.sleep(2)
                            window['-MENSAGEM-'].update('')
                            window.finalize()
                            contador += 1
                            window['-PROGRESS BAR-'].UpdateBar((contador + 1) * (100 / total))
                            window['-TOTAL_BAIXADO-'].update(f'{int((contador + 1) * (100 / total))}%')
                            window.finalize()

        except Exception as e:

            window['-MENSAGEM-'].update(f'erro - {e}')
            window.finalize()
            time.sleep(2)
            window['-MENSAGEM-'].update('')
            window.finalize()


#Função que auxilia na atualização da lista de músicas na pasta quando baixada
def listar_arquivos_em_pasta(caminho):
    pasta = Path(caminho)
    if pasta.is_dir():
        arquivos = [[item['nome'], os.path.join(os.getcwd(), item['caminho'])] for item in [{'nome': arquivo.name, 'caminho': str(arquivo)} for arquivo in pasta.iterdir() if arquivo.is_file()]]
        return arquivos
    else:
        return []
    
class models:

    def __init__(self) -> None:
        # Busca o banco de dados
        documents_path = Path(os.path.expanduser('~'), 'Documents')
        self.db_path = Path(documents_path, 'yd.db')

    def valida_db(self):
        #cria o banco de dados
        if not self.db_path.exists():
            conn = sqlite3.connect(self.db_path)
            
            try:
                # Força a criação do arquivo de banco de dados
                conn.execute(
                """  
                CREATE TABLE IF NOT EXISTS config(pasta_padrao VARCHAR);
                            
                """)
                conn.commit()
            except sqlite3.Error as e:
                print(f"Erro: {e}")
            finally:
                conn.close()

    def atualizar_pasta(self, nome_pasta):
        conn = sqlite3.connect(self.db_path)

        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                UPDATE config
                SET pasta_padrao = ?
                """, (nome_pasta,))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro: {e}")
        finally:
            conn.close()

    def consultar_pasta(self):
        conn = sqlite3.connect(self.db_path)

        try:
            cursor = conn.cursor()
            
            dados = cursor.execute(
                
                """
                SELECT * FROM config

                """)

            result = dict(zip(["pasta"], dados.fetchall()[0]))

        except sqlite3.Error as e:
            print(f"Erro: {e}")
        finally:
            conn.close()
            return result
