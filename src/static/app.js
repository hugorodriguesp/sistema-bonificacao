// Configuração da API
const API_BASE = '/api';

// Estado da aplicação
let atendentes = [];
let avaliacoes = [];
let criterios = [];

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadInitialData();
    showSection('dashboard');
});

// Carregar dados iniciais
async function loadInitialData() {
    try {
        await Promise.all([
            loadAtendentes(),
            loadAvaliacoes(),
            loadCriterios()
        ]);
        updateDashboard();
    } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
    }
}

// Carregar atendentes
async function loadAtendentes() {
    try {
        const response = await fetch(`${API_BASE}/atendentes`);
        if (response.ok) {
            atendentes = await response.json();
        }
    } catch (error) {
        console.error('Erro ao carregar atendentes:', error);
    }
}

// Carregar avaliações
async function loadAvaliacoes() {
    try {
        const response = await fetch(`${API_BASE}/avaliacoes`);
        if (response.ok) {
            const data = await response.json();
            avaliacoes = data.avaliacoes || [];
        }
    } catch (error) {
        console.error('Erro ao carregar avaliações:', error);
    }
}

// Carregar critérios
async function loadCriterios() {
    try {
        const response = await fetch(`${API_BASE}/criterios`);
        if (response.ok) {
            criterios = await response.json();
        }
    } catch (error) {
        console.error('Erro ao carregar critérios:', error);
    }
}

// Mostrar seção
function showSection(sectionName) {
    // Esconder todas as seções
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.style.display = 'none');
    
    // Mostrar seção selecionada
    const targetSection = document.getElementById(`${sectionName}-section`);
    if (targetSection) {
        targetSection.style.display = 'block';
    }
    
    // Carregar dados da seção
    switch(sectionName) {
        case 'dashboard':
            updateDashboard();
            break;
        case 'atendentes':
            renderAtendentes();
            break;
        case 'avaliacoes':
            renderAvaliacoes();
            break;
        case 'relatorios':
            loadRelatorios();
            break;
    }
}

// Atualizar dashboard
function updateDashboard() {
    // Estatísticas gerais
    document.getElementById('total-atendentes').textContent = atendentes.length;
    document.getElementById('total-avaliacoes').textContent = avaliacoes.length;
    
    // Calcular média de pontuação
    const mediaPontuacao = atendentes.length > 0 
        ? Math.round(atendentes.reduce((sum, a) => sum + a.pontuacao_atual, 0) / atendentes.length)
        : 0;
    document.getElementById('media-pontuacao').textContent = mediaPontuacao;
    
    // Melhor performer
    const topPerformer = atendentes.length > 0 
        ? atendentes.reduce((max, a) => a.pontuacao_atual > max.pontuacao_atual ? a : max)
        : null;
    document.getElementById('top-performer').textContent = topPerformer ? topPerformer.nome : '-';
    
    // Ranking
    renderRanking();
    
    // Avaliações recentes
    renderRecentEvaluations();
}

// Renderizar ranking
function renderRanking() {
    const rankingList = document.getElementById('ranking-list');
    const sortedAtendentes = [...atendentes].sort((a, b) => b.pontuacao_atual - a.pontuacao_atual);
    
    if (sortedAtendentes.length === 0) {
        rankingList.innerHTML = '<p class="text-muted">Nenhum atendente cadastrado.</p>';
        return;
    }
    
    let html = '<div class="list-group">';
    sortedAtendentes.forEach((atendente, index) => {
        const status = getStatusClass(atendente.pontuacao_atual);
        const badge = index < 3 ? `<span class="badge bg-warning text-dark">#${index + 1}</span>` : '';
        
        html += `
            <div class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                    ${badge}
                    <strong>${atendente.nome}</strong>
                    <small class="text-muted d-block">${atendente.cargo}</small>
                </div>
                <div class="text-end">
                    <span class="badge bg-primary">${atendente.pontuacao_atual} pts</span>
                    <small class="${status.class} d-block">${status.text}</small>
                </div>
            </div>
        `;
    });
    html += '</div>';
    
    rankingList.innerHTML = html;
}

