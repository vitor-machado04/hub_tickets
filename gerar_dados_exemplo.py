"""
Script para gerar dados de exemplo para demonstração do Dashboard de Tickets
Execute este script para popular a aplicação com dados de teste.
"""

from data_manager import DataManager
from datetime import datetime, timedelta
import random

def gerar_dados_exemplo():
    """
    Gera dados de exemplo para demonstração da aplicação.
    """
    print("🎫 Gerando dados de exemplo para o Dashboard de Tickets...")
    
    # Inicializar o gerenciador de dados
    dm = DataManager("dados_tickets.xlsx")
    
    # Data inicial (30 dias atrás)
    data_inicio = datetime.now() - timedelta(days=30)
    
    # Gerar dados para os últimos 30 dias
    for i in range(30):
        data_atual = data_inicio + timedelta(days=i)
        
        # Simular variação semanal (menos tickets nos fins de semana)
        if data_atual.weekday() >= 5:  # Sábado e Domingo
            multiplicador = 0.3
        else:
            multiplicador = 1.0
        
        # Gerar números aleatórios com tendência realista
        base_iniciados = random.randint(5, 25)
        base_finalizados = random.randint(3, 20)
        base_andamento = random.randint(10, 40)
        
        tickets_iniciados = int(base_iniciados * multiplicador)
        tickets_finalizados = int(base_finalizados * multiplicador)
        tickets_andamento = int(base_andamento * multiplicador)
        
        # Adicionar registro
        sucesso = dm.adicionar_registro(
            data_atual.date(),
            tickets_iniciados,
            tickets_finalizados,
            tickets_andamento
        )
        
        if sucesso:
            print(f"✅ {data_atual.strftime('%d/%m/%Y')}: {tickets_iniciados} iniciados, {tickets_finalizados} finalizados, {tickets_andamento} em andamento")
        else:
            print(f"❌ Erro ao adicionar registro para {data_atual.strftime('%d/%m/%Y')}")
    
    print("\n🎉 Dados de exemplo gerados com sucesso!")
    print("📊 Execute 'streamlit run app.py' para visualizar o dashboard")

def gerar_dados_realistas():
    """
    Gera dados mais realistas seguindo padrões típicos de suporte.
    """
    print("📈 Gerando dados realistas para demonstração...")
    
    dm = DataManager("dados_tickets.xlsx")
    
    # Cenários para diferentes períodos
    cenarios = [
        {"periodo": "início_mes", "dias": 10, "atividade": "alta"},
        {"periodo": "meio_mes", "dias": 10, "atividade": "normal"},
        {"periodo": "fim_mes", "dias": 10, "atividade": "baixa"}
    ]
    
    data_atual = datetime.now() - timedelta(days=30)
    
    for cenario in cenarios:
        for dia in range(cenario["dias"]):
            if cenario["atividade"] == "alta":
                tickets_iniciados = random.randint(15, 30)
                tickets_finalizados = random.randint(10, 25)
                tickets_andamento = random.randint(25, 45)
            elif cenario["atividade"] == "normal":
                tickets_iniciados = random.randint(8, 18)
                tickets_finalizados = random.randint(8, 20)
                tickets_andamento = random.randint(15, 35)
            else:  # baixa
                tickets_iniciados = random.randint(3, 12)
                tickets_finalizados = random.randint(5, 15)
                tickets_andamento = random.randint(8, 25)
            
            # Ajustar para fins de semana
            if data_atual.weekday() >= 5:
                tickets_iniciados = int(tickets_iniciados * 0.4)
                tickets_finalizados = int(tickets_finalizados * 0.6)
                tickets_andamento = int(tickets_andamento * 0.8)
            
            dm.adicionar_registro(
                data_atual.date(),
                tickets_iniciados,
                tickets_finalizados,
                tickets_andamento
            )
            
            data_atual += timedelta(days=1)
    
    print("✅ Dados realistas gerados com sucesso!")

def mostrar_estatisticas():
    """
    Mostra estatísticas dos dados gerados.
    """
    dm = DataManager("dados_tickets.xlsx")
    stats = dm.obter_estatisticas()
    
    print("\n📊 ESTATÍSTICAS DOS DADOS GERADOS:")
    print("=" * 50)
    print(f"📅 Período: {stats['periodo_inicio'].strftime('%d/%m/%Y') if stats['periodo_inicio'] else 'N/A'} a {stats['periodo_fim'].strftime('%d/%m/%Y') if stats['periodo_fim'] else 'N/A'}")
    print(f"📋 Total de registros: {stats['total_registros']}")
    print(f"📥 Total de tickets iniciados: {stats['total_iniciados']}")
    print(f"✅ Total de tickets finalizados: {stats['total_finalizados']}")
    print(f"📊 Média diária - Iniciados: {stats['media_iniciados']:.1f}")
    print(f"📊 Média diária - Finalizados: {stats['media_finalizados']:.1f}")
    print(f"📊 Média diária - Em andamento: {stats['media_andamento']:.1f}")
    print("=" * 50)

if __name__ == "__main__":
    print("🎫 GERADOR DE DADOS DE EXEMPLO - DASHBOARD DE TICKETS")
    print("=" * 60)
    
    opcao = input("""
Escolha uma opção:
1. Gerar dados básicos de exemplo (30 dias)
2. Gerar dados realistas com cenários
3. Mostrar estatísticas dos dados existentes
4. Limpar dados existentes

Digite sua opção (1-4): """)
    
    if opcao == "1":
        gerar_dados_exemplo()
        mostrar_estatisticas()
    elif opcao == "2":
        gerar_dados_realistas()
        mostrar_estatisticas()
    elif opcao == "3":
        mostrar_estatisticas()
    elif opcao == "4":
        import os
        if os.path.exists("dados_tickets.xlsx"):
            os.remove("dados_tickets.xlsx")
            print("🗑️ Dados limpos com sucesso!")
        else:
            print("ℹ️ Nenhum arquivo de dados encontrado.")
    else:
        print("❌ Opção inválida!")
    
    print("\n🚀 Para usar a aplicação, execute: streamlit run app.py")
