"""
Arquivo de configuração e utilitários para o Dashboard de Tickets
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Configurações da aplicação
APP_CONFIG = {
    'title': 'Dashboard de Tickets de Suporte',
    'version': '1.0.0',
    'author': 'Sistema de Gestão de Tickets',
    'description': 'Sistema para acompanhamento e gestão de tickets de suporte'
}

# Configurações de cores para os gráficos
CORES = {
    'iniciados': '#1f77b4',
    'finalizados': '#2ca02c',
    'andamento': '#ff7f0e',
    'background': '#f0f2f6'
}

# Configurações dos gráficos
GRAFICOS_CONFIG = {
    'height': 400,
    'margin': dict(l=50, r=50, t=50, b=50),
    'font_size': 12
}

def aplicar_estilo_customizado():
    """
    Aplica estilos CSS customizados à aplicação.
    """
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .success-message {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .warning-message {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #e7f3ff;
        border-left: 4px solid #1f77b4;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0d5aa7, #1e7e34);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

def criar_grafico_linha_temporal(df, titulo="Evolução dos Tickets"):
    """
    Cria um gráfico de linha temporal para os tickets.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        titulo (str): Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure: Gráfico configurado
    """
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Adicionar linhas para cada tipo de ticket
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['tickets_iniciados'],
        mode='lines+markers',
        name='Tickets Iniciados',
        line=dict(color=CORES['iniciados'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['tickets_finalizados'],
        mode='lines+markers',
        name='Tickets Finalizados',
        line=dict(color=CORES['finalizados'], width=3),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df['tickets_andamento'],
        mode='lines+markers',
        name='Tickets em Andamento',
        line=dict(color=CORES['andamento'], width=3),
        marker=dict(size=8)
    ))
    
    # Configurar layout
    fig.update_layout(
        title=titulo,
        xaxis_title="Data",
        yaxis_title="Número de Tickets",
        height=GRAFICOS_CONFIG['height'],
        margin=GRAFICOS_CONFIG['margin'],
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def criar_grafico_barras_comparativo(df, titulo="Comparativo de Tickets"):
    """
    Cria um gráfico de barras comparativo.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        titulo (str): Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure: Gráfico configurado
    """
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df['data'],
        y=df['tickets_iniciados'],
        name='Iniciados',
        marker_color=CORES['iniciados']
    ))
    
    fig.add_trace(go.Bar(
        x=df['data'],
        y=df['tickets_finalizados'],
        name='Finalizados',
        marker_color=CORES['finalizados']
    ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title="Data",
        yaxis_title="Número de Tickets",
        barmode='group',
        height=GRAFICOS_CONFIG['height'],
        margin=GRAFICOS_CONFIG['margin']
    )
    
    return fig

def criar_grafico_pizza(valores, labels, titulo="Distribuição de Tickets"):
    """
    Cria um gráfico de pizza.
    
    Args:
        valores (list): Lista com os valores
        labels (list): Lista com os rótulos
        titulo (str): Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure: Gráfico configurado
    """
    cores = [CORES['iniciados'], CORES['finalizados'], CORES['andamento']]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=valores,
        marker_colors=cores,
        textinfo='label+percent',
        textfont_size=12
    )])
    
    fig.update_layout(
        title=titulo,
        height=GRAFICOS_CONFIG['height'],
        margin=GRAFICOS_CONFIG['margin']
    )
    
    return fig

def criar_grafico_area(df, coluna, titulo="Gráfico de Área"):
    """
    Cria um gráfico de área.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        coluna (str): Nome da coluna para o gráfico
        titulo (str): Título do gráfico
        
    Returns:
        plotly.graph_objects.Figure: Gráfico configurado
    """
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['data'],
        y=df[coluna],
        fill='tonexty',
        mode='lines',
        name=coluna.replace('_', ' ').title(),
        line=dict(color=CORES['andamento'])
    ))
    
    fig.update_layout(
        title=titulo,
        xaxis_title="Data",
        yaxis_title="Número de Tickets",
        height=GRAFICOS_CONFIG['height'],
        margin=GRAFICOS_CONFIG['margin']
    )
    
    return fig

def formatar_numero(numero):
    """
    Formata números para exibição.
    
    Args:
        numero (float): Número para formatar
        
    Returns:
        str: Número formatado
    """
    if numero >= 1000000:
        return f"{numero/1000000:.1f}M"
    elif numero >= 1000:
        return f"{numero/1000:.1f}K"
    else:
        return f"{numero:.0f}"

def calcular_kpis(df):
    """
    Calcula KPIs importantes dos dados.
    
    Args:
        df (pd.DataFrame): DataFrame with the data
        
    Returns:
        dict: Dicionário com KPIs calculados
    """
    if df.empty:
        return {
            'taxa_resolucao': 0,
            'tempo_medio_resolucao': 0,
            'tendencia_iniciados': 0,
            'tendencia_finalizados': 0,
            'eficiencia': 0
        }
    
    # Taxa de resolução (finalizados / iniciados)
    total_iniciados = df['tickets_iniciados'].sum()
    total_finalizados = df['tickets_finalizados'].sum()
    taxa_resolucao = (total_finalizados / total_iniciados * 100) if total_iniciados > 0 else 0
    
    # Tendências (comparar últimos 7 dias com 7 dias anteriores)
    if len(df) >= 14:
        ultimos_7 = df.tail(7)
        anteriores_7 = df.iloc[-14:-7]
        
        tendencia_iniciados = (
            (ultimos_7['tickets_iniciados'].mean() - anteriores_7['tickets_iniciados'].mean()) 
            / anteriores_7['tickets_iniciados'].mean() * 100
        ) if anteriores_7['tickets_iniciados'].mean() > 0 else 0
        
        tendencia_finalizados = (
            (ultimos_7['tickets_finalizados'].mean() - anteriores_7['tickets_finalizados'].mean()) 
            / anteriores_7['tickets_finalizados'].mean() * 100
        ) if anteriores_7['tickets_finalizados'].mean() > 0 else 0
    else:
        tendencia_iniciados = 0
        tendencia_finalizados = 0
    
    # Eficiência (finalizados / (iniciados + andamento))
    total_andamento = df['tickets_andamento'].sum()
    eficiencia = (
        total_finalizados / (total_iniciados + total_andamento) * 100
    ) if (total_iniciados + total_andamento) > 0 else 0
    
    return {
        'taxa_resolucao': taxa_resolucao,
        'tendencia_iniciados': tendencia_iniciados,
        'tendencia_finalizados': tendencia_finalizados,
        'eficiencia': eficiencia
    }

def exibir_metricas_principais(df):
    """
    Exibe as métricas principais em cards organizados.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
    """
    if df.empty:
        st.warning("⚠️ Nenhum dado disponível para calcular métricas.")
        return
    
    kpis = calcular_kpis(df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_iniciados = df['tickets_iniciados'].sum()
        st.metric(
            "📥 Total Iniciados",
            formatar_numero(total_iniciados),
            delta=f"{kpis['tendencia_iniciados']:+.1f}%" if kpis['tendencia_iniciados'] != 0 else None
        )
    
    with col2:
        total_finalizados = df['tickets_finalizados'].sum()
        st.metric(
            "✅ Total Finalizados",
            formatar_numero(total_finalizados),
            delta=f"{kpis['tendencia_finalizados']:+.1f}%" if kpis['tendencia_finalizados'] != 0 else None
        )
    
    with col3:
        st.metric(
            "📊 Taxa de Resolução",
            f"{kpis['taxa_resolucao']:.1f}%"
        )
    
    with col4:
        media_andamento = df['tickets_andamento'].mean()
        st.metric(
            "⏳ Média em Andamento",
            f"{media_andamento:.1f}"
        )

def validar_dados_entrada(tickets_iniciados, tickets_finalizados, tickets_andamento):
    """
    Valida os dados de entrada do formulário.
    
    Args:
        tickets_iniciados (int): Número de tickets iniciados
        tickets_finalizados (int): Número de tickets finalizados
        tickets_andamento (int): Número de tickets em andamento
        
    Returns:
        tuple: (bool, str) - (é_valido, mensagem_erro)
    """
    if tickets_iniciados < 0 or tickets_finalizados < 0 or tickets_andamento < 0:
        return False, "❌ Os valores não podem ser negativos."
    
    if tickets_iniciados == 0 and tickets_finalizados == 0 and tickets_andamento == 0:
        return False, "⚠️ Pelo menos um valor deve ser maior que zero."
    
    return True, ""

def gerar_relatorio_periodo(df, data_inicio, data_fim):
    """
    Gera um relatório para um período específico.
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        data_inicio (date): Data de início
        data_fim (date): Data de fim
        
    Returns:
        dict: Relatório com estatísticas do período
    """
    df_periodo = df[
        (df['data'].dt.date >= data_inicio) & 
        (df['data'].dt.date <= data_fim)
    ]
    
    if df_periodo.empty:
        return None
    
    return {
        'periodo': f"{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}",
        'total_dias': len(df_periodo),
        'total_iniciados': df_periodo['tickets_iniciados'].sum(),
        'total_finalizados': df_periodo['tickets_finalizados'].sum(),
        'media_andamento': df_periodo['tickets_andamento'].mean(),
        'dia_maior_atividade': df_periodo.loc[
            (df_periodo['tickets_iniciados'] + df_periodo['tickets_finalizados']).idxmax(),
            'data'
        ].strftime('%d/%m/%Y'),
        'pico_tickets_iniciados': df_periodo['tickets_iniciados'].max(),
        'pico_tickets_finalizados': df_periodo['tickets_finalizados'].max()
    }
