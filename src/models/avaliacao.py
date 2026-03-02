from datetime import datetime

class Avaliacao:
    _id_counter = 1
    _avaliacoes = {}
    
    CRITERIOS_POSITIVOS = {
        'resolucao_primeiro_contato': {'nome': 'Resolução no Primeiro Contato', 'pontos': 5},
        'satisfacao_cliente': {'nome': 'Satisfação do Cliente', 'pontos': 3},
        'tempo_otimizado': {'nome': 'Tempo Médio de Atendimento Otimizado', 'pontos': 2},
        'proatividade': {'nome': 'Proatividade na Solução', 'pontos': 4},
        'empatia': {'nome': 'Empatia e Cortesia', 'pontos': 3},
        'conhecimento': {'nome': 'Conhecimento do Produto/Serviço', 'pontos': 3}
    }
    
    CRITERIOS_NEGATIVOS = {
        'reabertura': {'nome': 'Reabertura de Chamado', 'pontos': -5},
        'insatisfacao': {'nome': 'Insatisfação do Cliente', 'pontos': -4},
        'tempo_excessivo': {'nome': 'Tempo Médio de Espera Excessivo', 'pontos': -3},
        'falta_resolucao': {'nome': 'Falta de Resolução', 'pontos': -7},
        'falta_cortesia': {'nome': 'Falta de Cortesia/Empatia', 'pontos': -6},
        'informacao_incorreta': {'nome': 'Informação Incorreta/Incompleta', 'pontos': -5}
    }
    
    def __init__(self, atendente_id, criterio, observacoes, avaliador):
        self.id = Avaliacao._id_counter
        Avaliacao._id_counter += 1
        self.atendente_id = atendente_id
        self.criterio = criterio
        self.observacoes = observacoes
        self.avaliador = avaliador
        self.data_avaliacao = datetime.utcnow()
        self.pontos = self._calcular_pontos(criterio)
        Avaliacao._avaliacoes[self.id] = self
    
    def _calcular_pontos(self, criterio):
        if criterio in self.CRITERIOS_POSITIVOS:
            return self.CRITERIOS_POSITIVOS[criterio]['pontos']
        elif criterio in self.CRITERIOS_NEGATIVOS:
            return self.CRITERIOS_NEGATIVOS[criterio]['pontos']
        return 0
    
    def to_dict(self):
        return {
            'id': self.id,
            'atendente_id': self.atendente_id,
            'criterio': self.criterio,
            'observacoes': self.observacoes,
            'avaliador': self.avaliador,
            'data_avaliacao': self.data_avaliacao.isoformat(),
            'pontos': self.pontos
        }
    
    @classmethod
    def get_all(cls):
        return list(cls._avaliacoes.values())
    
    @classmethod
    def get_by_id(cls, id):
        return cls._avaliacoes.get(id)
    
    @classmethod
    def get_by_atendente(cls, atendente_id):
        return [a for a in cls._avaliacoes.values() if a.atendente_id == atendente_id]
    
    @classmethod
    def delete(cls, id):
        if id in cls._avaliacoes:
            del cls._avaliacoes[id]
