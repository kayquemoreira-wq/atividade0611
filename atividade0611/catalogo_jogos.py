"""Catálogo de Jogos - versão Prompt de Comando (Windows).

Execute com:  python catalogo_jogos.py
Os dados ficam salvos em jogos.json (mesma pasta do script).
"""
import json
import os
from collections import Counter

ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jogos.json")

PLATAFORMAS = ["PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile", "Outra"]
GENEROS = ["Ação", "Aventura", "RPG", "Estratégia", "Esporte", "Corrida",
           "Terror", "Simulação", "Puzzle", "Outro"]


# ---------- Persistência ----------
def carregar():
    if not os.path.exists(ARQUIVO):
        return []
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("Aviso: não foi possível ler o arquivo de dados. Iniciando vazio.")
        return []


def salvar(jogos):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(jogos, f, ensure_ascii=False, indent=2)


# ---------- Utilidades ----------
def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPressione ENTER para continuar...")


def escolher_opcao(titulo, opcoes):
    """Mostra uma lista numerada e devolve a opção escolhida."""
    print(f"\n{titulo}")
    for i, op in enumerate(opcoes, 1):
        print(f"  {i}) {op}")
    while True:
        entrada = input("Escolha o número: ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(opcoes):
            escolhida = opcoes[int(entrada) - 1]
            if escolhida in ("Outra", "Outro"):
                digitado = input("Digite o nome: ").strip()
                return digitado or escolhida
            return escolhida
        print("Opção inválida.")


def proximo_id(jogos):
    return max((j["id"] for j in jogos), default=0) + 1


def mostrar_jogo(j):
    status = "[X] Concluído" if j["concluido"] else "[ ] Pendente"
    print(f"{j['id']:>3} | {j['titulo']:<30} | {j['plataforma']:<16} | "
          f"{j['genero']:<12} | {status}")


def mostrar_lista(lista):
    if not lista:
        print("\nNenhum jogo encontrado.")
        return
    print(f"\n{'ID':>3} | {'Título':<30} | {'Plataforma':<16} | "
          f"{'Gênero':<12} | Status")
    print("-" * 90)
    for j in lista:
        mostrar_jogo(j)


# ---------- Funcionalidades ----------
def cadastrar(jogos):
    print("\n=== Cadastrar jogo ===")
    titulo = input("Título: ").strip()
    if not titulo:
        print("O título não pode ser vazio.")
        return
    if any(j["titulo"].lower() == titulo.lower() for j in jogos):
        print("Esse jogo já está cadastrado.")
        return
    plataforma = escolher_opcao("Plataforma:", PLATAFORMAS)
    genero = escolher_opcao("Gênero:", GENEROS)
    jogos.append({
        "id": proximo_id(jogos),
        "titulo": titulo,
        "plataforma": plataforma,
        "genero": genero,
        "concluido": False,
    })
    salvar(jogos)
    print(f"\n'{titulo}' cadastrado com sucesso!")


def listar(jogos):
    print("\n=== Todos os jogos ===")
    mostrar_lista(sorted(jogos, key=lambda j: j["titulo"].lower()))


def marcar_concluido(jogos):
    print("\n=== Marcar como concluído ===")
    mostrar_lista(jogos)
    if not jogos:
        return
    entrada = input("\nID do jogo (ENTER para cancelar): ").strip()
    if not entrada.isdigit():
        return
    for j in jogos:
        if j["id"] == int(entrada):
            j["concluido"] = not j["concluido"]
            salvar(jogos)
            estado = "concluído" if j["concluido"] else "pendente"
            print(f"'{j['titulo']}' agora está {estado}.")
            return
    print("ID não encontrado.")


def pesquisar(jogos):
    print("\n=== Pesquisar título ===")
    termo = input("Digite parte do título: ").strip().lower()
    if not termo:
        return
    mostrar_lista([j for j in jogos if termo in j["titulo"].lower()])


def remover(jogos):
    print("\n=== Remover jogo ===")
    mostrar_lista(jogos)
    if not jogos:
        return
    entrada = input("\nID do jogo (ENTER para cancelar): ").strip()
    if not entrada.isdigit():
        return
    for j in jogos:
        if j["id"] == int(entrada):
            if input(f"Remover '{j['titulo']}'? (s/n): ").lower() == "s":
                jogos.remove(j)
                salvar(jogos)
                print("Removido.")
            return
    print("ID não encontrado.")


def estatisticas(jogos):
    print("\n=== Estatísticas ===")
    total = len(jogos)
    if total == 0:
        print("Nenhum jogo cadastrado ainda.")
        return
    concluidos = sum(j["concluido"] for j in jogos)
    print(f"Total de jogos:   {total}")
    print(f"Concluídos:       {concluidos} ({concluidos / total:.0%})")
    print(f"Pendentes:        {total - concluidos}")

    for titulo, campo in (("Por plataforma", "plataforma"), ("Por gênero", "genero")):
        print(f"\n{titulo}:")
        for nome, qtd in Counter(j[campo] for j in jogos).most_common():
            print(f"  {nome:<18} {qtd:>3}  {'#' * qtd}")


# ---------- Menu ----------
def menu():
    jogos = carregar()
    acoes = {
        "1": cadastrar,
        "2": listar,
        "3": marcar_concluido,
        "4": pesquisar,
        "5": estatisticas,
        "6": remover,
    }
    while True:
        limpar_tela()
        print("=" * 40)
        print("        CATÁLOGO DE JOGOS")
        print("=" * 40)
        print("1) Cadastrar jogo")
        print("2) Listar jogos")
        print("3) Marcar/desmarcar como concluído")
        print("4) Pesquisar por título")
        print("5) Estatísticas")
        print("6) Remover jogo")
        print("0) Sair")
        opcao = input("\nEscolha: ").strip()
        if opcao == "0":
            print("Até a próxima!")
            break
        acao = acoes.get(opcao)
        if acao:
            acao(jogos)
        else:
            print("Opção inválida.")
        pausar()


if __name__ == "__main__":
    menu()
