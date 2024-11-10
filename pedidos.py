import sqlite3
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox

class PedidoApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db = None  # Inicia o atributo db, que será usado para operações no banco de dados
        self.carregar_pedidos()

    def initUI(self):
        # Layout
        layout = QtWidgets.QVBoxLayout(self)

        # Campos de entrada para cliente, descrição, valor unitário, quantidade, e valor total
        self.cliente_input = QtWidgets.QLineEdit(self)
        self.cliente_input.setPlaceholderText("Nome do Cliente")
        
        self.descricao_input = QtWidgets.QLineEdit(self)
        self.descricao_input.setPlaceholderText("Descrição do Produto")
        
        self.valor_unitario_input = QtWidgets.QLineEdit(self)
        self.valor_unitario_input.setPlaceholderText("Valor Unitário")
        self.valor_unitario_input.setValidator(QtGui.QDoubleValidator(0.99, 99.99, 2))
        
        self.quantidade_input = QtWidgets.QSpinBox(self)
        self.quantidade_input.setMinimum(1)
        self.quantidade_input.setMaximum(1000)
        
        self.valor_total_input = QtWidgets.QLineEdit(self)
        self.valor_total_input.setPlaceholderText("Valor Total")
        self.valor_total_input.setReadOnly(True)

        # Conectando o evento de alteração nos campos de valor unitário e quantidade
        self.valor_unitario_input.textChanged.connect(self.atualizar_valor_total)
        self.quantidade_input.valueChanged.connect(self.atualizar_valor_total)

        # Adicionando widgets ao layout
        layout.addWidget(self.cliente_input)
        layout.addWidget(self.descricao_input)
        layout.addWidget(self.valor_unitario_input)
        layout.addWidget(self.quantidade_input)
        layout.addWidget(self.valor_total_input)

        # Botão para salvar o pedido
        self.salvar_button = QtWidgets.QPushButton('Salvar Pedido', self)
        self.salvar_button.clicked.connect(self.salvar_pedido)
        layout.addWidget(self.salvar_button)

        # Tabela para exibir pedidos
        self.table_pedidos = QtWidgets.QTableWidget(self)
        layout.addWidget(self.table_pedidos)

        # Definir título da janela e exibição
        self.setWindowTitle('Cadastro de Pedido')
        self.setGeometry(100, 100, 600, 400)
        self.show()

    def atualizar_valor_total(self):
        """Atualiza o valor total automaticamente baseado no valor unitário e quantidade."""
        try:
            valor_unitario = float(self.valor_unitario_input.text())  # Pegando o valor unitário
            quantidade = self.quantidade_input.value()  # Pegando a quantidade
            valor_total = valor_unitario * quantidade  # Calculando o valor total
            self.valor_total_input.setText(f"R$ {valor_total:.2f}")  # Atualizando o campo de valor total
        except ValueError:
            self.valor_total_input.setText("R$ 0.00")  # Caso o valor unitário não seja um número válido

    def salvar_pedido(self):
        """Função que salvará o pedido no banco de dados (exemplo)."""
        cliente = self.cliente_input.text()
        descricao = self.descricao_input.text()
        valor_unitario = float(self.valor_unitario_input.text())
        quantidade = self.quantidade_input.value()
        valor_total = valor_unitario * quantidade
        data_entrega = "12/12/2024"  # Pode ser coletado de outro campo de data

        # Conectar ao banco de dados e inserir os dados
        connection = sqlite3.connect('system.db')
        cursor = connection.cursor()

        cursor.execute(""" 
            INSERT INTO pedidos (cliente, descricao, valor_und, quantidade, valor_total, data_entrega)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cliente, descricao, valor_unitario, quantidade, valor_total, data_entrega))

        # Salvar as alterações e fechar a conexão
        connection.commit()
        connection.close()

        # Limpar os campos após salvar
        self.cliente_input.clear()
        self.descricao_input.clear()
        self.valor_unitario_input.clear()
        self.quantidade_input.setValue(1)
        self.valor_total_input.clear()

        self.carregar_pedidos()  # Atualiza a tabela de pedidos

        QMessageBox.information(self, 'Sucesso', 'Pedido salvo com sucesso!')

    def carregar_pedidos(self):
        """Carrega os pedidos na tabela."""
        try:
            cn = sqlite3.connect('system.db')
            result = pd.read_sql_query("SELECT * FROM pedidos", cn)
            cn.close()

            if result.empty:
                print("Nenhum pedido encontrado.")  # Verifica se os dados estão vazios
                return

            self.table_pedidos.setRowCount(len(result))  # Define o número de linhas
            self.table_pedidos.setColumnCount(len(result.columns))  # Define o número de colunas
            self.table_pedidos.setHorizontalHeaderLabels(result.columns.tolist())  # Ajusta os nomes das colunas

            for row_idx, row in result.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_pedidos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            for i in range(len(result.columns)):
                self.table_pedidos.resizeColumnToContents(i)  # Ajusta as colunas

        except Exception as e:
            print(f"Erro ao carregar pedidos: {e}")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = PedidoApp()
    sys.exit(app.exec_())
