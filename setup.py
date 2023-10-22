"""Crir executável, funciona somente para windows"""

import os
from pathlib import Path

pasta_atual = Path('.')
nome = 'AKSI-YD 1.0'

for pasta in pasta_atual.iterdir():
    busca_env = list(pasta.glob('Scripts'))
    
    if busca_env:
        pasta_env = str(pasta / 'Scripts' / 'python.exe')
        pasta_installer = str(pasta / 'Scripts' / 'pyinstaller.exe')

caminho_env = os.path.join(os.getcwd(), pasta_env)
caminho_installer = os.path.join(os.getcwd(), pasta_installer)

try:
    os.system(f'''
            {caminho_env} {pasta_installer} --onefile --add-data "favicons;favicons" --noconsole --name="{nome}" --icon="favicons\\favicon_g.ico"  main.py
            ''')
except Exception as e:

    print(f'erro ({e}) , tente executar manualmente em seu terminal!')