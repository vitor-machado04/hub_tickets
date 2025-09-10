# 🎫 Dashboard de Tickets de Suporte

Sistema completo para gerenciamento e acompanhamento de tickets de suporte com interface web interativa desenvolvida em Streamlit.

## 📋 Funcionalidades

### ✨ Principais Recursos
- **Registro Diário**: Registre facilmente tickets iniciados, finalizados e em andamento
- **Armazenamento Automático**: Dados salvos automaticamente em planilha Excel
- **Dashboard Interativo**: Visualize dados em tempo real com gráficos dinâmicos
- **Relatórios Detalhados**: Gere relatórios completos com estatísticas
- **Filtros Avançados**: Filtre dados por período e tipos específicos
- **Exportação**: Exporte dados em formato CSV

### 📊 Tipos de Visualizações
- Gráficos de linha temporal
- Gráficos de barras comparativos
- Gráficos de pizza para distribuição
- Gráficos de área
- Métricas e KPIs em tempo real

## 🚀 Como Usar

### Pré-requisitos
- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
   ```bash
   git clone <repositorio>
   cd hub_tickets
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

4. **Acesse no navegador**
   - A aplicação abrirá automaticamente no navegador
   - URL padrão: `http://localhost:8501`

## 📖 Manual de Uso

### 1. 📊 Dashboard Principal
- Visualize métricas gerais dos tickets
- Acompanhe gráficos em tempo real
- Veja estatísticas resumidas

### 2. ➕ Registrar Dados
- Selecione a data do registro
- Informe o número de tickets:
  - **Iniciados**: Novos tickets abertos no dia
  - **Finalizados**: Tickets resolvidos no dia
  - **Em Andamento**: Tickets ativos no dia
- Clique em "Salvar Dados"

### 3. 📈 Relatórios
- Visualize estatísticas detalhadas
- Consulte dados históricos completos
- Baixe relatórios em CSV

### 4. 🔍 Filtros Avançados
- Filtre por período específico
- Filtre por tipo de ticket
- Visualize dados customizados

## 🗂️ Estrutura de Arquivos

```
hub_tickets/
├── app.py              # Aplicação principal Streamlit
├── data_manager.py     # Gerenciador de dados e Excel
├── utils.py            # Utilitários e configurações
├── requirements.txt    # Dependências do projeto
├── README.md          # Este arquivo
└── dados_tickets.xlsx # Arquivo Excel (criado automaticamente)
```

## 📁 Armazenamento de Dados

Os dados são armazenados automaticamente em um arquivo Excel (`dados_tickets.xlsx`) com a seguinte estrutura:

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| data | Date | Data do registro |
| tickets_iniciados | Integer | Número de tickets iniciados |
| tickets_finalizados | Integer | Número de tickets finalizados |
| tickets_andamento | Integer | Número de tickets em andamento |

## 🎨 Personalização

### Modificar Cores dos Gráficos
Edite o arquivo `utils.py` na seção `CORES`:
```python
CORES = {
    'iniciados': '#1f77b4',    # Azul
    'finalizados': '#2ca02c',  # Verde
    'andamento': '#ff7f0e',    # Laranja
    'background': '#f0f2f6'    # Fundo
}
```

### Configurar Nome do Arquivo Excel
No arquivo `data_manager.py`, modifique:
```python
def __init__(self, arquivo_excel="dados_tickets.xlsx"):
```

## 🔧 Recursos Técnicos

### Tecnologias Utilizadas
- **Streamlit**: Framework web para Python
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Gráficos interativos
- **OpenPyXL**: Leitura/escrita de arquivos Excel
- **XlsxWriter**: Criação avançada de planilhas Excel

### Funcionalidades Avançadas
- Cache automático de dados
- Validação de entrada
- Backup automático
- Tratamento de erros
- Interface responsiva

## 📊 KPIs Calculados

O sistema calcula automaticamente:
- **Taxa de Resolução**: Percentual de tickets finalizados
- **Tendências**: Comparação entre períodos
- **Eficiência**: Relação entre tickets processados
- **Médias**: Valores médios por período

## 🐛 Solução de Problemas

### Erro ao Salvar Dados
- Verifique se o arquivo Excel não está aberto em outro programa
- Confirme as permissões de escrita na pasta

### Gráficos Não Aparecem
- Verifique se o Plotly está instalado corretamente
- Reinicie a aplicação

### Dados Não Carregam
- Verifique se o arquivo `dados_tickets.xlsx` existe
- Confirme se os dados estão no formato correto

## 🔄 Atualizações Futuras

Recursos planejados:
- Integração com Google Sheets
- Notificações por email
- Relatórios automatizados
- API REST para integração
- Dashboard mobile

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este README
2. Consulte os comentários no código
3. Teste com dados de exemplo

---

**Desenvolvido para otimizar o gerenciamento de tickets de suporte | 2025**
