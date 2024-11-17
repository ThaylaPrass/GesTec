import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class HistoricoManager:
    def consultar_historico(self, cliente, data_inicio, data_fim):
        try:
            cn = sqlite3.connect('system.db')
            cursor = cn.cursor()

            # Converter as datas para o formato correto
            data_inicio_conv = datetime.strptime(data_inicio, '%d-%m-%Y').strftime('%Y-%m-%d')
            data_fim_conv = datetime.strptime(data_fim, '%d-%m-%Y').strftime('%Y-%m-%d')

            query = """
                SELECT 
                    p.id,
                    p.cliente,
                    p.data_entrega,
                    p.descricao,
                    p.valor_und,
                    p.quantidade,
                    p.valor_total
                FROM pedidos p
                WHERE p.cliente = ?
                AND DATE(p.data_entrega) BETWEEN DATE(?) AND DATE(?)
                ORDER BY p.data_entrega DESC
            """
            params = [cliente, data_inicio_conv, data_fim_conv]

            cursor.execute(query, params)
            resultados = cursor.fetchall()
            cn.close()

            print("Resultados do filtro:", resultados)  # Adiciona print para verificar os resultados do filtro
            return resultados

        except Exception as e:
            print(f"Erro na consulta do histórico: {e}")
            return []
        
        
    def exibir_historico(self, table_widget, cliente, data_inicio, data_fim):
        try:
            resultados = self.consultar_historico(cliente, data_inicio, data_fim)

            # Adiciona print para verificar os resultados
            print("Resultados da consulta:", resultados)

            # Limpa a tabela antes de preencher com novos dados
            table_widget.setRowCount(0)

            # Preenche a tabela com os resultados
            for row_number, row_data in enumerate(resultados):
                table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            
            print("Histórico exibido com sucesso!")
        except Exception as e:
            print(f"Erro ao exibir histórico: {e}")