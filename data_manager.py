import pandas as pd
import os
from datetime import datetime, date
import streamlit as st

class DataManager:
    def __init__(self, arquivo_excel="dados_tickets.xlsx"):
        """
        Inicializa o gerenciador de dados.
        
        Args:
            arquivo_excel (str): Nome do arquivo Excel para armazenar os dados
        """
        self.arquivo_excel = arquivo_excel
        self.inicializar_arquivo()
    
    def inicializar_arquivo(self):
        """
        Inicializa o arquivo Excel se ele não existir.
        """
        if not os.path.exists(self.arquivo_excel):
            # Criar DataFrame vazio com as colunas necessárias
            df_inicial = pd.DataFrame(columns=[
                'data', 'tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'
            ])
            
            # Salvar no arquivo Excel
            try:
                df_inicial.to_excel(self.arquivo_excel, index=False)
                print(f"Arquivo {self.arquivo_excel} criado com sucesso.")
            except Exception as e:
                st.error(f"Erro ao criar arquivo Excel: {e}")
    
    def carregar_dados(self):
        """
        Carrega os dados do arquivo Excel.
        
        Returns:
            pd.DataFrame: DataFrame com os dados carregados
        """
        try:
            if os.path.exists(self.arquivo_excel):
                df = pd.read_excel(self.arquivo_excel)
                
                # Garantir que a coluna data seja do tipo datetime
                if not df.empty and 'data' in df.columns:
                    df['data'] = pd.to_datetime(df['data'])
                    # Ordenar por data
                    df = df.sort_values('data').reset_index(drop=True)
                
                return df
            else:
                return pd.DataFrame(columns=[
                    'data', 'tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'
                ])
        except Exception as e:
            st.error(f"Erro ao carregar dados: {e}")
            return pd.DataFrame(columns=[
                'data', 'tickets_iniciados', 'tickets_finalizados', 'tickets_andamento'
            ])
    
    def adicionar_registro(self, data_registro, tickets_iniciados, tickets_finalizados, tickets_andamento):
        """
        Adiciona um novo registro de tickets.
        
        Args:
            data_registro (date): Data do registro
            tickets_iniciados (int): Número de tickets iniciados
            tickets_finalizados (int): Número de tickets finalizados
            tickets_andamento (int): Número de tickets em andamento
            
        Returns:
            bool: True se o registro foi adicionado com sucesso, False caso contrário
        """
        try:
            # Carregar dados existentes
            df = self.carregar_dados()
            
            # Verificar se já existe um registro para esta data
            data_registro_str = pd.to_datetime(data_registro)
            
            if not df.empty and 'data' in df.columns:
                if data_registro_str in df['data'].values:
                    # Atualizar registro existente
                    mask = df['data'] == data_registro_str
                    df.loc[mask, 'tickets_iniciados'] = tickets_iniciados
                    df.loc[mask, 'tickets_finalizados'] = tickets_finalizados
                    df.loc[mask, 'tickets_andamento'] = tickets_andamento
                else:
                    # Adicionar novo registro
                    novo_registro = pd.DataFrame({
                        'data': [data_registro_str],
                        'tickets_iniciados': [tickets_iniciados],
                        'tickets_finalizados': [tickets_finalizados],
                        'tickets_andamento': [tickets_andamento]
                    })
                    df = pd.concat([df, novo_registro], ignore_index=True)
            else:
                # Primeiro registro
                df = pd.DataFrame({
                    'data': [data_registro_str],
                    'tickets_iniciados': [tickets_iniciados],
                    'tickets_finalizados': [tickets_finalizados],
                    'tickets_andamento': [tickets_andamento]
                })
            
            # Ordenar por data
            df = df.sort_values('data').reset_index(drop=True)
            
            # Salvar no arquivo Excel
            df.to_excel(self.arquivo_excel, index=False)
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao adicionar registro: {e}")
            return False
    
    def obter_estatisticas(self):
        """
        Calcula estatísticas básicas dos dados.
        
        Returns:
            dict: Dicionário com estatísticas
        """
        df = self.carregar_dados()
        
        if df.empty:
            return {
                'total_registros': 0,
                'periodo_inicio': None,
                'periodo_fim': None,
                'media_iniciados': 0,
                'media_finalizados': 0,
                'media_andamento': 0,
                'total_iniciados': 0,
                'total_finalizados': 0
            }
        
        return {
            'total_registros': len(df),
            'periodo_inicio': df['data'].min(),
            'periodo_fim': df['data'].max(),
            'media_iniciados': df['tickets_iniciados'].mean(),
            'media_finalizados': df['tickets_finalizados'].mean(),
            'media_andamento': df['tickets_andamento'].mean(),
            'total_iniciados': df['tickets_iniciados'].sum(),
            'total_finalizados': df['tickets_finalizados'].sum()
        }
    
    def filtrar_dados(self, data_inicio=None, data_fim=None):
        """
        Filtra os dados por período.
        
        Args:
            data_inicio (date): Data de início do filtro
            data_fim (date): Data de fim do filtro
            
        Returns:
            pd.DataFrame: DataFrame filtrado
        """
        df = self.carregar_dados()
        
        if df.empty:
            return df
        
        if data_inicio:
            df = df[df['data'].dt.date >= data_inicio]
        
        if data_fim:
            df = df[df['data'].dt.date <= data_fim]
        
        return df
    
    def excluir_registro(self, data_registro):
        """
        Exclui um registro específico.
        
        Args:
            data_registro (date): Data do registro a ser excluído
            
        Returns:
            bool: True se o registro foi excluído com sucesso, False caso contrário
        """
        try:
            df = self.carregar_dados()
            
            if df.empty:
                return False
            
            data_registro_str = pd.to_datetime(data_registro)
            
            # Remover o registro
            df = df[df['data'] != data_registro_str]
            
            # Salvar no arquivo Excel
            df.to_excel(self.arquivo_excel, index=False)
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao excluir registro: {e}")
            return False
    
    def exportar_csv(self, nome_arquivo=None):
        """
        Exporta os dados para um arquivo CSV.
        
        Args:
            nome_arquivo (str): Nome do arquivo CSV (opcional)
            
        Returns:
            str: Conteúdo do CSV como string
        """
        df = self.carregar_dados()
        
        if df.empty:
            return ""
        
        # Formatar a data para melhor visualização
        df_export = df.copy()
        df_export['data'] = df_export['data'].dt.strftime('%d/%m/%Y')
        
        if nome_arquivo:
            df_export.to_csv(nome_arquivo, index=False)
        
        return df_export.to_csv(index=False)
    
    def backup_dados(self):
        """
        Cria um backup dos dados com timestamp.
        
        Returns:
            bool: True se o backup foi criado com sucesso, False caso contrário
        """
        try:
            if os.path.exists(self.arquivo_excel):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nome_backup = f"backup_dados_tickets_{timestamp}.xlsx"
                
                df = self.carregar_dados()
                df.to_excel(nome_backup, index=False)
                
                return True
            return False
            
        except Exception as e:
            st.error(f"Erro ao criar backup: {e}")
            return False
