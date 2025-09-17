import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import os
from data_manager import DataManager

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Tickets de Suporte",
    page_icon="🎫",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar o gerenciador de dados
def init_data_manager():
    return DataManager()

# Criar instância sem cache para evitar problemas de persistência
data_manager = init_data_manager()

# Título principal
st.title("🎫 Dashboard de Tickets de Suporte")
st.markdown("---")

# Sidebar para navegação
st.sidebar.title("Menu de Navegação")
page = st.sidebar.selectbox(
    "Escolha uma opção:",
    ["🏠 Dashboard Hoje", "📊 Dashboard Geral", "📈 Relatórios", "🔍 Filtros Avançados"]
)

if page == "🏠 Dashboard Hoje":
    # Data de hoje
    hoje = date.today()
    st.header(f"📅 Dashboard de Hoje - {hoje.strftime('%d/%m/%Y')}")
    
    # Carregar dados
    df = data_manager.carregar_dados()
    
    # Verificar se já existe registro para hoje
    dados_hoje = None
    if not df.empty:
        dados_hoje_mask = df['data'].dt.date == hoje
        if dados_hoje_mask.any():
            dados_hoje = df[dados_hoje_mask].iloc[0]
    
    # Status do dia
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if dados_hoje is not None:
            st.success(f"✅ Dados já registrados para hoje ({hoje.strftime('%d/%m/%Y')})")
            
            # Mostrar dados atuais do dia
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("🎫 Iniciados Hoje", int(dados_hoje['tickets_iniciados']))
            with col_b:
                st.metric("✅ Finalizados Hoje", int(dados_hoje['tickets_finalizados']))
            with col_c:
                st.metric("⏳ Em Andamento", int(dados_hoje['tickets_andamento']))
            
            # Mostrar links dos chamados se existirem
            if 'links_chamados' in dados_hoje and dados_hoje['links_chamados'] and str(dados_hoje['links_chamados']).strip():
                st.subheader("🔗 Links dos Chamados de Hoje:")
                links_texto = str(dados_hoje['links_chamados'])
                # Detectar se são links separados por linha ou vírgula
                if '\n' in links_texto:
                    links = [link.strip() for link in links_texto.split('\n') if link.strip()]
                else:
                    links = [link.strip() for link in links_texto.split(',') if link.strip()]
                
                for i, link in enumerate(links, 1):
                    if link.startswith('http'):
                        st.markdown(f"**{i}.** [Chamado {i}]({link})")
                    else:
                        st.markdown(f"**{i}.** {link}")
        else:
            st.warning(f"⚠️ Ainda não há dados registrados para hoje ({hoje.strftime('%d/%m/%Y')})")
            st.info("👇 Use o formulário abaixo para registrar os dados do dia")
    
    with col2:
        if dados_hoje is not None:
            st.info("💡 **Dica:** Você pode atualizar os dados do dia a qualquer momento usando o formulário abaixo.")
    
    st.markdown("---")
    
    # Formulário para lançar/atualizar dados de hoje
    st.subheader("📝 Lançar/Atualizar Dados de Hoje")
    
    # Pre-carregar valores se já existem dados para hoje
    valor_iniciados = int(dados_hoje['tickets_iniciados']) if dados_hoje is not None else 0
    valor_finalizados = int(dados_hoje['tickets_finalizados']) if dados_hoje is not None else 0
    valor_andamento = int(dados_hoje['tickets_andamento']) if dados_hoje is not None else 0
    valor_links = str(dados_hoje['links_chamados']) if dados_hoje is not None and 'links_chamados' in dados_hoje else ""
    
    with st.form("dados_hoje"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tickets_iniciados = st.number_input(
                "🎫 Tickets Iniciados Hoje:",
                min_value=0,
                value=valor_iniciados,
                help="Número de tickets que foram iniciados hoje"
            )
        
        with col2:
            tickets_finalizados = st.number_input(
                "✅ Tickets Finalizados Hoje:",
                min_value=0,
                value=valor_finalizados,
                help="Número de tickets que foram finalizados hoje"
            )
        
        with col3:
            tickets_andamento = st.number_input(
                "⏳ Tickets em Andamento:",
                min_value=0,
                value=valor_andamento,
                help="Número total de tickets em andamento hoje"
            )
        
        # Campo para links dos chamados
        links_chamados = st.text_area(
            "🔗 Links dos Chamados Abertos:",
            value=valor_links,
            height=100,
            help="Cole aqui os links dos chamados abertos hoje (um por linha ou separados por vírgula)",
            placeholder="Exemplo:\nhttps://link1.com\nhttps://link2.com\nou\nlink1, link2, link3"
        )
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submitted = st.form_submit_button("💾 Salvar/Atualizar Dados", width='stretch')
        with col_btn2:
            if dados_hoje is not None:
                excluir = st.form_submit_button("🗑️ Excluir Dados de Hoje", width='stretch')
        
        if submitted:
            sucesso = data_manager.adicionar_registro(
                hoje, tickets_iniciados, tickets_finalizados, tickets_andamento, links_chamados
            )
            
            if sucesso:
                if dados_hoje is not None:
                    st.success(f"✅ Dados atualizados com sucesso para hoje ({hoje.strftime('%d/%m/%Y')})!")
                else:
                    st.success(f"✅ Dados registrados com sucesso para hoje ({hoje.strftime('%d/%m/%Y')})!")
                st.balloons()
                st.rerun()  # Recarregar página para mostrar dados atualizados
            else:
                st.error("❌ Erro ao salvar os dados. Tente novamente.")
        
        if dados_hoje is not None and 'excluir' in locals() and excluir:
            if data_manager.excluir_registro(hoje):
                st.success("🗑️ Dados de hoje excluídos com sucesso!")
                st.rerun()
            else:
                st.error("❌ Erro ao excluir dados.")
    
    # Mostrar histórico dos últimos 7 dias
    if not df.empty:
        st.markdown("---")
        st.subheader("📊 Últimos 7 Dias")
        
        # Pegar últimos 7 dias
        ultimos_7_dias = df.tail(7)
        
        # Gráfico dos últimos 7 dias
        fig_linha = px.line(
            ultimos_7_dias,
            x='data',
            y=['tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'],
            title="Evolução dos Últimos 7 Dias",
            labels={'value': 'Número de Tickets', 'variable': 'Tipo de Ticket'}
        )
        fig_linha.update_layout(height=300)
        st.plotly_chart(fig_linha, width='stretch')
        
        # Tabela dos últimos 7 dias
        df_display = ultimos_7_dias.copy()
        df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
        
        # Truncar links para exibição na tabela
        if 'links_chamados' in df_display.columns:
            df_display['links_resumo'] = df_display['links_chamados'].apply(
                lambda x: (str(x)[:50] + "...") if x and len(str(x)) > 50 else str(x) if x else ""
            )
        
        df_display = df_display.rename(columns={
            'data': 'Data',
            'tickets_iniciados': 'Iniciados',
            'tickets_finalizados': 'Finalizados',
            'tickets_andamento': 'Em Andamento',
            'links_resumo': 'Links (resumo)'
        })
        
        # Selecionar apenas as colunas que queremos mostrar
        colunas_exibir = ['Data', 'Iniciados', 'Finalizados', 'Em Andamento']
        if 'Links (resumo)' in df_display.columns:
            colunas_exibir.append('Links (resumo)')
        
        st.dataframe(df_display[colunas_exibir], width='stretch', hide_index=True)

elif page == "📊 Dashboard Geral":
    st.header("Dashboard Interativo")
    
    # Carregar dados
    df = data_manager.carregar_dados()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado. Registre alguns dados primeiro!")
    else:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_iniciados = df['tickets_iniciados'].sum()
            st.metric("Total de Tickets Iniciados", total_iniciados)
        
        with col2:
            total_finalizados = df['tickets_finalizados'].sum()
            st.metric("Total de Tickets Finalizados", total_finalizados)
        
        with col3:
            media_andamento = df['tickets_andamento'].mean()
            st.metric("Média de Tickets em Andamento", f"{media_andamento:.1f}")
        
        with col4:
            total_registros = len(df)
            st.metric("Total de Registros", total_registros)
        
        st.markdown("---")
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de linha temporal
            fig_linha = px.line(
                df, 
                x='data', 
                y=['tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'],
                title="Evolução dos Tickets ao Longo do Tempo",
                labels={'value': 'Número de Tickets', 'variable': 'Tipo de Ticket'}
            )
            fig_linha.update_layout(height=400)
            st.plotly_chart(fig_linha, use_container_width=True)
        
        with col2:
            # Gráfico de barras dos últimos 7 dias
            ultimos_7_dias = df.tail(7)
            fig_bar = px.bar(
                ultimos_7_dias,
                x='data',
                y=['tickets_iniciados', 'tickets_finalizados'],
                title="Tickets Iniciados vs Finalizados (Últimos 7 dias)",
                barmode='group'
            )
            fig_bar.update_layout(height=400)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Gráfico de pizza para distribuição total
        col1, col2 = st.columns(2)
        
        with col1:
            # Pizza dos totais
            totais = [
                df['tickets_iniciados'].sum(),
                df['tickets_finalizados'].sum(),
                df['tickets_andamento'].sum()
            ]
            labels = ['Iniciados', 'Finalizados', 'Em Andamento']
            
            fig_pizza = px.pie(
                values=totais,
                names=labels,
                title="Distribuição Total de Tickets"
            )
            st.plotly_chart(fig_pizza, use_container_width=True)
        
        with col2:
            # Gráfico de área
            fig_area = px.area(
                df,
                x='data',
                y='tickets_andamento',
                title="Tickets em Andamento ao Longo do Tempo",
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig_area, use_container_width=True)

elif page == "📈 Relatórios":
    st.header("Relatórios Detalhados")
    
    df = data_manager.carregar_dados()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado.")
    else:
        # Estatísticas resumidas
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Estatísticas Resumidas")
            stats = df[['tickets_iniciados', 'tickets_finalizados', 'tickets_andamento']].describe()
            st.dataframe(stats, use_container_width=True)
        
        with col2:
            st.subheader("📅 Informações do Período")
            st.write(f"**Período:** {df['data'].min().strftime('%d/%m/%Y')} a {df['data'].max().strftime('%d/%m/%Y')}")
            st.write(f"**Total de dias registrados:** {len(df)}")
            st.write(f"**Média diária de tickets iniciados:** {df['tickets_iniciados'].mean():.1f}")
            st.write(f"**Média diária de tickets finalizados:** {df['tickets_finalizados'].mean():.1f}")
            st.write(f"**Média diária de tickets em andamento:** {df['tickets_andamento'].mean():.1f}")
        
        st.markdown("---")
        
        # Tabela de dados
        st.subheader("📋 Dados Completos")
        
        # Adicionar formatação à tabela
        df_display = df.copy()
        df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
        df_display = df_display.rename(columns={
            'data': 'Data',
            'tickets_iniciados': 'Iniciados',
            'tickets_finalizados': 'Finalizados',
            'tickets_andamento': 'Em Andamento'
        })
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Botão para download
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Baixar dados em CSV",
            data=csv,
            file_name=f"tickets_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

elif page == "🔍 Filtros Avançados":
    st.header("Filtros Avançados")
    
    df = data_manager.carregar_dados()
    
    if df.empty:
        st.warning("⚠️ Nenhum dado encontrado.")
    else:
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            data_inicio = st.date_input(
                "Data de Início:",
                value=df['data'].min().date(),
                min_value=df['data'].min().date(),
                max_value=df['data'].max().date()
            )
        
        with col2:
            data_fim = st.date_input(
                "Data de Fim:",
                value=df['data'].max().date(),
                min_value=df['data'].min().date(),
                max_value=df['data'].max().date()
            )
        
        with col3:
            tipo_filtro = st.selectbox(
                "Filtrar por:",
                ["Todos", "Apenas dias com tickets iniciados", "Apenas dias com tickets finalizados", "Apenas dias com tickets em andamento"]
            )
        
        # Aplicar filtros
        df_filtrado = df[(df['data'].dt.date >= data_inicio) & (df['data'].dt.date <= data_fim)]
        
        if tipo_filtro == "Apenas dias com tickets iniciados":
            df_filtrado = df_filtrado[df_filtrado['tickets_iniciados'] > 0]
        elif tipo_filtro == "Apenas dias com tickets finalizados":
            df_filtrado = df_filtrado[df_filtrado['tickets_finalizados'] > 0]
        elif tipo_filtro == "Apenas dias com tickets em andamento":
            df_filtrado = df_filtrado[df_filtrado['tickets_andamento'] > 0]
        
        if df_filtrado.empty:
            st.warning("⚠️ Nenhum dado encontrado para os filtros aplicados.")
        else:
            st.success(f"✅ Encontrados {len(df_filtrado)} registros para o período selecionado.")
            
            # Gráfico dos dados filtrados
            fig = px.line(
                df_filtrado,
                x='data',
                y=['tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'],
                title=f"Dados Filtrados - {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Tabela dos dados filtrados
            df_display = df_filtrado.copy()
            df_display['data'] = df_display['data'].dt.strftime('%d/%m/%Y')
            df_display = df_display.rename(columns={
                'data': 'Data',
                'tickets_iniciados': 'Iniciados',
                'tickets_finalizados': 'Finalizados',
                'tickets_andamento': 'Em Andamento'
            })
            
            st.dataframe(df_display, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.markdown("Desenvolvido para gerenciamento de tickets de suporte | 2025")