// Renderizar avaliações recentes
function renderRecentEvaluations() {
    const recentEvaluations = document.getElementById('recent-evaluations');
    const recentAvaliacoes = avaliacoes.slice(0, 5);
    
    if (recentAvaliacoes.length === 0) {
        recentEvaluations.innerHTML = '<p class="text-muted">Nenhuma avaliação encontrada.</p>';
        return;
    }
    
    let html = '<div class="list-group list-group-flush">';
    recentAvaliacoes.forEach(avaliacao => {
        const atendente = atendentes.find(a => a.id === avaliacao.atendente_id);
        const atendenteNome = atendente ? atendente.nome : 'Desconhecido';
        const pontuacaoClass = avaliacao.pontuacao > 0 ? 'text-success' : 'text-danger';
        
        html += `
            <div class="list-group-item">
                <div class="d-flex w-100 justify-content-between">
                    <h6 class="mb-1">${atendenteNome}</h6>
                    <small class="${pontuacaoClass}">${avaliacao.pontuacao > 0 ? '+' : ''}${avaliacao.pontuacao} pts</small>
                </div>
                <p class="mb-1">${avaliacao.criterio}</p>
                <small class="text-muted">${formatDate(avaliacao.data_avaliacao)}</small>
            </div>
        `;
    });
    html += '</div>';
    
    recentEvaluations.innerHTML = html;
}

