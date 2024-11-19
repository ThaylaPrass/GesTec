import sqlite3
from datetime import datetime
import pandas as pd
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime

class HistoricoManager:
    def consultar_historico(self, cliente, data_inicio, data_fim):
        try:
            cn = sqlite3.connect('system.db')
            cursor = cn.cursor()

            # Converter as datas para o formato correto
            data_inicio_conv = datetime.strptime(data_inicio, '%d-%m-%Y').strftime('%d-%m-%Y')
            data_fim_conv = datetime.strptime(data_fim, '%d-%m-%Y').strftime('%d-%m-%Y')

            print(f"Consultando histórico para cliente: {cliente}, entre {data_inicio_conv} e {data_fim_conv}")

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
                AND p.data_entrega BETWEEN ? AND ?
                ORDER BY p.data_entrega DESC
            """
            params = [cliente, data_inicio_conv, data_fim_conv]

            cursor.execute(query, params)
            resultados = cursor.fetchall()
            cn.close()

            print("Resultados do filtro:", resultados)
            return resultados

        except Exception as e:
            print(f"Erro na consulta do histórico: {e}")
            return []
        
    def setup_table(self, table_widget):
        table_widget.setColumnCount(7)  # Define o número de colunas
        table_widget.setHorizontalHeaderLabels(['id_pedido', 'Cliente', 'Data de Entrega', 'Descrição', 'Valor Unidade', 'Quantidade', 'Valor Total'])
            
    def exibir_historico(self, table_widget, cliente, data_inicio, data_fim):
        try:
            # Consultar os dados do histórico
            resultados = self.consultar_historico(cliente, data_inicio, data_fim)

            # Adiciona print para verificar os resultados
            print("Resultados da consulta:", resultados)

            # Limpa a tabela antes de preencher com novos dados
            table_widget.setRowCount(0)

            if not resultados:
                print("Nenhum resultado encontrado para os filtros aplicados.")
                return

            # Configurar os cabeçalhos das colunas
            table_widget.setColumnCount(7)  # Número de colunas da tabela
            table_widget.setHorizontalHeaderLabels([
                "ID", "Cliente", "Data de Entrega", "Descrição", 
                "Valor Unitário", "Quantidade", "Valor Total"
            ])

            # Preenche a tabela com os resultados
            for row_number, row_data in enumerate(resultados):
                table_widget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            # Ajusta automaticamente as colunas para o conteúdo
            table_widget.resizeColumnsToContents()

            # Garante que a coluna de ID não esteja oculta
            table_widget.setColumnHidden(0, False)

            print("Histórico exibido com sucesso!")
        except Exception as e:
            print(f"Erro ao exibir histórico: {e}")

    
    def exportar_para_excel(self, table_widget):
        try:
            # Cria uma lista para armazenar os dados
            dados = []

            # Lê os dados da tabela
            for row in range(table_widget.rowCount()):
                linha = []
                for column in range(table_widget.columnCount()):
                    item = table_widget.item(row, column)
                    linha.append(item.text() if item else "")
                dados.append(linha)

            # Cria um DataFrame com os dados da tabela
            colunas = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
            df = pd.DataFrame(dados, columns=colunas)

            data_hora_atual = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formata a data e hora
            # Caminho fixo para salvar o arquivo Excel
            caminho_arquivo =  f"C:/Users/thayl/OneDrive/Área de Trabalho/Projeto 4 Semestre/Excel/historico_{data_hora_atual}.xlsx"

            # Salva o DataFrame no caminho especificado
            df.to_excel(caminho_arquivo, index=False)

            QMessageBox.information(None, "Sucesso", f"Arquivo Excel exportado com sucesso para:\n{caminho_arquivo}")
        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Ocorreu um erro ao exportar: {e}")



    def exportar_para_pdf(self, table_widget):
        try:
            
            data_hora_atual = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            
            caminho_pdf = f"C:/Users/thayl/OneDrive/Área de Trabalho/Projeto 4 Semestre/PDF/historico_{data_hora_atual}.pdf"
            c = canvas.Canvas(caminho_pdf, pagesize=landscape(A4))

            
            largura, altura = landscape(A4)
            y = altura - 40  # Margem superior

            # Títulos das colunas
            colunas = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
            c.setFont("Helvetica-Bold", 12)
            c.drawCentredString(largura / 2, y, "Relatório de Histórico")
            y -= 20

            # Imprimir cabeçalhos
            c.setFont("Helvetica-Bold", 10)
            col_width = largura / len(colunas)  # Ajustar largura das colunas

            for i, coluna in enumerate(colunas):
                c.drawCentredString((i + 0.5) * col_width, y, coluna)
            y -= 20

            # Imprimir os dados da tabela
            c.setFont("Helvetica", 10)
            for row in range(table_widget.rowCount()):
                for col in range(table_widget.columnCount()):
                    item = table_widget.item(row, col)
                    text = item.text() if item else ""
                    c.drawCentredString((col + 0.5) * col_width, y, text)
                y -= 20
                if y < 50:  # Nova página se ultrapassar o limite
                    c.showPage()
                    c.setFont("Helvetica", 10)
                    y = altura - 50

            # # Adicionar linhas à tabela
            # c.setLineWidth(1)
            # y = altura - 90
            # for row in range(table_widget.rowCount() + 1):
            #     c.line(50, y, largura - 50, y)
            #     y -= 20
            # x_offset = 50
            # for col in range(table_widget.columnCount() + 1):
            #     c.line(x_offset, altura - 70, x_offset, y + 20)
            #     x_offset += col_width

            c.save()
            QMessageBox.information(None, "Sucesso", f"Arquivo PDF exportado com sucesso para:\n{caminho_pdf}")
        except Exception as e:
            print(f"Ocorreu um erro ao exportar: {e}")
            QMessageBox.critical(None, "Erro", f"Ocorreu um erro ao exportar o PDF:\n{e}")