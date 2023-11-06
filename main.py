from codes import yd, listar_arquivos_em_pasta, models
import PySimpleGUI as sg
from pathlib import Path
import subprocess
import os, sys
import time

#cria o banco de dados caso não exista
banco = models()
banco.valida_db()

# Busca as informações de músicas e vídeos baixadas
try:
    pasta_consulta = banco.consultar_pasta()['pasta']
except KeyError:
    pasta_consulta = ''

if pasta_consulta:
    print("existe", pasta_consulta)
    data_musica = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'musicas'))
    data_video = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'videos'))

# Tema do aplicativo                               
sg.theme('DefaultNoMoreNagging')

# Definir o layout da janela com a tabela, o Column é usado para deixa centralizado o conteúdo
layout = [
    #Título
    [sg.Column(
        [
            [sg.Text('AKSI - Baixador de Videos e Músicas 🎶📺', font=('Any 16'))]
        ],element_justification='c',vertical_alignment='c',expand_x=True, expand_y=True
    )],
    #coluna para link do youtube
    [sg.Column(
     [
        # Barra de progrosse de dowload de playlist
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS BAR-', visible=False), sg.Text('0%', key='-TOTAL_BAIXADO-', visible=False)],
        # Mensagens de avisos
        [sg.Text('', font=('Any 13'),text_color='green',key='-MENSAGEM-', size=(80))],
        # Campo que recebe o link do youtube URLInput
        [sg.Text('Url do vídeo do Youtube', font=('Any 14'))],
        [sg.Input('', size=(80), key='URLInput')]
     ],element_justification='c',vertical_alignment='c',expand_x=True, expand_y=True
    )],

    #coluna para botão de baixar
    [sg.Column(
        [
            [sg.Button('Baixar Música', size=(15, 1)),
             sg.Button('Baixar Vídeo', size=(15, 1))]
        ],
        element_justification='c', vertical_alignment='c', expand_x=True, expand_y=True
    )],

    #Tabela de Musicas baixadas
    [sg.Text(f'{len(data_musica)} - Musicas na pasta',size=(100), justification='center', font=('Any 12'))],
    [sg.Table(values=data_musica, headings=['Nome', 'Caminho'], auto_size_columns=False,
              display_row_numbers=False, justification='left', num_rows=5, col_widths=(30, 70), key='TableMusica')],

    #Tabela de vídeos baixados
    [sg.Text(f'{len(data_video)} - Vídeos na pasta',size=(100), justification='center', font=('Any 12'))],
    [sg.Table(values=data_video, headings=['Nome', 'Caminho'], auto_size_columns=False,
              display_row_numbers=False, justification='left', num_rows=5, col_widths=(30, 70), key='TableVideo')],
    
    #Botões
    [sg.Button('Abrir Pasta Videos', size=(15, 1)),
     sg.Button('Abrir Pasta Músicas', size=(15, 1)),
     sg.Text(f'Pasta atual: {pasta_consulta}', size=55),
     sg.Button('Selecionar pasta de Download', button_color='DimGray')]

    ]

# Verifica se o programa está sendo executado como um executável compilado
if getattr(sys, 'frozen', False):
    # Caminho para o ícone quando o programa é um executável
    icon_path = os.path.join(sys._MEIPASS, 'favicons\\favicon_g.ico')
else:
    # Caminho para o ícone quando o programa é um script
    icon_path = 'favicons\\favicon_g.ico'

# Cria a janela da aplicação
window = sg.Window('AKSI Musics and Videos', layout, finalize=True, size=(950,500), icon=icon_path)

while True:

    # Faz as leitura dos eventos que ocorre no app
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Fechar'):
        break

    if event == 'Baixar Música':

        # Passo uma instância do progress bar para ser alterada conforme baixa as músicas
        progress_bar = window['-PROGRESS BAR-']
        #Link inserido pelo usuário
        url = values['URLInput']

        if url:
            baixar = yd(url)
            baixar.baixar_musica(window=window)

            # Após o download, atualize os dados da tabela de músicas
            data_musica = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'musicas'))
            window['TableMusica'].update(data_musica)
            window['-TOTAL_BAIXADO-'].update('')
            window['-MENSAGEM-'].update('Musicas Baixadas!', text_color='green')
            window.finalize()
            time.sleep(2)
            window['-MENSAGEM-'].update('')
            progress_bar.update(visible=False)
            window['-TOTAL_BAIXADO-'].update(visible=False)
            window.finalize()

    if event == 'Baixar Vídeo':

        # Passo uma instância do progress bar para ser alterada conforme baixa as músicas
        progress_bar = window['-PROGRESS BAR-']
         #Link inserido pelo usuário
        url = values['URLInput']

        if url:
            baixar = yd(url)
            baixar.baixar_video(window=window)

            # Após o download, atualize os dados da tabela de músicas
            data_video = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'videos'))
            window['TableVideo'].update(data_video)
            window['-TOTAL_BAIXADO-'].update('')
            window['-MENSAGEM-'].update('Vídeos Baixados!', text_color='green')
            window.finalize()
            time.sleep(2)
            window['-MENSAGEM-'].update('')
            progress_bar.update(visible=False)
            window['-TOTAL_BAIXADO-'].update(visible=False)
            window.finalize()

    # Abre a pasta onde estão salvos os vídeos
    if event == 'Abrir Pasta Videos':
        caminho_da_pasta = os.path.join(pasta_consulta, 'videos').replace("\\", "/").replace("/","\\")
        subprocess.Popen(['explorer', caminho_da_pasta])
    
    # Abre a pasta onde estão salvas as musicas
    if event == 'Abrir Pasta Músicas':
        caminho_da_pasta = os.path.join(pasta_consulta, 'musicas').replace("\\", "/").replace("/","\\")
        subprocess.Popen(['explorer', caminho_da_pasta])

    #Altera a pasta de download
    if event == 'Selecionar pasta de Download':
        text = sg.popup_get_folder('Pasta de Download')
        resultado_alteracao = banco.atualizar_pasta(nome_pasta=text)

        if resultado_alteracao:
            # Busca as informações de músicas e vídeos baixadas
            try:
                pasta_consulta = banco.consultar_pasta()['pasta']
            except KeyError:
                pasta_consulta = ''

            data_musica = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'musicas'))
            data_video = listar_arquivos_em_pasta(os.path.join(pasta_consulta, 'videos'))
            window['TableMusica'].update(data_musica)
            window['TableVideo'].update(data_video)

            sg.popup('Sucesso', 'A pasta selecionada foi... ', text)
        else:
            sg.popup('Falha', 'Pasta Selecionada é inválida')


#Finaliza o app
window.close()
