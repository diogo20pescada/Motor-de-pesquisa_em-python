import tkinter as tk
from tkinter import scrolledtext
from googlesearch import search
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import re

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
stopwords_portugues = set(stopwords.words('portuguese'))

def obter_palavras_chave(pergunta):
    tokens = word_tokenize(pergunta.lower())
    palavras_chave = [palavra for palavra in tokens if palavra.isalnum() and palavra not in stopwords_portugues]
    return palavras_chave

def pesquisar_google(query, num_resultados=1): # Limitando a 1 resultado para simplificar
    resultados = []
    try:
        for j in search(query, num_resultados, num_resultados, 2):
            resultados.append(j)
    except Exception as e:
        resultados = (f"Erro ao pesquisar no Google: {e}")
    return resultados

def obter_html(url):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()
        return resposta.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return None

def extrair_texto(html):
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        texto = ' '.join(soup.stripped_strings)
        return texto
    return None

def obter_resposta_refinada(pergunta, resultados_google):
    if resultados_google:
        url = resultados_google[0]
        html = obter_html(url)
        texto = extrair_texto(html)
        if texto:
            # Tenta encontrar números no texto
            numeros = re.findall(r'\b\d+(\.\d+)?\b', texto)
            if numeros:
                return f"Possível resposta numérica encontrada em {url}: {numeros[0]}"
            else:
                return f"Encontrei informações em {url}, mas não consegui extrair um número como resposta."
        else:
            return f"Não consegui acessar ou extrair texto de {url}."
    else:
        return "Não encontrei resultados relevantes no Google."


def processar_pergunta():
    pergunta_usuario = entrada_pergunta.get()
    area_resposta.config(state=tk.NORMAL)
    area_resposta.delete(1.0, tk.END)

    resultados_google = pesquisar_google(pergunta_usuario)
    if resultados_google:
        resposta_ia = obter_resposta_refinada(pergunta_usuario, resultados_google)
        area_resposta.insert(tk.END, resposta_ia)
    else:
        area_resposta.insert(tk.END, "Não encontrei resultados relevantes no Google para esta pergunta.")

    area_resposta.config(state=tk.DISABLED)
    entrada_pergunta.delete(0, tk.END)

# GUI (inalterada)
janela = tk.Tk()
janela.title("IA com Busca no Google")

label_pergunta = tk.Label(janela, text="Faça sua pergunta:")
label_pergunta.pack(padx=10, pady=10, anchor=tk.W)
entrada_pergunta = tk.Entry(janela, width=60)
entrada_pergunta.pack(padx=10, pady=5, fill=tk.X)

botao_perguntar = tk.Button(janela, text="Perguntar", command=processar_pergunta)
botao_perguntar.pack(padx=10, pady=10)

label_resposta = tk.Label(janela, text="Resposta:")
label_resposta.pack(padx=10, pady=10, anchor=tk.W)
area_resposta = scrolledtext.ScrolledText(janela, width=60, height=15, state=tk.DISABLED)
area_resposta.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

janela.mainloop()
