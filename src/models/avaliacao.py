from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Avaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    atendente_id = db.Column(db.Integer, db.ForeignKey('atendente.id'), nullable=False)
    criterio = db.Column(db.String(100), nullable=False)
    pontuacao = db.Column(db.Integer, nullable=False)
    observacoes = db.Column(db.Text)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)
    avaliador = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'<Avaliacao {self.criterio} - {self.pontuacao} pontos>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'atendente_id': self.atendente_id,
            'criterio': self.criterio,
            'pontuacao': self.pontuacao,
            'observacoes': self.observacoes,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'avaliador': self.avaliador
        }

class CriterioAvaliacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    pontuacao_padrao = db.Column(db.Integer, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'positivo' ou 'negativo'
    ativo = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<CriterioAvaliacao {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'pontuacao_padrao': self.pontuacao_padrao,
            'tipo': self.tipo,
            'ativo': self.ativo
        }

