from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox, QToolBox, QVBoxLayout, QStackedWidget, QApplication, QWidget, QMainWindow, QTableWidgetItem, QMessageBox, QPushButton, QLineEdit, QTableWidget, QCalendarWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets
from database import data_base
from login import Ui_Form
from ui_main import Ui_MainWindow
import sys
import pdb
from datetime import datetime
from historico_manager import HistoricoManager
import sqlite3
import pandas as pd




#LOGIN


class Login(QWidget, Ui_Form):
    def __init__(self) -> None:
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login do Sistema")
        
        # Campo de senha para mostrar asteriscos
        self.txt_password.setEchoMode(QLineEdit.Password)
        self.btn_login.clicked.connect(self.open_system)


    def open_system(self):
        username = self.txt_username.text()  
        password = self.txt_password.text()
        
        if username == 'admin' and password == '123':
            self.w = MainWindow()
            self.w.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Erro', 'Nome de usuário ou senha inválidos')





class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Sistema de Cadastro e Faturamento")
        
        self.db = data_base()
        self.db.Conecta()

        if not self.db.conn or not self.db.cursor:
            print("Erro: A conexão ou o cursor não foram inicializados corretamente.")
            return

        self.btn_gerar_relatorio.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_historico))
        self.table_historico = self.findChild(QTableWidget, 'tableWidget_historico')

        self.historico_manager = HistoricoManager()
        
        self.btn_excel = self.findChild(QPushButton, 'btn_excel')
        if self.btn_excel:
            self.btn_excel.clicked.connect(self.acao_exportar_para_excel)

        self.btn_pdf = self.findChild(QPushButton, 'btn_pdf')
        if self.btn_pdf:
            self.btn_pdf.clicked.connect(self.acao_exportar_para_pdf)



          

       
        ##############################################
        #TOGLLE BUTTON
        self.btn_toggle.clicked.connect(self.leFtMenu)
        ##############################################

        #Paginas do Sistema
        self.btn_home.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_home))
        self.btn_cliente.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_cadastro_cliente))    
        self.btn_produtos.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_cadastro_produto))  
        self.btn_pedidos.clicked.connect(lambda: self.Pages.setCurrentWidget(self.pg_cadastro_pedidos))
        


         
          
        # Acesso aos widgets da página de produtos
     
        self.lineEdit_nome_produto = self.findChild(QLineEdit, 'lineEdit_nome_produto')  
        self.lineEdit_quantidade_produto = self.findChild(QLineEdit, 'lineEdit_quantidade_produto')  
        self.btn_salvar_produto = self.findChild(QPushButton, 'btn_salvar_produto')  
        self.btn_deletar_produto = self.findChild(QPushButton, 'btn_deletar_produto')  
        self.btn_alterar_produto = self.findChild(QPushButton, 'btn_alterar_produto') 

        
        
        self.table_produtos = self.findChild(QTableWidget, 'tableWidget_produtos')
        


   
        # Acesso aos widgets da página de clientes
        
        self.lineEdit_nome_cliente = self.findChild(QLineEdit, 'lineEdit_nome_cliente')
        self.lineEdit_contato_cliente = self.findChild(QLineEdit, 'lineEdit_contato_cliente')
        self.btn_alterar_cliente = self.findChild(QPushButton, 'btn_alterar_cliente')
        self.btn_deletar_cliente = self.findChild(QPushButton, 'btn_deletar_cliente')
        self.btn_salvar_cliente = self.findChild(QPushButton, 'btn_salvar_cliente')


        self.table_cliente = self.findChild(QTableWidget, 'tableWidget_cliente')




        # Acesso aos widgets da página de pedidos
       
        self.lineEdit_pedido_descricao = self.findChild(QLineEdit, 'lineEdit_pedido_descricao')
        self.lineEdit_valor_und = self.findChild(QLineEdit, 'lineEdit_valor_und') 
        self.lineEdit_valor_total = self.findChild(QLineEdit, 'lineEdit_valor_total') 
        self.lineEdit_pedidos_quantidade = self.findChild(QLineEdit, 'lineEdit_pedidos_quantidade')
        self.lineEdit_pedido_nome = self.findChild(QLineEdit, 'lineEdit_pedido_nome')
        # self.lineEdit_pedido_cliente = self.findChild(QLineEdit, 'lineEdit_pedido_cliente')
        self.comboBox_clientes = self.findChild(QComboBox, 'comboBox_clientes')        
        self.lineEdit_data_entrega = self.findChild(QLineEdit, 'lineEdit_data_entrega') 
        self.btn_salvar_pedido = self.findChild(QPushButton, 'btn_salvar_pedido')
        self.btn_alterar_pedido = self.findChild(QPushButton, 'btn_alterar_pedido')
        self.btn_deletar_pedido = self.findChild(QPushButton, 'btn_deletar_pedido')

        self.table_pedidos = self.findChild(QTableWidget, 'tableWidget_pedidos')
        

        
        
        # Conectar os botões de produtos
        self.btn_salvar_produto.clicked.connect(self.adicionar_produto)  
        self.btn_deletar_produto.clicked.connect(self.deletar_produto)  
        self.btn_alterar_produto.clicked.connect(self.alterar_produto)  


        # Conectar os botões de clientes
        self.btn_salvar_cliente.clicked.connect(self.adicionar_cliente)  
        self.btn_deletar_cliente.clicked.connect(self.deletar_cliente)  
        self.btn_alterar_cliente.clicked.connect(self.alterar_cliente)
        
      
        # Conectar os botões de pedidos
        self.btn_salvar_pedido.clicked.connect(self.adicionar_pedido)
        self.btn_deletar_pedido.clicked.connect(self.deletar_pedido)
        self.btn_alterar_pedido.clicked.connect(self.alterar_pedido)

    
        # Carregar dados
        self.carregar_clientes()
        self.carregar_pedidos()
        self.carregar_produtos()
        self.preencher_comboBox_clientes()

        self.show()

     # Conectar os campos ao método de cálculo automático
        self.lineEdit_valor_und.textChanged.connect(self.calcular_valor_total)
        self.lineEdit_pedidos_quantidade.textChanged.connect(self.calcular_valor_total)

    def calcular_valor_total(self):
        try:
            valor_und = float(self.lineEdit_valor_und.text().strip()) if self.lineEdit_valor_und.text() else 0
            quantidade = int(self.lineEdit_pedidos_quantidade.text().strip()) if self.lineEdit_pedidos_quantidade.text() else 0
            valor_total = valor_und * quantidade
            self.lineEdit_valor_total.setText(f"{valor_total:.2f}")  
        except ValueError:
            self.lineEdit_valor_total.setText("0.00")  # Se os campos não forem números, define como 0


        # pdb.set_trace()


    

        #Animação do Menu   

    def leFtMenu(self):

        width = self.left_menu.width()

        if width ==0:
            newWidth = 180
        else:
            newWidth = 0

        self.animation = QtCore.QPropertyAnimation(self.left_menu, b"maximumWidth")
        self.animation.setDuration(350)  # Define a duração da animação 
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    
    

    def preencher_comboBox_clientes(self):
        try:
            # Conecta ao banco de dados
            cn = sqlite3.connect('system.db')
            cursor = cn.cursor()

            # Tenta obter os clientes da tabela 'cliente'
            cursor.execute("SELECT nome FROM cliente")
            clientes = cursor.fetchall()

            # Preenche o comboBox_clientes
            self.comboBox_clientes.clear()
            if clientes:
                for cliente in clientes:
                    self.comboBox_clientes.addItem(cliente[0])
            else:
                self.comboBox_clientes.addItem("Nenhum cliente encontrado")

            # Preenche o ComboBox de histórico 
            self.comboBox_clientes_historico.clear()
            if clientes:
                self.comboBox_clientes_historico.addItem("Todos os clientes")  # Adiciona a opção para selecionar todos
                for cliente in clientes:
                    self.comboBox_clientes_historico.addItem(cliente[0])
            else:
                self.comboBox_clientes_historico.addItem("Nenhum cliente encontrado")

            cn.close()

        except sqlite3.OperationalError as e:
            print(f"Erro ao acessar banco de dados: {e}")
            self.comboBox_clientes.clear()
            self.comboBox_clientes.addItem("Erro ao acessar o banco de dados.")
            self.comboBox_clientes_historico.clear()
            self.comboBox_clientes_historico.addItem("Erro ao acessar o banco de dados.")
        except Exception as e:
            print(f"Erro ao preencher ComboBox de clientes: {e}")
            self.comboBox_clientes.clear()
            self.comboBox_clientes.addItem("Erro desconhecido ao carregar clientes.")
            self.comboBox_clientes_historico.clear()
            self.comboBox_clientes_historico.addItem("Erro desconhecido ao carregar clientes.")


    
    
        # HISTORICO

        
        self.tableWidget_historico = QTableWidget()
        self.setup_table()

        self.btn_gerar_relatorio = self.findChild(QPushButton, 'btn_gerar_relatorio')
        if self.btn_gerar_relatorio:
            self.btn_gerar_relatorio.clicked.connect(self.filtrar_e_abrir_historico)

        self.comboBox_clientes_historico = self.findChild(QComboBox, 'comboBox_clientes_historico')
        self.calendar_inicio = self.findChild(QCalendarWidget, 'calendar_inicio')
        self.calendar_fim = self.findChild(QCalendarWidget, 'calendar_fim')

        self.pg_historico = self.findChild(QWidget, 'pg_historico')
        if self.pg_historico:
            self.table_historico = self.pg_historico.findChild(QTableWidget, 'tableWidget_historico')
            if self.table_historico:
                print("QTableWidget encontrado com sucesso!")
            else:
                print("Erro: tableWidget_historico não encontrado dentro de pg_historico!")
        else:
            print("Erro: pg_historico não encontrado!")

        # Sempre tornar a página e a tabela visíveis
        if self.pg_historico:
            self.pg_historico.setVisible(True)
        if self.table_historico:
            self.table_historico.setVisible(True)

    def setup_table(self):
        self.tableWidget_historico.setColumnCount(7)  # Defina o número de colunas
        self.tableWidget_historico.setHorizontalHeaderLabels(['ID', 'Data de Entrega', 'Cliente', 'Descrição', 'Valor Unidade', 'Quantidade', 'Valor Total'])

    def preencher_tabela(self, resultados):
        for row_idx, row_data in enumerate(resultados):
            self.tableWidget_historico.insertRow(row_idx)
            for col_idx, col_data in enumerate(row_data):
                self.tableWidget_historico.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        

    def get_cliente(self):
        return self.comboBox_clientes_historico.currentText()

    def get_data_inicio(self):
        return self.calendar_inicio.selectedDate().toString("dd-MM-yyyy")

    def get_data_fim(self):
        return self.calendar_fim.selectedDate().toString("dd-MM-yyyy")

    def filtrar_e_abrir_historico(self):
        if not self.table_historico:
            print("Erro: QTableWidget não está disponível.")
            return

        cliente = self.get_cliente()
        data_inicio = self.get_data_inicio()
        data_fim = self.get_data_fim()

        print(f"Cliente: {cliente}")
        print(f"Data Início: {data_inicio}")
        print(f"Data Fim: {data_fim}")

        self.historico_manager.exibir_historico(self.table_historico, cliente, data_inicio, data_fim)


    def acao_exportar_para_excel(self):
        cliente = self.get_cliente()
        self.historico_manager.exportar_para_excel(self.table_historico, cliente)

    def acao_exportar_para_pdf(self):
        cliente = self.get_cliente()
        self.historico_manager.exportar_para_pdf(self.table_historico, cliente)

    
    # CLIENTE
            

    def carregar_clientes(self):
        try:
            clientes = self.db.get_clients()  

            
            self.comboBox_clientes.clear()
            self.comboBox_clientes.addItem("Selecione um cliente")
            for _, nome, _ in clientes:
                self.comboBox_clientes.addItem(nome)

            
            self.comboBox_clientes_historico.clear()
            self.comboBox_clientes_historico.addItem("Selecione um cliente")
            for _, nome, _ in clientes:
                self.comboBox_clientes_historico.addItem(nome)

            
            self.table_cliente.setRowCount(len(clientes))
            self.table_cliente.setColumnCount(3)
            self.table_cliente.setHorizontalHeaderLabels(['ID', 'Nome', 'Contato'])

            for row_idx, (id_cliente, nome, contato) in enumerate(clientes):
                self.table_cliente.setItem(row_idx, 0, QTableWidgetItem(str(id_cliente)))
                self.table_cliente.setItem(row_idx, 1, QTableWidgetItem(nome))
                self.table_cliente.setItem(row_idx, 2, QTableWidgetItem(contato))

            # Ajuste o tamanho das colunas
            for i in range(3):
                self.table_cliente.resizeColumnToContents(i)

        except Exception as e:
            print(f"Erro ao carregar clientes: {e}")


    


    

    def adicionar_cliente(self):
        try:
            nome = self.lineEdit_nome_cliente.text().strip()  
            contato = self.lineEdit_contato_cliente.text().strip()

            if nome and contato:
                self.db.insert_client(nome, contato) 
                self.carregar_clientes() 
                self.lineEdit_nome_cliente.clear()
                self.lineEdit_contato_cliente.clear()
                QMessageBox.information(self, 'Sucesso', 'Cliente cadastrado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao cadastrar o cliente.')



    def alterar_cliente(self):
        try:
            selected_items = self.table_cliente.selectedItems()
            if selected_items:
                id_cliente = selected_items[0].text() 
                nome = self.lineEdit_nome_cliente.text().strip()
                contato = self.lineEdit_contato_cliente.text().strip()

                if nome and contato:  
                    self.db.update_client(id_cliente, nome, contato)  
                    self.carregar_clientes()  
                    self.lineEdit_nome_cliente.clear()
                    self.lineEdit_contato_cliente.clear()
                    QMessageBox.information(self, 'Sucesso', 'Cliente atualizado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um cliente para alterar.')

        except Exception as e:
            print(f"Erro ao alterar cliente: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao alterar o cliente.')


    def deletar_cliente(self):
        try:
            selected_items = self.table_cliente.selectedItems()
            if selected_items:
                id_cliente = selected_items[0].text()  
                self.db.remove_client(id_cliente) 
                self.carregar_clientes()  
                QMessageBox.information(self, 'Sucesso', 'Cliente removido com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um cliente para remover.')

        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o cliente.')



            # PEDIDOS


    def carregar_pedidos(self):
        try:
            cn = sqlite3.connect('system.db')
            result = pd.read_sql_query("SELECT * FROM pedidos", cn)
            cn.close()

            self.table_pedidos.setRowCount(len(result))
            self.table_pedidos.setColumnCount(len(result.columns))
            self.table_pedidos.setHorizontalHeaderLabels(['ID', 'Cliente', 'Data de Entrega', 'Nome do Pedido', 'Descrição', 'Valor Unitário', 'Quantidade', 'Valor Total'])

            for row_idx, row in result.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_pedidos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Redimensiona as colunas para ajustar ao conteúdo
            for i in range(len(result.columns)):
                self.table_pedidos.resizeColumnToContents(i)

        except Exception as e:
            print(f"Erro ao carregar pedidos: {e}")


    def adicionar_pedido(self):
        try:
            cliente = self.comboBox_clientes.currentText().strip() if self.comboBox_clientes is not None else None
            data_entrega = self.lineEdit_data_entrega.text().strip() if self.lineEdit_data_entrega is not None else None
            nome_pedido = self.lineEdit_pedido_nome.text().strip() if self.lineEdit_pedido_nome is not None else None
            descricao = self.lineEdit_pedido_descricao.text().strip() if self.lineEdit_pedido_descricao is not None else None
            valor_und = self.lineEdit_valor_und.text().strip() if self.lineEdit_valor_und is not None else None
            quantidade = self.lineEdit_pedidos_quantidade.text().strip() if self.lineEdit_pedidos_quantidade is not None else None
            valor_total = self.lineEdit_valor_total.text().strip() if self.lineEdit_valor_total is not None else None
            

            
            
            print(f"Cliente: {cliente}")
            print(f"Data de Entrega: {data_entrega}")
            print(f"Nome do Pedido: {nome_pedido}")
            print(f"Descrição: {descricao}")
            print(f"Valor Unitário: {valor_und}")
            print(f"Quantidade: {quantidade}")
            print(f"Valor Total: {valor_total}")
            

            if cliente and data_entrega and nome_pedido and descricao and valor_und and quantidade and valor_total:
                # Valida a data de entrega
                try:
                    data_entrega_formatada = datetime.strptime(data_entrega, '%d-%m-%Y').date()
                    print(f"Data de Entrega Formatada: {data_entrega_formatada}")
                except ValueError:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira uma data de entrega válida no formato dd-mm-yyyy.')
                    return
                
                self.db.insert_order(cliente, data_entrega, nome_pedido, descricao, valor_und, quantidade, valor_total)
                self.carregar_pedidos()  
                self.lineEdit_data_entrega.clear()
                self.lineEdit_pedido_nome.clear()
                self.lineEdit_pedido_descricao.clear()
                self.lineEdit_valor_und.clear()
                self.lineEdit_pedidos_quantidade.clear()
                self.lineEdit_valor_total.clear()
                
                QMessageBox.information(self, 'Sucesso', 'Pedido cadastrado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
        except Exception as e:
            print(f"Erro ao adicionar pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao cadastrar o pedido.')


    def alterar_pedido(self):
        try:
            selected_items = self.table_pedidos.selectedItems()
            if selected_items:
                row = self.table_pedidos.currentRow()
                
                id_pedido = self.table_pedidos.item(row, 0).text().strip()
                cliente = self.table_pedidos.item(row, 1).text().strip()
                data_entrega = self.table_pedidos.item(row, 2).text().strip()
                nome_pedido = self.table_pedidos.item(row, 3).text().strip()
                descricao = self.table_pedidos.item(row, 4).text().strip()
                valor_und = self.table_pedidos.item(row, 5).text().strip()
                quantidade = self.table_pedidos.item(row, 6).text().strip()
                valor_total = self.table_pedidos.item(row, 7).text().strip()

                if cliente and data_entrega and nome_pedido and descricao and valor_und and quantidade and valor_total:
                    self.db.update_order(id_pedido, cliente, data_entrega, nome_pedido, descricao, valor_und, quantidade, valor_total)
                    self.carregar_pedidos()
                    self.limpar_campos_pedido()
                    QMessageBox.information(self, 'Sucesso', 'Pedido alterado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos.')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um pedido para alterar.')
        except Exception as e:
            print(f"Erro ao alterar pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao alterar o pedido.')


    def deletar_pedido(self):
        try:
            selected_items = self.table_pedidos.selectedItems()
            if selected_items:
                id_pedido = selected_items[0].text() 
                self.db.remove_order(id_pedido)  

                self.carregar_pedidos() 

                QMessageBox.information(self, 'Sucesso', 'Pedido removido com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um pedido para remover.')
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o pedido.')

    def limpar_campos_pedido(self):
        self.comboBox_clientes.clear()
        self.lineEdit_data_entrega.clear()
        self.lineEdit_pedido_nome.clear()
        self.lineEdit_pedido_descricao.clear()
        self.lineEdit_valor_und.clear()
        self.lineEdit_pedidos_quantidade.clear()
        self.lineEdit_valor_total.clear()
        



        #HISTÓRICO

    

    
    # def consultar_historico(self, cliente, data_inicio, data_fim):
    #     try:
    #         # Certifique-se de que a conexão e o cursor estão inicializados corretamente
    #         if self.db.conn and self.db.cursor:
    #             query = """
    #                 SELECT h.id, h.id_pedido, p.cliente, p.descricao, h.data_entrega, h.valor_und, h.quantidade, h.valor_total
    #                 FROM historico h
    #                 JOIN pedidos p ON h.id_pedido = p.id
    #                 WHERE p.cliente LIKE ? AND p.data_entrega BETWEEN ? AND ?
    #             """
    #             self.db.cursor.execute(query, (f'%{cliente}%', data_inicio, data_fim))  # Passando os parâmetros
    #             historico = self.db.cursor.fetchall()
    #             return historico
    #         else:
    #             print("Erro: Conexão ou cursor não inicializado corretamente.")
    #             return []
    #     except Exception as e:
    #         print(f"Erro ao consultar o histórico: {e}")
    #         return []


    # def exibir_historico(self):
    #     try:
    #         # Obtenha os valores dos filtros
    #         cliente = self.comboBox_clientes_historico.currentText().strip()  # Por exemplo, de um comboBox
    #         data_inicio = self.calendar_inicio.selectedDate().toString("dd-MM-yyyy")  # Usando o formato correto
    #         data_fim = self.calendar_fim.selectedDate().toString("dd-MM-yyyy")  # Usando o formato correto

    #         # Consultar os dados do histórico
    #         historico = self.consultar_historico(cliente, data_inicio, data_fim)

    #         # Configurar a tabela
    #         self.table_historico.setRowCount(len(historico))
    #         self.table_historico.setColumnCount(8)  # Ajustar o número de colunas conforme necessário
    #         self.table_historico.setHorizontalHeaderLabels(
    #             ["ID", "ID Pedido", "Cliente", "Descrição", "Data de Entrega", "Valor Unitário", "Quantidade", "Valor Total"]
    #         )

    #         # Inserir os dados na tabela
    #         for i, registro in enumerate(historico):
    #             for j, valor in enumerate(registro):
    #                 self.table_historico.setItem(i, j, QTableWidgetItem(str(valor)))

    #     except Exception as e:
    #         print(f"Erro ao exibir histórico: {e}")


    
# PRODUTO




    def carregar_produtos(self):
        try:
            cn = sqlite3.connect('system.db')
            result = pd.read_sql_query("SELECT * FROM produtos", cn)
            cn.close()

            # Define o número de linhas e colunas da tabela
            self.table_produtos.setRowCount(len(result))
            self.table_produtos.setColumnCount(len(result.columns))
            self.table_produtos.setHorizontalHeaderLabels(result.columns)

            # Preenche as células da tabela com os dados
            for row_idx, row in result.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_produtos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Ajusta o tamanho das colunas
            for i in range(len(result.columns)):
                self.table_produtos.resizeColumnToContents(i)

        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")

    def adicionar_produto(self):
        try:
            nome = self.lineEdit_nome_produto.text().strip()  
            quantidade = self.lineEdit_quantidade_produto.text().strip()

            if nome and quantidade.isdigit():  
                self.db.insert_product(nome, int(quantidade)) 
                self.carregar_produtos()  
                self.lineEdit_nome_produto.clear() 
                self.lineEdit_quantidade_produto.clear() 
                QMessageBox.information(self, 'Sucesso', 'Produto cadastrado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos corretamente.')

        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao cadastrar o produto.')


    def deletar_produto(self):
        try:
            selected_items = self.table_produtos.selectedItems()
            if selected_items:
                id_produto = selected_items[0].text() 
                self.db.remove_product(int(id_produto)) 
                self.carregar_produtos()  
                QMessageBox.information(self, 'Sucesso', f'Produto com ID {id_produto} removido com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um produto para remover.')
        except Exception as e:
            print(f"Erro ao remover produto: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o produto.')


    def alterar_produto(self):
        try:
            selected_items = self.table_produtos.selectedItems()
            if selected_items:
                id_produto = selected_items[0].text()  
                nome = self.lineEdit_nome_produto.text().strip()
                nova_quantidade = self.lineEdit_quantidade_produto.text().strip()

                if nome and nova_quantidade.isdigit():
                    nova_quantidade = int(nova_quantidade)
                    self.db.update_product(int(id_produto), nome, nova_quantidade)  
                    self.carregar_produtos() 
                    self.lineEdit_quantidade_produto.clear()  
                    QMessageBox.information(self, 'Sucesso', 'Produto alterado com sucesso!')
                else:
                    QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos corretamente.')

        except ValueError:
            QMessageBox.warning(self, 'Erro', 'A quantidade deve ser um número inteiro!')
        except Exception as e:
            print(f"Erro ao alterar produto: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao alterar o produto.')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # window = Login()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


