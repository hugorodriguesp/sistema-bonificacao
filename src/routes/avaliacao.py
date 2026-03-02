from flask import Blueprint, request, jsonify
from src.models.avaliacao import Avaliacao
from src.models.atendente import Atendente

avaliacao_bp = Blueprint('avaliacao', __name__)

@avaliacao_bp.route('/avaliacoes', methods=['GET'])
def get_avaliacoes():
    avaliacoes = [a.to_dict() for a in Avaliacao.get_all()]
    return jsonify(avaliacoes), 200

@avaliacao_bp.route('/avaliacoes', methods=['POST'])
def create_avaliacao():
    data = request.get_json()
    if not data or not all(k in data for k in ['atendente_id', 'criterio', 'observacoes', 'avaliador']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    atendente = Atendente.get_by_id(data['atendente_id'])
    if not atendente:
        return jsonify({'error': 'Atendente não encontrado'}), 404
    
    avaliacao = Avaliacao(data['atendente_id'], data['criterio'], data['observacoes'], data['avaliador'])
    
    # Atualizar pontuação do atendente
    atendente.pontuacao_atual += avaliacao.pontos
    atendente.avaliacoes.append(avaliacao)
    
    return jsonify(avaliacao.to_dict()), 201

@avaliacao_bp.route('/avaliacoes/<int:id>', methods=['GET'])
def get_avaliacao(id):
    avaliacao = Avaliacao.get_by_id(id)
    if not avaliacao:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    return jsonify(avaliacao.to_dict()), 200

@avaliacao_bp.route('/avaliacoes/atendente/<int:atendente_id>', methods=['GET'])
def get_avaliacoes_atendente(atendente_id):
    avaliacoes = [a.to_dict() for a in Avaliacao.get_by_atendente(atendente_id)]
    return jsonify(avaliacoes), 200

@avaliacao_bp.route('/avaliacoes/<int:id>', methods=['DELETE'])
def delete_avaliacao(id):
    avaliacao = Avaliacao.get_by_id(id)
    if not avaliacao:
        return jsonify({'error': 'Avaliação não encontrada'}), 404
    
    Avaliacao.delete(id)
    return '', 204

@avaliacao_bp.route('/criterios', methods=['GET'])
def get_criterios():
    return jsonify({
        'positivos': Avaliacao.CRITERIOS_POSITIVOS,
        'negativos': Avaliacao.CRITERIOS_NEGATIVOS
    }), 200

@avaliacao_bp.route('/dashboard', methods=['GET'])
def get_dashboard():
    atendentes = Atendente.get_all()
    total_avaliacoes = len(Avaliacao.get_all())
    
    dashboard = {
        'total_atendentes': len(atendentes),
        'total_avaliacoes': total_avaliacoes,
        'atendentes': [a.to_dict() for a in atendentes],
        'media_pontuacao': sum(a.pontuacao_atual for a in atendentes) / len(atendentes) if atendentes else 0
    }
    
    return jsonify(dashboard), 200
