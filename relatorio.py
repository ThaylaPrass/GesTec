import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
import pandas as pd

class HistoricoManager:
    def consultar_historico(self, cliente, data_inicio, data_fim):
        """
        Consulta o histórico de pedidos com filtros melhorados.
        """
        try:
            cn = sqlite3.connect('system.db')
            cursor = cn.cursor()

            # Converter datas para o formato correto (dd-MM-yyyy para yyyy-MM-dd)
            data_inicio_conv = datetime.strptime(data_inicio, '%d-%m-%Y').strftime('%Y-%m-%d')
            data_fim_conv = datetime.strptime(data_fim, '%d-%m-%Y').strftime('%Y-%m-%d')

            query = """
                SELECT 
                    p.id,
                    p.cliente,
                    p.descricao,
                    p.valor_und,
                    p.quantidade,
                    p.valor_total,
                    p.data_entrega
                FROM pedidos p
                WHERE 1=1
            """
            params = []

            # Adiciona filtro de cliente apenas se um cliente específico foi selecionado
            if cliente and cliente != "Todos":
                query += " AND p.cliente = ?"
                params.append(cliente)

            # Adiciona filtros de data
            query += """ 
                AND DATE(p.data_entrega) BETWEEN DATE(?) AND DATE(?)
                ORDER BY p.data_entrega DESC
            """
            params.extend([data_inicio_conv, data_fim_conv])

            # Executar a consulta
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            cn.close()

            return resultados

        except Exception as e:
            print(f"Erro na consulta do histórico: {e}")
            return []

    def exibir_historico(self, table_historico, cliente, data_inicio, data_fim):
        """
        Exibe o histórico na tabela com formatação melhorada.
        """
        try:
            # Buscar os dados
            resultados = self.consultar_historico(cliente, data_inicio, data_fim)

            # Configurar a tabela
            table_historico.setRowCount(len(resultados))
            headers = ["ID", "Cliente", "Descrição", "Valor Unit.", "Qtd", "Valor Total", "Data Entrega"]
            table_historico.setColumnCount(len(headers))
            table_historico.setHorizontalHeaderLabels(headers)

            # Preencher a tabela
            total_valor = 0
            for row, dados in enumerate(resultados):
                for col, valor in enumerate(dados):
                    item = QTableWidgetItem()
                    
                    # Formatação específica para cada tipo de dado
                    if col in [3, 5]:  # Valores monetários
                        item.setText(f"R$ {float(valor):.2f}")
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    elif col == 4:  # Quantidade
                        item.setText(str(valor))
                        item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    elif col == 6:  # Data
                        data = datetime.strptime(valor, '%Y-%m-%d').strftime('%d/%m/%Y')
                        item.setText(data)
                        item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
                    else:
                        item.setText(str(valor))
                        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                    
                    table_historico.setItem(row, col, item)
                    
                    # Somar valor total
                    if col == 5:
                        total_valor += float(valor)

            # Ajustar larguras das colunas
            table_historico.resizeColumnsToContents()
            
            # Retornar estatísticas
            return {
                'total_pedidos': len(resultados),
                'valor_total': total_valor
            }

        except Exception as e:
            print(f"Erro ao exibir histórico: {e}")
            QMessageBox.critical(None, 'Erro', f'Erro ao exibir histórico: {str(e)}')
            return {'total_pedidos': 0, 'valor_total': 0}

    def atualizar_resumo_historico(self, stats, label_total_pedidos, label_valor_total):
        """ 
        Atualiza os labels de resumo com as estatísticas do histórico
        """
        label_total_pedidos.setText(f"Total de Pedidos: {stats['total_pedidos']}")
        label_valor_total.setText(f"Valor Total: R$ {stats['valor_total']:.2f}")