// Renderizar lista de atendentes
function renderAtendentes() {
    const atendentesList = document.getElementById('atendentes-list');
    
    if (atendentes.length === 0) {
        atendentesList.innerHTML = '<p class="text-muted">Nenhum atendente cadastrado.</p>';
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Nome</th>
                        <th>Email</th>
                        <th>Cargo</th>
                        <th>Pontuação</th>
                        <th>Status</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    atendentes.forEach(atendente => {
        const status = getStatusClass(atendente.pontuacao_atual);
        html += `
            <tr>
                <td><strong>${atendente.nome}</strong></td>
                <td>${atendente.email}</td>
                <td>${atendente.cargo}</td>
                <td><span class="badge bg-primary">${atendente.pontuacao_atual} pts</span></td>
                <td><span class="${status.class}">${status.text}</span></td>
                <td>
                    <button class="btn btn-sm btn-outline-info" onclick="viewAtendenteDetails(${atendente.id})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    atendentesList.innerHTML = html;
}

// Renderizar lista de avaliações
function renderAvaliacoes() {
    const avaliacoesList = document.getElementById('avaliacoes-list');
    
    if (avaliacoes.length === 0) {
        avaliacoesList.innerHTML = '<p class="text-muted">Nenhuma avaliação encontrada.</p>';
        return;
    }
    
    let html = `
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Atendente</th>
                        <th>Critério</th>
                        <th>Pontuação</th>
                        <th>Avaliador</th>
                        <th>Data</th>
                        <th>Observações</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    avaliacoes.forEach(avaliacao => {
        const atendente = atendentes.find(a => a.id === avaliacao.atendente_id);
        const atendenteNome = atendente ? atendente.nome : 'Desconhecido';
        const pontuacaoClass = avaliacao.pontuacao > 0 ? 'text-success' : 'text-danger';
        
        html += `
            <tr>
                <td><strong>${atendenteNome}</strong></td>
                <td>${avaliacao.criterio}</td>
                <td><span class="${pontuacaoClass}">${avaliacao.pontuacao > 0 ? '+' : ''}${avaliacao.pontuacao}</span></td>
                <td>${avaliacao.avaliador}</td>
                <td>${formatDate(avaliacao.data_avaliacao)}</td>
                <td>${avaliacao.observacoes || '-'}</td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    avaliacoesList.innerHTML = html;
}

// Carregar relatórios
async function loadRelatorios() {
    try {
        const response = await fetch(`${API_BASE}/relatorio/desempenho`);
        if (response.ok) {
            const relatorio = await response.json();
            renderRelatorio(relatorio);
        }
    } catch (error) {
        console.error('Erro ao carregar relatórios:', error);
    }
}

// Renderizar relatório
function renderRelatorio(relatorio) {
    const relatorioDesempenho = document.getElementById('relatorio-desempenho');
    
    if (relatorio.length === 0) {
        relatorioDesempenho.innerHTML = '<p class="text-muted">Nenhum dado disponível para relatório.</p>';
        return;
    }
    
    let html = `
        <h4>Relatório de Desempenho da Equipe</h4>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Posição</th>
                        <th>Atendente</th>
                        <th>Cargo</th>
                        <th>Pontuação</th>
                        <th>Total de Avaliações</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
    `;
    
    relatorio.forEach((item, index) => {
        const statusClass = getStatusClassByText(item.status);
        html += `
            <tr>
                <td><strong>#${index + 1}</strong></td>
                <td>${item.atendente.nome}</td>
                <td>${item.atendente.cargo}</td>
                <td><span class="badge bg-primary">${item.atendente.pontuacao_atual} pts</span></td>
                <td>${item.total_avaliacoes}</td>
                <td><span class="${statusClass}">${item.status}</span></td>
            </tr>
        `;
    });
    
    html += '</tbody></table></div>';
    relatorioDesempenho.innerHTML = html;
}

// Mostrar modal de novo atendente
function showAddAtendenteModal() {
    const modal = new bootstrap.Modal(document.getElementById('addAtendenteModal'));
    modal.show();
}

// Adicionar atendente
async function addAtendente() {
    const nome = document.getElementById('nome').value;
    const email = document.getElementById('email').value;
    const cargo = document.getElementById('cargo').value;
    
    if (!nome || !email) {
        alert('Nome e email são obrigatórios!');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/atendentes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, email, cargo })
        });
        
        if (response.ok) {
            const novoAtendente = await response.json();
            atendentes.push(novoAtendente);
            
            // Fechar modal e limpar formulário
            const modal = bootstrap.Modal.getInstance(document.getElementById('addAtendenteModal'));
            modal.hide();
            document.getElementById('addAtendenteForm').reset();
            
            // Atualizar interface
            updateDashboard();
            renderAtendentes();
            
            alert('Atendente cadastrado com sucesso!');
        } else {
            const error = await response.json();
            alert('Erro ao cadastrar atendente: ' + error.error);
        }
    } catch (error) {
        console.error('Erro ao adicionar atendente:', error);
        alert('Erro ao cadastrar atendente!');
    }
}

// Mostrar modal de nova avaliação
async function showAddAvaliacaoModal() {
    // Carregar atendentes no select
    const atendenteSelect = document.getElementById('atendente_select');
    atendenteSelect.innerHTML = '<option value="">Selecione um atendente</option>';
    atendentes.forEach(atendente => {
        atendenteSelect.innerHTML += `<option value="${atendente.id}">${atendente.nome}</option>`;
    });
    
    // Carregar critérios no select
    const criterioSelect = document.getElementById('criterio_select');
    criterioSelect.innerHTML = '<option value="">Selecione um critério</option>';
    
    // Critérios padrão se não houver no banco
    const criteriosPadrao = [
        { nome: 'Resolução no Primeiro Contato', pontuacao_padrao: 5 },
        { nome: 'Satisfação do Cliente', pontuacao_padrao: 3 },
        { nome: 'Tempo Médio de Atendimento Otimizado', pontuacao_padrao: 2 },
        { nome: 'Proatividade na Solução', pontuacao_padrao: 4 },
        { nome: 'Empatia e Cortesia', pontuacao_padrao: 3 },
        { nome: 'Conhecimento do Produto/Serviço', pontuacao_padrao: 3 },
        { nome: 'Reabertura de Chamado', pontuacao_padrao: -5 },
        { nome: 'Insatisfação do Cliente', pontuacao_padrao: -4 },
        { nome: 'Tempo Médio de Espera Excessivo', pontuacao_padrao: -3 },
        { nome: 'Falta de Resolução', pontuacao_padrao: -7 },
        { nome: 'Falta de Cortesia/Empatia', pontuacao_padrao: -6 },
        { nome: 'Informação Incorreta/Incompleta', pontuacao_padrao: -5 }
    ];
    
    const criteriosParaUsar = criterios.length > 0 ? criterios : criteriosPadrao;
    
    criteriosParaUsar.forEach(criterio => {
        criterioSelect.innerHTML += `<option value="${criterio.nome}" data-pontuacao="${criterio.pontuacao_padrao}">${criterio.nome} (${criterio.pontuacao_padrao > 0 ? '+' : ''}${criterio.pontuacao_padrao} pts)</option>`;
    });
    
    // Atualizar pontuação quando critério for selecionado
    criterioSelect.addEventListener('change', function() {
        const selectedOption = this.options[this.selectedIndex];
        const pontuacao = selectedOption.getAttribute('data-pontuacao');
        if (pontuacao) {
            document.getElementById('pontuacao').value = pontuacao;
        }
    });
    
    const modal = new bootstrap.Modal(document.getElementById('addAvaliacaoModal'));
    modal.show();
}

// Adicionar avaliação
async function addAvaliacao() {
    const atendenteId = document.getElementById('atendente_select').value;
    const criterio = document.getElementById('criterio_select').value;
    const pontuacao = parseInt(document.getElementById('pontuacao').value);
    const observacoes = document.getElementById('observacoes').value;
    const avaliador = document.getElementById('avaliador').value;
    
    if (!atendenteId || !criterio || !avaliador) {
        alert('Atendente, critério e avaliador são obrigatórios!');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/avaliacoes`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                atendente_id: parseInt(atendenteId),
                criterio,
                pontuacao,
                observacoes,
                avaliador
            })
        });
        
        if (response.ok) {
            const novaAvaliacao = await response.json();
            avaliacoes.unshift(novaAvaliacao);
            
            // Atualizar pontuação do atendente
            const atendente = atendentes.find(a => a.id === parseInt(atendenteId));
            if (atendente) {
                atendente.pontuacao_atual += pontuacao;
            }
            
            // Fechar modal e limpar formulário
            const modal = bootstrap.Modal.getInstance(document.getElementById('addAvaliacaoModal'));
            modal.hide();
            document.getElementById('addAvaliacaoForm').reset();
            
            // Atualizar interface
            updateDashboard();
            renderAvaliacoes();
            
            alert('Avaliação registrada com sucesso!');
        } else {
            const error = await response.json();
            alert('Erro ao registrar avaliação: ' + error.error);
        }
    } catch (error) {
        console.error('Erro ao adicionar avaliação:', error);
        alert('Erro ao registrar avaliação!');
    }
}

// Funções auxiliares
function getStatusClass(pontuacao) {
    if (pontuacao > 120) {
        return { class: 'status-excelente', text: 'Excelente' };
    } else if (pontuacao > 100) {
        return { class: 'status-bom', text: 'Bom' };
    } else if (pontuacao > 80) {
        return { class: 'status-regular', text: 'Regular' };
    } else {
        return { class: 'status-necessita-melhoria', text: 'Necessita Melhoria' };
    }
}

function getStatusClassByText(status) {
    switch(status) {
        case 'Excelente': return 'status-excelente';
        case 'Bom': return 'status-bom';
        case 'Regular': return 'status-regular';
        case 'Necessita Melhoria': return 'status-necessita-melhoria';
        default: return '';
    }
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR') + ' ' + date.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
}

function viewAtendenteDetails(atendenteId) {
    // Implementar visualização de detalhes do atendente
    alert(`Visualizar detalhes do atendente ID: ${atendenteId}`);
}

