#!/bin/bash
if ! command -v pyenv &> /dev/null; then                                             
      echo "pyenv não encontrado. Instale com: brew install pyenv"                     
      exit 1                                                                          
fi

cd etl

echo "Configurando Python 3.12..."                                                   
pyenv local 3.12

echo "Atualizando pip..."
pip install --upgrade pip

echo "Criando ambiente virtual..."
~/.pyenv/versions/3.12.13/bin/python3 -m venv .venv
source .venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Ambiente configurado!"
