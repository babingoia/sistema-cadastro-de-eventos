import datetime
import json
import os

from Classes import Pessoa, EventoPessoa, Evento

# Estados
sair = 0

# Memoria
pessoas: list = []
eventos: list = []
evento_pessoa = []

# Cache
pessoas_cache: dict = {}
eventos_cache: dict = {}
ligacoes_cache: dict = {}


def importar_arquivos():
    global pessoas, eventos, evento_pessoa

    path_pessoas = 'Arquivos/Pessoas/'
    path_eventos = 'Arquivos/Eventos/'
    path_ligacao = 'Arquivos/Ligacoes/'

    for file in os.listdir(path_pessoas):
        file_abridos = open(path_pessoas + file, 'r')
        dados = json.load(file_abridos)
        pessoa = Pessoa(dados["id"], dados["nome"], dados["email"], dados["preferencias"])
        pessoas.append(pessoa)

    for file in os.listdir(path_eventos):
        file_abridos = open(path_eventos + file, 'r')
        dados = json.load(file_abridos)
        data = datetime.datetime.fromisoformat(dados["data"].strip('"'))
        evento = Evento(dados["nome"], dados["temas"], data)
        eventos.append(evento)

    for file in os.listdir(path_ligacao):
        file_abridos = open(path_ligacao + file, 'r')
        dados = json.load(file_abridos)
        ligacao = EventoPessoa(dados["id_pessoa"], dados["nome_evento"])
        evento_pessoa.append(ligacao)

    atualizar_cache()

def exportar_memoria():
    global pessoas, eventos, evento_pessoa

    path_pessoas = 'Arquivos/Pessoas/'
    path_eventos = 'Arquivos/Eventos/'
    path_ligacoes = 'Arquivos/Ligacoes/'

    for pessoa in pessoas:
        with open(path_pessoas + pessoa.nome + ".json", 'w') as fp:
            json.dump(pessoa.__dict__, fp)

    for evento in eventos:
        evento_dict = {"nome": evento.nome,
                       "temas": evento.temas,
                       "data": json.dumps(evento.data.isoformat())
                       }
        with open(path_eventos + evento.nome + ".json", 'w') as fp:
            json.dump(evento_dict, fp)

    for ligacao in evento_pessoa:
        with open(path_ligacoes + str(ligacao.id_pessoa) + ligacao.nome_evento + ".json", 'w') as fp:
            json.dump(ligacao.__dict__, fp)


def atualizar_cache():
    global pessoas_cache, pessoas, evento_pessoa, ligacoes_cache, eventos, eventos_cache

    print("Atualizando cache...")
    pessoas_cache = {pessoa.id: pessoa for pessoa in pessoas}
    eventos_cache = {evento.nome: evento for evento in eventos}
    ligacoes_cache = {ligacao.id_pessoa: ligacao.nome_evento for ligacao in evento_pessoa}
    print("Cache atualizado.")


def criar_decoy():
    global pessoas, eventos

    pessoa = Pessoa(1, "Marcos andrade", "marcos@gmail.com", ['filmes', 'comédia'])
    pessoas.append(pessoa)

    evento = Evento("festa do terror", ['terror', 'festa'], datetime.datetime(2025, 10, 20))
    eventos.append(evento)

    eventos.append(Evento("baile das mascaras", ['mascaras', 'baile'], datetime.datetime(2026, 12, 30)))
    atualizar_cache()


def criar_evento():
    global eventos

    print("Ok, você escolheu cadastrar um evento, é isso mesmo que deseja?")
    print("1 -> Sim, qualquer outra coisa = não")
    confirm = int(input())

    if confirm != 1:
        return

    while True:
        check_eventos = 0

        print("Ok, primeiro digite o nome do evento")
        nome = input().strip().lower()

        for evento in eventos:
            if nome == evento.nome:
                check_eventos = 1

        if check_eventos == 1:
            print("Esse nome já existe, por favor escolher outro.")
        else:
            break

    print(nome)

    temas = []
    while True:

        print("Agora digite o tema do evento, um de cada vez se tiver mais de um.")
        tema = input().strip().lower()
        print(tema)

        temas.append(tema)
        print(temas)

        print("Deseja colocar mais algum tema?")
        print("1 -> Sim, qualquer coisa pra não.")
        confirm = input()

        if confirm.isdigit():
            if int(confirm) != 1:
                break
        else:
            break

    print("Qual ano será o evento?")
    ano = int(input().strip())

    print("Qual será o mês?")
    mes = int(input().strip())

    print("Qual será o dia?")
    dia = int(input().strip())

    data = datetime.datetime(ano, mes, dia)

    evento = Evento(nome, temas, data)
    eventos.append(evento)
    atualizar_cache()


