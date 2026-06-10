#logica.py
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_DATABASE = os.path.join(BASE_DIR, 'database.txt')
PASTA_WEB_PAGES = os.path.join(BASE_DIR, 'web_pages')


def carregar_urls():
    if not os.path.exists(CAMINHO_DATABASE):
        return []
    with open(CAMINHO_DATABASE, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]


def construir_arvore(urls):
    arvore = {}
    for url in urls:
        partes = url.split('/')
        no_atual = arvore
        for parte in partes:
            if not parte:
                continue
            if parte not in no_atual:
                no_atual[parte] = {}
            no_atual = no_atual[parte]
    return arvore


def buscar_no(arvore, url_atual):
    if not url_atual:
        return arvore
    partes = url_atual.split('/')
    no_atual = arvore
    for parte in partes:
        if not parte:
            continue
        if parte in no_atual:
            no_atual = no_atual[parte]
        else:
            return None
    return no_atual


def obter_links_disponiveis(arvore, url_atual):
    no = buscar_no(arvore, url_atual)
    if no is not None and isinstance(no, dict):
        return list(no.keys())
    return []


def carregar_pagina(url):
    if not url:
        return ""


    nome_arquivo = url.replace("/", "_").strip()
    if not nome_arquivo.endswith(".txt"):
        nome_arquivo += ".txt"


    caminho_completo = os.path.join(PASTA_WEB_PAGES, nome_arquivo)


    if os.path.exists(caminho_completo):
        with open(caminho_completo, "r", encoding="utf-8") as f:
            return f.read()


    return f"Erro 404: O arquivo de renderizacao '{nome_arquivo}' nao foi encontrado em disco."
