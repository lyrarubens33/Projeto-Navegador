#main.py
import os
from logica import (
    carregar_urls, construir_arvore, obter_links_disponiveis,
    carregar_pagina, buscar_no, CAMINHO_DATABASE, PASTA_WEB_PAGES
)


def exibir_interface(url_atual, historico, links_disponiveis):
    os.system('cls' if os.name == 'nt' else 'clear')


    print("=" * 60)
    print(f" Historico de Visitas: {historico if historico else '[ ]'}")
    print(f" Home: [{url_atual if url_atual else ''}]")
    print("=" * 60)
   
    print(" Links disponiveis:")
    if links_disponiveis:
        for link in links_disponiveis:
            print(f"   /{link}")
    else:
        print("   (Nenhum sublink disponivel a partir desta pagina)")


    if url_atual:
        print("\n" + "-" * 25 + " CONTEUDO DA PAGINA " + "-" * 25)
        print(carregar_pagina(url_atual))
        print("-" * 70)
    else:
        print("\n[Navegador Inicializado - Digite um dominio raiz para comecar]")
        print("-" * 70)


    print(" [URL] ou Comandos: #back | #showhist | #add <url> | #remover <url> | #help | #sair")
    print("-" * 70)


def navegador():
    historico = []  
    url_atual = ""  


    while True:
        urls_no_banco = carregar_urls()
        arvore = construir_arvore(urls_no_banco)
        links_disponiveis = obter_links_disponiveis(arvore, url_atual)


        exibir_interface(url_atual, historico, links_disponiveis)
        entrada = input("url: ").strip()


        if not entrada:
            continue


        if entrada == "#sair":
            print("\nEncerrando o simulador...")
            break


        elif entrada == "#help":
            print("""
----------------------- AJUDA SIMULADOR -----------------------
#sair          -> Encerra o programa com sucesso.
#back          -> Desempilha a ultima pagina visitada e retorna.
#showhist      -> Exibe de forma detalhada a situacao da Pilha.
#add <url>     -> Cadastra um novo dominio ou subpasta (Max: 2 filhos).
#remover <url> -> Exclui o mapeamento logico e fisico da URL.
---------------------------------------------------------------""")
            input("Pressione Enter para retornar...")
            continue


        elif entrada == "#back":
            if historico:
                url_atual = historico.pop()
            else:
                url_atual = ""
                print("\nVoce retornou para a HOME inicial.")
                input("\nPressione Enter para continuar...")
            continue


        elif entrada == "#showhist":
            print("\n------- HISTORICO COMPLETO (PILHA) -------")
            if historico:
                for i, url in enumerate(historico, 1):
                    print(f" Nivel {i}: [{url}]")
            else:
                print(" O historico esta vazio.")
            print("------------------------------------------")
            input("\nPressione Enter...")
            continue


        elif entrada.startswith("#add "):
            nova_url = entrada.replace("#add ", "").strip()


            if not nova_url.startswith("/") and not nova_url.startswith(("www.", "http://", "https://")):
                print("\n[Erro]: Formato de URL invalido. Use www., http:// ou https:// para dominios raiz.")
                input("\nPressione Enter...")
                continue


            if nova_url in urls_no_banco:
                print("\n[Erro]: Esta URL ja consta no banco de dados.")
                input("\nPressione Enter...")
                continue


            if "/" in nova_url:
                partes_nova = nova_url.split("/")
                caminho_pai = "/".join(partes_nova[:-1])
               
                if caminho_pai:  
                    no_pai = buscar_no(arvore, caminho_pai)
                    if no_pai and len(no_pai) >= 2:
                        print("\n[Erro de Diretorio]: Esta pagina pai ja atingiu o limite maximo de 2 links internos!")
                        input("\nPressione Enter...")
                        continue


            try:
                os.makedirs(PASTA_WEB_PAGES, exist_ok=True)
                nome_arq = nova_url.replace("/", "_")
                if not nome_arq.endswith(".txt"):
                    nome_arq += ".txt"


                caminho_p = os.path.join(PASTA_WEB_PAGES, nome_arq)
               
                with open(caminho_p, "w", encoding="utf-8") as p:
                    p.write("======================================\n")
                    p.write(f"       BEM-VINDO AO SITE: {nova_url}\n")
                    p.write("======================================\n")
                    p.write("\n[Esta pagina foi criada com sucesso pelo sistema]")


                with open(CAMINHO_DATABASE, "a", encoding="utf-8") as f:
                    f.write(f"{nova_url}\n")


                print(f"\nURL '{nova_url}' registrada com sucesso!")
            except Exception as e:
                print(f"Erro no processamento de I/O: {e}")
            input("\nPressione Enter...")
            continue


        elif entrada.startswith("#remover "):
            url_para_remover = entrada.replace("#remover ", "").strip()
            if url_para_remover not in urls_no_banco:
                print(f"\nA URL '{url_para_remover}' nao foi encontrada.")
                input("\nPressione Enter...")
                continue


            try:
                urls_no_banco.remove(url_para_remover)
                with open(CAMINHO_DATABASE, "w", encoding="utf-8") as f:
                    for url in urls_no_banco:
                        f.write(f"{url}\n")


                nome_arq = url_para_remover.replace("/", "_")
                if not nome_arq.endswith(".txt"):
                    nome_arq += ".txt"
                caminho_arquivo = os.path.join(PASTA_WEB_PAGES, nome_arq)


                if os.path.exists(caminho_arquivo):
                    os.remove(caminho_arquivo)


                if url_atual == url_para_remover:
                    url_atual = ""
               
                while url_para_remover in historico:
                    historico.remove(url_para_remover)


                print(f"\nURL '{url_para_remover}' removida com sucesso.")
            except Exception as e:
                print(f"Erro na remocao fisica: {e}")
            input("\nPressione Enter...")
            continue


        destino = entrada
        if entrada.startswith("/"):
            sublink = entrada.replace("/", "", 1)
            if url_atual:
                if sublink in links_disponiveis:
                    destino = f"{url_atual}/{sublink}"
                else:
                    destino = f"{url_atual}{entrada}"
            else:
                destino = sublink


        if destino in urls_no_banco:
            if url_atual and url_atual != destino:
                historico.append(url_atual)
            url_atual = destino
        else:
            print(f"\nErro 404: O destino '{destino}' nao existe no banco de dados.")
            input("Pressione Enter...")


if __name__ == "__main__":
    navegador()