def criar_pessoa():
    global pessoas

    print("Ok, você escolheu cadastrar uma pessoa, é isso mesmo que deseja?")
    print("1 -> Sim, qualquer outra coisa = não")
    confirm = int(input())

    if confirm != 1:
        return

    print("Primeiro digite o nome da pessoa")
    nome = input()
    print(nome)

    print("O email da pessoa:")
    email = input()
    print(email)

    preferencias = []
    while True:

        print("Agora digite a preferencia da pessoa, uma de cada vez se tiver mais de uma.")
        preferencia = input().strip().lower()
        print(preferencia)

        preferencias.append(preferencia)
        print(preferencias)

        print("Deseja colocar mais alguma preferencia?")
        print("1 -> Sim, qualquer coisa pra não.")
        confirm = input()

        if confirm.isdigit():
            if int(confirm) != 1:
                break
        else:
            break

    id = len(pessoas) + 1

    pessoa = Pessoa(id, nome, email, preferencias)
    pessoas.append(pessoa)
    atualizar_cache()


def listar(escolha: int):
    global pessoas, eventos, evento_pessoa

    match escolha:
        case 1:
            for pessoa in pessoas:
                print(pessoa.id)
                print(pessoa.nome)
                print(pessoa.email)
                print(pessoa.preferencias)
        case 2:
            for evento in eventos:
                print(evento.nome)
                print(evento.temas)
                print(evento.data)
        case 3:
            for ligacao in evento_pessoa:
                print(ligacao.id_pessoa)
                print(ligacao.nome_evento)


def inscrever_pessoa_em_evento():
    global eventos, pessoas, evento_pessoa

    pessoa = procurar_obj(1)
    evento = procurar_obj(2)

    print("Evento e Pessoa encontrados. Ligando eles.")
    ligacao = EventoPessoa(pessoa.id, evento.nome)
    evento_pessoa.append(ligacao)
    atualizar_cache()


def procurar_obj(escolha):
    global eventos_cache, pessoas_cache, evento_pessoa

    match escolha:
        case 1:
            listar(1)
            while True:
                try:
                    print("Escolha por id, qual pessoa deseja usar.")
                    id_pessoa = int(input().strip())

                    if pessoas_cache[id_pessoa]:
                        return pessoas_cache[id_pessoa]
                    else:
                        print("Id de pessoa não encontrado.")

                except ValueError:
                    print("Valor não numérico encontrado.")
        case 2:
            listar(2)
            while True:
                print("Escolha por nome, qual evento deseja usar.")
                nome_evento = input().strip().lower()

                if eventos_cache[nome_evento]:
                    return eventos_cache[nome_evento]
                else:
                    print("Evento não encontrado.")


def procurar_eventos_em_pessoa():
    global eventos_cache, pessoas, evento_pessoa

    print("Deseja mesmo procurar todos os eventos que uma pessoa está inscrita?")
    print("1 -> sim, qualquer outro valor para não")
    confirm = int(input())

    if confirm != 1:
        return

    pessoa = procurar_obj(1)

    nomes_eventos_da_pessoa = []

    for ligacao in evento_pessoa:
        if ligacao.id_pessoa == pessoa.id:
            nomes_eventos_da_pessoa.append(ligacao.nome_evento)

    for nome in nomes_eventos_da_pessoa:
        print(eventos_cache[nome].nome)
        print(eventos_cache[nome].temas)
        print(eventos_cache[nome].data)


def procurar_pessoas_em_eventos():
    global eventos, pessoas_cache, evento_pessoa

    print("Deseja mesmo procurar todas as pessoas inscritas em um evento?")
    print("1 -> sim, qualquer outro valor para não")
    confirm = int(input())

    if confirm != 1:
        return

    evento = procurar_obj(2)

    ids_pessoas_no_evento = []

    for ligacao in evento_pessoa:
        if ligacao.nome_evento == evento.nome:
            ids_pessoas_no_evento.append(ligacao.id_pessoa)

    for id in ids_pessoas_no_evento:
        print(pessoas_cache[id].nome)
        print(pessoas_cache[id].email)
        print(pessoas_cache[id].preferencias)


def escolher_funcao(funcao):
    global sair
    match funcao:
        case 1:
            criar_pessoa()
        case 2:
            criar_evento()
        case 3:
            print("Deseja listar pessoas ou eventos?")
            print("1 -> Pessoas")
            print("2 -> Eventos")
            print("qualquer outro retorna")
            escolha = int(input())

            listar(escolha)
        case 4:
            inscrever_pessoa_em_evento()
        case 5:
            procurar_eventos_em_pessoa()
        case 6:
            procurar_pessoas_em_eventos()
        case 7:
            pass
        case 8:
            pass
        case 9:
            sair = -1


def main():
    try:
        print("Bem vindo ao criador de eventos! Por favor, selecione o que deseja fazer.")
        print("1 -> Cadastrar uma Pessoa")
        print("2 -> Cadastrar Evento")
        print("3 -> Listar")
        print("4 -> Inscrever Pessoa em evento")
        print("5 -> Procurar Inscrições de uma Pessoa")
        print("6 -> Procurar Pessoas de um evento")
        print("7 -> Criar Análise Pessoa")
        print("8 -> Criar Análise Evento")
        print("9 -> Sair")
        funcao = int(input())
        escolher_funcao(funcao)
    except ValueError:
        print("Por favor insira a função corretamente.")


importar_arquivos()
while True:
    if sair == -1:
        exportar_memoria()
        break
    main()
