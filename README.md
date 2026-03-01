# Sistema de Bonificação e Avaliação de Desempenho

Um sistema web completo para gerenciar avaliações de desempenho, bonificações e desqualificações de equipes de atendimento ao cliente.

## Características

✅ **Dashboard em Tempo Real**
- Estatísticas gerais da equipe
- Ranking de desempenho
- Avaliações recentes

✅ **Gestão de Atendentes**
- Cadastro e gerenciamento de atendentes
- Acompanhamento de pontuação individual
- Status de desempenho automático

✅ **Sistema de Avaliações**
- 6 critérios positivos para bonificação
- 6 critérios negativos para desqualificação
- Pontuação automática
- Histórico completo

✅ **Relatórios**
- Relatório de desempenho da equipe
- Ranking por pontuação
- Análise de status individual

## Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite
- **Estilo**: Bootstrap 5
- **Ícones**: Font Awesome

## Instalação Local

### Pré-requisitos
- Python 3.11+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone ou extraia o projeto**
   ```bash
   cd sistema_bonificacao
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python -m src.main
   ```

5. **Acesse no navegador**
   ```
   http://localhost:5000
   ```

## Implantação no Render

### Pré-requisitos
- Conta no GitHub
- Conta no Render (gratuita)

### Passos

1. **Faça upload do código para o GitHub**
   - Crie um novo repositório no GitHub
   - Faça push do código

2. **Conecte ao Render**
   - Acesse https://render.com
   - Clique em "New +" > "Web Service"
   - Selecione seu repositório do GitHub
   - Configure:
     - **Name**: sistema-bonificacao
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn -w 1 -b 0.0.0.0:$PORT src.main:app`
   - Clique em "Create Web Service"

3. **Aguarde a implantação**
   - O Render construirá e implantará automaticamente
   - Você receberá uma URL pública para acessar o sistema

## Critérios de Avaliação

### Positivos (Bonificação)
- Resolução no Primeiro Contato: +5 pts
- Satisfação do Cliente: +3 pts
- Tempo Médio de Atendimento Otimizado: +2 pts
- Proatividade na Solução: +4 pts
- Empatia e Cortesia: +3 pts
- Conhecimento do Produto/Serviço: +3 pts

### Negativos (Desqualificação)
- Reabertura de Chamado: -5 pts
- Insatisfação do Cliente: -4 pts
- Tempo Médio de Espera Excessivo: -3 pts
- Falta de Resolução: -7 pts
- Falta de Cortesia/Empatia: -6 pts
- Informação Incorreta/Incompleta: -5 pts

## Sistema de Pontuação

- **Base**: 100 pontos por período
- **Excelente**: > 120 pontos
- **Bom**: 101-120 pontos
- **Regular**: 81-100 pontos
- **Necessita Melhoria**: ≤ 80 pontos

## Estrutura do Projeto

```
sistema_bonificacao/
├── src/
│   ├── models/           # Modelos de dados
│   ├── routes/           # Rotas da API
│   ├── static/           # Arquivos estáticos (HTML, CSS, JS)
│   ├── database/         # Banco de dados SQLite
│   └── main.py           # Ponto de entrada
├── requirements.txt      # Dependências Python
├── render.yaml           # Configuração do Render
├── .gitignore            # Arquivos ignorados pelo Git
└── README.md             # Este arquivo
```

## Uso

### Cadastrando um Atendente
1. Acesse "Atendentes"
2. Clique em "Novo Atendente"
3. Preencha nome, email e cargo
4. Clique em "Salvar"

### Registrando uma Avaliação
1. Acesse "Avaliações"
2. Clique em "Nova Avaliação"
3. Selecione o atendente e critério
4. Adicione observações
5. Clique em "Salvar"

### Consultando Relatórios
1. Acesse "Relatórios"
2. Visualize o desempenho da equipe
3. Analise o ranking e status

## Suporte e Documentação

Para mais informações, consulte:
- `manual_usuario.md` - Manual completo do usuário
- `documentacao_tecnica.md` - Documentação técnica para desenvolvedores

## Licença

Este projeto é fornecido como está para uso interno.

## Autor

Desenvolvido por **Manus AI** - 2026
