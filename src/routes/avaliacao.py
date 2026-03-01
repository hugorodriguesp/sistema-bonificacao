from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.atendente import Atendente
from src.models.avaliacao import Avaliacao, CriterioAvaliacao
from datetime import datetime

avaliacao_bp = Blueprint('avaliacao', __name__)

@avaliacao_bp.route('/avaliacoes', methods=['POST'])
def create_avaliacao():
    try:
        data = request.get_json()
        
        if not data or not data.get('atendente_id') or not data.get('criterio'):
            return jsonify({'error': 'Atendente ID e critério são obrigatórios'}), 400
        
        # Verificar se atendente existe
        atendente = Atendente.query.get(data['atendente_id'])
        if not atendente:
            return jsonify({'error': 'Atendente não encontrado'}), 404
        
        avaliacao = Avaliacao(
            atendente_id=data['atendente_id'],
            criterio=data['criterio'],
            pontuacao=data.get('pontuacao', 0),
            observacoes=data.get('observacoes', ''),
            avaliador=data.get('avaliador', 'Sistema')
        )
        
        db.session.add(avaliacao)
        
        # Atualizar pontuação do atendente
        atendente.pontuacao_atual += avaliacao.pontuacao
        
        db.session.commit()
        
        return jsonify(avaliacao.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@avaliacao_bp.route('/avaliacoes', methods=['GET'])
def get_avaliacoes():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        atendente_id = request.args.get('atendente_id', type=int)
        
        query = Avaliacao.query
        
        if atendente_id:
            query = query.filter_by(atendente_id=atendente_id)
        
        avaliacoes = query.order_by(Avaliacao.data_avaliacao.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'avaliacoes': [avaliacao.to_dict() for avaliacao in avaliacoes.items],
            'total': avaliacoes.total,
            'pages': avaliacoes.pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@avaliacao_bp.route('/criterios', methods=['GET'])
def get_criterios():
    try:
        criterios = CriterioAvaliacao.query.filter_by(ativo=True).all()
        return jsonify([criterio.to_dict() for criterio in criterios])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@avaliacao_bp.route('/criterios', methods=['POST'])
def create_criterio():
    try:
        data = request.get_json()
        
        if not data or not data.get('nome') or not data.get('pontuacao_padrao'):
            return jsonify({'error': 'Nome e pontuação padrão são obrigatórios'}), 400
        
        criterio = CriterioAvaliacao(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            pontuacao_padrao=data['pontuacao_padrao'],
            tipo=data.get('tipo', 'positivo')
        )
        
        db.session.add(criterio)
        db.session.commit()
        
        return jsonify(criterio.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@avaliacao_bp.route('/relatorio/desempenho', methods=['GET'])
def relatorio_desempenho():
    try:
        # Relatório geral de desempenho
        atendentes = Atendente.query.filter_by(ativo=True).all()
        relatorio = []
        
        for atendente in atendentes:
            avaliacoes = Avaliacao.query.filter_by(atendente_id=atendente.id).all()
            
            total_avaliacoes = len(avaliacoes)
            pontuacao_total = sum(av.pontuacao for av in avaliacoes)
            
            # Classificar desempenho
            if atendente.pontuacao_atual > 120:
                status = 'Excelente'
            elif atendente.pontuacao_atual > 100:
                status = 'Bom'
            elif atendente.pontuacao_atual > 80:
                status = 'Regular'
            else:
                status = 'Necessita Melhoria'
            
            relatorio.append({
                'atendente': atendente.to_dict(),
                'total_avaliacoes': total_avaliacoes,
                'pontuacao_total': pontuacao_total,
                'status': status
            })
        
        # Ordenar por pontuação
        relatorio.sort(key=lambda x: x['atendente']['pontuacao_atual'], reverse=True)
        
        return jsonify(relatorio)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

