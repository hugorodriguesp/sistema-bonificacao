from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.atendente import Atendente
from src.models.avaliacao import Avaliacao

atendente_bp = Blueprint('atendente', __name__)

@atendente_bp.route('/atendentes', methods=['GET'])
def get_atendentes():
    try:
        atendentes = Atendente.query.filter_by(ativo=True).all()
        return jsonify([atendente.to_dict() for atendente in atendentes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@atendente_bp.route('/atendentes', methods=['POST'])
def create_atendente():
    try:
        data = request.get_json()
        
        if not data or not data.get('nome') or not data.get('email'):
            return jsonify({'error': 'Nome e email são obrigatórios'}), 400
        
        # Verificar se email já existe
        existing = Atendente.query.filter_by(email=data['email']).first()
        if existing:
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        atendente = Atendente(
            nome=data['nome'],
            email=data['email'],
            cargo=data.get('cargo', 'Atendente')
        )
        
        db.session.add(atendente)
        db.session.commit()
        
        return jsonify(atendente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@atendente_bp.route('/atendentes/<int:atendente_id>', methods=['GET'])
def get_atendente(atendente_id):
    try:
        atendente = Atendente.query.get_or_404(atendente_id)
        return jsonify(atendente.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@atendente_bp.route('/atendentes/<int:atendente_id>/avaliacoes', methods=['GET'])
def get_avaliacoes_atendente(atendente_id):
    try:
        atendente = Atendente.query.get_or_404(atendente_id)
        avaliacoes = Avaliacao.query.filter_by(atendente_id=atendente_id).order_by(Avaliacao.data_avaliacao.desc()).all()
        return jsonify([avaliacao.to_dict() for avaliacao in avaliacoes])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@atendente_bp.route('/atendentes/<int:atendente_id>/pontuacao', methods=['GET'])
def get_pontuacao_atendente(atendente_id):
    try:
        atendente = Atendente.query.get_or_404(atendente_id)
        
        # Calcular pontuação total baseada nas avaliações
        avaliacoes = Avaliacao.query.filter_by(atendente_id=atendente_id).all()
        pontuacao_total = 100  # Pontuação base
        
        for avaliacao in avaliacoes:
            pontuacao_total += avaliacao.pontuacao
        
        # Atualizar pontuação no banco
        atendente.pontuacao_atual = pontuacao_total
        db.session.commit()
        
        return jsonify({
            'atendente_id': atendente_id,
            'nome': atendente.nome,
            'pontuacao_atual': pontuacao_total,
            'total_avaliacoes': len(avaliacoes)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

