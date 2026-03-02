from flask import Blueprint, request, jsonify
from src.models.atendente import Atendente

atendente_bp = Blueprint('atendente', __name__)

@atendente_bp.route('/atendentes', methods=['GET'])
def get_atendentes():
    atendentes = [a.to_dict() for a in Atendente.get_all()]
    return jsonify(atendentes), 200

@atendente_bp.route('/atendentes', methods=['POST'])
def create_atendente():
    data = request.get_json()
    if not data or not all(k in data for k in ['nome', 'email', 'cargo']):
        return jsonify({'error': 'Dados incompletos'}), 400
    
    atendente = Atendente(data['nome'], data['email'], data['cargo'])
    return jsonify(atendente.to_dict()), 201

@atendente_bp.route('/atendentes/<int:id>', methods=['GET'])
def get_atendente(id):
    atendente = Atendente.get_by_id(id)
    if not atendente:
        return jsonify({'error': 'Atendente não encontrado'}), 404
    return jsonify(atendente.to_dict()), 200

@atendente_bp.route('/atendentes/<int:id>', methods=['PUT'])
def update_atendente(id):
    atendente = Atendente.get_by_id(id)
    if not atendente:
        return jsonify({'error': 'Atendente não encontrado'}), 404
    
    data = request.get_json()
    if 'nome' in data:
        atendente.nome = data['nome']
    if 'email' in data:
        atendente.email = data['email']
    if 'cargo' in data:
        atendente.cargo = data['cargo']
    
    return jsonify(atendente.to_dict()), 200

@atendente_bp.route('/atendentes/<int:id>', methods=['DELETE'])
def delete_atendente(id):
    atendente = Atendente.get_by_id(id)
    if not atendente:
        return jsonify({'error': 'Atendente não encontrado'}), 404
    
    Atendente.delete(id)
    return '', 204
