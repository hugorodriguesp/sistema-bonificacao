from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Atendente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cargo = db.Column(db.String(50), nullable=False)
    data_contratacao = db.Column(db.DateTime, default=datetime.utcnow)
    ativo = db.Column(db.Boolean, default=True)
    pontuacao_atual = db.Column(db.Integer, default=100)
    
    # Relacionamento com avaliações
    avaliacoes = db.relationship('Avaliacao', backref='atendente', lazy=True)
    
    def __repr__(self):
        return f'<Atendente {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'cargo': self.cargo,
            'data_contratacao': self.data_contratacao.isoformat() if self.data_contratacao else None,
            'ativo': self.ativo,
            'pontuacao_atual': self.pontuacao_atual
        }

