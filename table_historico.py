import sqlite3
from PyQt5 import QtCore, QtGui, QtWidgets

class RelatorioApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layout principal
        layout = QtWidgets.QVBoxLayout(self)

        # Adicionar título
        self.titulo = QtWidgets.QLabel("Selecione o intervalo de datas para o relatório", self)
        layout.addWidget(self.titulo)

        # Layout para exibir o calendário
        calendario_layout = QtWidgets.QHBoxLayout()

        # Calendário de Data de Início
        self.calendario_inicio = QtWidgets.QCalendarWidget(self)
        self.calendario_inicio.setGridVisible(True)
        self.calendario_inicio.clicked.connect(self.atualizar_data_inicio)
        calendario_layout.addWidget(QtWidgets.QLabel("Data Início:"))
        calendario_layout.addWidget(self.calendario_inicio)

        # Calendário de Data de Fim
        self.calendario_fim = QtWidgets.QCalendarWidget(self)
        self.calendario_fim.setGridVisible(True)
        self.calendario_fim.clicked.connect(self.atualizar_data_fim)
        calendario_layout.addWidget(QtWidgets.QLabel("Data Fim:"))
        calendario_layout.addWidget(self.calendario_fim)

        layout.addLayout(calendario_layout)

        # Botão para gerar o relatório
        self.gerar_button = QtWidgets.QPushButton('Gerar Relatório', self)
        self.gerar_button.clicked.connect(self.gerar_relatorio)
        layout.addWidget(self.gerar_button)

        # Tabela para exibir os pedidos
        self.table = QtWidgets.QTableWidget(self)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Cliente", "Descrição", "Valor Unitário", "Quantidade", "Valor Total", "Data Entrega"])
        layout.addWidget(self.table)

        # Definir título da janela e exibição
        self.setWindowTitle('Relatório de Pedidos')
        self.setGeometry(100, 100, 800, 400)
        self.show()

    def atualizar_data_inicio(self):
        """Atualiza a data de início quando o usuário seleciona uma data no calendário de início."""
        data_inicio = self.calendario_inicio.selectedDate().toString("yy/MM/yyyy")
        self.data_inicio_input = data_inicio  # Armazena a data no formato necessário
        print(f"Data Início selecionada: {data_inicio}")

    def atualizar_data_fim(self):
        """Atualiza a data de fim quando o usuário seleciona uma data no calendário de fim."""
        data_fim = self.calendario_fim.selectedDate().toString("yy/MM/yyyy")
        self.data_fim_input = data_fim  # Armazena a data no formato necessário
        print(f"Data Fim selecionada: {data_fim}")

    def gerar_relatorio(self):
        """Gerar o relatório de pedidos dentro do intervalo de datas selecionado."""
        if hasattr(self, 'data_inicio_input') and hasattr(self, 'data_fim_input'):
            pedidos = self.consultar_pedidos(self.data_inicio_input, self.data_fim_input)
            self.exibir_relatorio(pedidos)
        else:
            QtWidgets.QMessageBox.warning(self, "Erro", "Por favor, selecione ambas as datas (início e fim).")

    def consultar_pedidos(self, data_inicio, data_fim):
        """Consultar os pedidos entre duas datas."""
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()

        # Consulta SQL para pegar os pedidos no intervalo de datas
        cursor.execute("""
            SELECT id, cliente, descricao, valor_und, quantidade, valor_total, data_entrega 
            FROM pedidos
            WHERE data_entrega BETWEEN ? AND ?
        """, (data_inicio, data_fim))

        # Buscar todos os pedidos
        pedidos = cursor.fetchall()

        connection.close()
        return pedidos

    def exibir_relatorio(self, pedidos):
        """Exibir os pedidos em uma tabela."""
        self.table.setRowCount(len(pedidos))  # Ajusta o número de linhas conforme os dados

        # Preencher a tabela com os dados
        for i, pedido in enumerate(pedidos):
            for j, valor in enumerate(pedido):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = RelatorioApp()
    sys.exit(app.exec_())
