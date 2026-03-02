from datetime import datetime

class Atendente:
    _id_counter = 1
    _atendentes = {}
    
    def __init__(self, nome, email, cargo):
        self.id = Atendente._id_counter
        Atendente._id_counter += 1
        self.nome = nome
        self.email = email
        self.cargo = cargo
        self.data_contratacao = datetime.utcnow()
        self.ativo = True
        self.pontuacao_atual = 100
        self.avaliacoes = []
        Atendente._atendentes[self.id] = self
    
    def __repr__(self):
        return f'<Atendente {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo,
            'data_contratacao': self.data_contratacao.isoformat(),
            'ativo': self.ativo,
            'pontuacao_atual': self.pontuacao_atual
        }
    
    @classmethod
    def get_all(cls):
        return list(cls._atendentes.values())
    
    @classmethod
    def get_by_id(cls, id):
        return cls._atendentes.get(id)
    
    @classmethod
    def delete(cls, id):
        if id in cls._atendentes:
            del cls._atendentes[id]
