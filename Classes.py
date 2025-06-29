from datetime import datetime


class Pessoa:
    def __init__(self, id: int, nome: str, email: str, preferencias: list):
        self.id: int = id
        self.nome: str = nome
        self.email: str = email
        self.preferencias: list = preferencias


class Evento:
    def __init__(self, nome: str, tema: list, data: datetime):
        self.nome: str = nome
        self.temas: list = tema
        self.data: datetime = data


class EventoPessoa:
    def __init__(self, id_pessoa: int, nome_evento: str):
        self.id_pessoa: int = id_pessoa
        self.nome_evento: str = nome_evento
