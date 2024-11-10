from PyQt5.QtWidgets import QStyledItemDelegate, QComboBox, QToolBox, QVBoxLayout, QStackedWidget, QApplication, QWidget, QMainWindow, QTableWidgetItem, QMessageBox, QPushButton, QLineEdit, QTableWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from database import data_base
from login import Ui_Form
from ui_main import Ui_MainWindow
import sys

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
         
    def keyPressEvent(self, event):
    # Verifica se a tecla pressionada é Enter ou Return
        if event.key() in (QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter):
            self.btn_login.click()  # Simula o clique no botão

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
        self.preencher_comboBox_clientes()
        self.db = data_base()
        self.db.Conecta()
        # appIcon = QIcon(u"")
        # self.setWindowIcon(appIcon)
           

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
     
        
        
        self.lineEdit_nome_produto = self.findChild(QLineEdit, 'lineEdit_nome_produto')  # Corrigido para QLineEdit
        self.lineEdit_quantidade_produto = self.findChild(QLineEdit, 'lineEdit_quantidade_produto')  # Correto para QLineEdit
        self.btn_salvar_produto = self.findChild(QPushButton, 'btn_salvar_produto')  # Continua sendo QPushButton
        self.btn_deletar_produto = self.findChild(QPushButton, 'btn_deletar_produto')  # Continua sendo QPushButton
        self.btn_alterar_produto = self.findChild(QPushButton, 'btn_alterar_produto')  # Faltava essa linha para o botão de alterar

        
        
        self.table_produtos = self.findChild(QTableWidget, 'tableWidget_produtos')
        
   
        # Acesso aos widgets da página de clientes
        self.btn_btn_salvar_cliente = self.findChild(QPushButton, 'btn_salvar_cliente')
        self.lineEdit_nome_cliente = self.findChild(QLineEdit, 'lineEdit_nome_cliente')
        self.lineEdit_contato_cliente = self.findChild(QLineEdit, 'lineEdit_contato_cliente')
        self.btn_alterar_cliente = self.findChild(QPushButton, 'btn_alterar_cliente')
        self.btn_alterar_cliente = self.findChild(QPushButton, 'btn_alterar_cliente')
        self.btn_deletar_cliente = self.findChild(QPushButton, 'btn_deletar_cliente')

        self.table_cliente = self.findChild(QTableWidget, 'tableWidget_cliente')


        # Acesso aos widgets da página de pedidos
       
        self.lineEdit_pedido_client = self.findChild(QLineEdit, 'lineEdit_pedido_client')
        self.lineEdit_pedido_descricao = self.findChild(QLineEdit, 'lineEdit_pedido_descricao')
        self.lineEdit_valor_und = self.findChild(QLineEdit, 'lineEdit_valor_und') 
        self.lineEdit_pedidos_quantidade = self.findChild(QLineEdit, 'lineEdit_pedidos_quantidade')
        self.comboBox_cliente = self.findChild(QComboBox, 'comboBox_cliente')
        self.lineEdite_data_de_entrega = self.findChild(QLineEdit, 'lineEdite_data_de_entrega')
        self.btn_salvar_pedido = self.findChild(QPushButton, 'btn_salvar_pedido')
        self.btn_alterar_pedido = self.findChild(QPushButton, 'btn_alterar_pedido')
        self.btn_deletar_pedido = self.findChild(QPushButton, 'btn_deletar_pedido')

        self.table_pedidos = self.findChild(QTableWidget, 'tableWidget_pedidos')
        


         # ToolBox histórico
        self.layout_historico = QVBoxLayout()
    #   self.frame_4 = QWidget(self)
        self.frame_4.setLayout(self.layout_historico)
        self.tableWidget_historico = QTableWidget(self.frame_4)
        self.layout_historico.addWidget(self.tableWidget_historico)

        self.table_historico = self.findChild(QTableWidget, 'tableWidget_historico')

            

        
        # Conectar os botões de produtos
        self.btn_salvar_produto.clicked.connect(self.adicionar_produto)  
        self.btn_deletar_produto.clicked.connect(self.deletar_produto)  
        self.btn_alterar_produto.clicked.connect(self.alterar_produto)  


        # Conectar os botões de clientes
        self.btn_btn_salvar_cliente.clicked.connect(self.adicionar_cliente)  
        self.btn_deletar_cliente.clicked.connect(self.deletar_cliente)  
        self.btn_alterar_cliente.clicked.connect(self.alterar_cliente)
        
      
        # Conectar os botões de pedidos
        self.btn_salvar_pedido.clicked.connect(self.adicionar_pedido)
        self.btn_deletar_pedido.clicked.connect(self.deletar_pedido)
        self.btn_alterar_pedido.clicked.connect(self.alterar_pedido)

        self.carregar_clientes()
        self.carregar_pedidos () # Adiciona a chamada para carregar pedidos ao iniciar a aplicação
        self.carregar_produtos() # Adiciona a chamada para carregar clientes ao iniciar a aplicação


        self.preencher_comboBox_clientes()

    

        #Animação do Menu   

    def leFtMenu(self):

        width = self.left_menu.width()

        if width ==0:
            newWidth = 180
        else:
            newWidth = 0

        self.animation = QtCore.QPropertyAnimation(self.left_menu, b"maximumWidth")
        self.animation.setDuration(500)  # Define a duração da animação em 500 milissegundos
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


    

    # CLIENTE
            

    

   

    def preencher_comboBox_clientes(self):
        try:
            # Conecta ao banco de dados
            cn = sqlite3.connect('system.db')
            cursor = cn.cursor()

            # Tenta obter os clientes da tabela 'cliente'
            cursor.execute("SELECT nome FROM cliente")  # Alterei 'clientes' para 'cliente'
            clientes = cursor.fetchall()

            # Preenche o ComboBox com os clientes
            self.comboBox_cliente.clear()  # Limpa o ComboBox antes de adicionar novos itens
            if clientes:
                for cliente in clientes:
                    self.comboBox_cliente.addItem(cliente[0])  # Adiciona cada cliente ao ComboBox
            else:
                self.comboBox_cliente.addItem("Nenhum cliente encontrado")  # Se não houver clientes, exibe uma mensagem

            cn.close()

        except sqlite3.OperationalError as e:
            # Se houve erro ao acessar o banco de dados, mostra erro no ComboBox
            print(f"Erro ao acessar banco de dados: {e}")
            self.comboBox_cliente.clear()
            self.comboBox_cliente.addItem("Erro ao acessar o banco de dados.")
        except Exception as e:
            # Caso outro erro aconteça
            print(f"Erro ao preencher ComboBox de clientes: {e}")
            self.comboBox_cliente.clear()
            self.comboBox_cliente.addItem("Erro desconhecido ao carregar clientes.")



    def carregar_clientes(self):
        try:
            clientes = self.db.get_clients()  # Obtenha a lista de clientes do banco de dados

            # Preencher o QComboBox com os nomes dos clientes
            self.comboBox_cliente.clear()  # Limpa o QComboBox antes de adicionar
            self.comboBox_cliente.addItem("Selecione um cliente")  # Adiciona um item padrão
            for _, nome, _ in clientes:
                self.comboBox_cliente.addItem(nome)  # Adiciona cada nome ao combo box

            # Atualiza a tabela de clientes
            self.table_cliente.setRowCount(len(clientes))  # Define o número de linhas da tabela
            self.table_cliente.setColumnCount(3)  # Defina o número de colunas (ajuste conforme necessário)
            self.table_cliente.setHorizontalHeaderLabels(['ID', 'Nome', 'Contato'])  # Defina os cabeçalhos das colunas

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
            nome = self.lineEdit_nome_cliente.text().strip()  # Remove espaços em branco das extremidades
            contato = self.lineEdit_contato_cliente.text().strip()

            if nome and contato:  # Verifica se ambos os campos estão preenchidos
                self.db.insert_client(nome, contato)  # O ID será gerado automaticamente
                self.carregar_clientes()  # Atualiza a tabela de clientes
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
                id_cliente = selected_items[0].text()  # ID do cliente selecionado
                nome = self.lineEdit_nome_cliente.text().strip()
                contato = self.lineEdit_contato_cliente.text().strip()

                if nome and contato:  # Verifica se ambos os campos estão preenchidos
                    self.db.update_client(id_cliente, nome, contato)  # Atualiza pelo ID
                    self.carregar_clientes()  # Atualiza a tabela de clientes
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
                id_cliente = selected_items[0].text()  # ID do cliente selecionado
                self.db.remove_client(id_cliente)  # Deleta pelo ID
                self.carregar_clientes()  # Atualiza a tabela de clientes
                QMessageBox.information(self, 'Sucesso', 'Cliente removido com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um cliente para remover.')

        except Exception as e:
            print(f"Erro ao remover cliente: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o cliente.')





    # PEDIDO
            


            
     
    def carregar_pedidos(self):
        try:
            cn = sqlite3.connect('system.db')
            result = pd.read_sql_query("SELECT * FROM pedidos", cn)  # Corrigir para 'pedidos'
            cn.close()

            self.table_pedidos.setRowCount(len(result))
            self.table_pedidos.setColumnCount(len(result.columns))
            self.table_pedidos.setHorizontalHeaderLabels(['ID', 'Nome Cliente', 'Descrição', 'Detalhes', 'Valor Unitário', 'Quantidade', 'Valor Total', 'Data de Entrega'])

            for row_idx, row in result.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_pedidos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            # Ajusta o tamanho das colunas
            for i in range(len(result.columns)):
                self.table_pedidos.resizeColumnToContents(i)

        except Exception as e:
            print(f"Erro ao carregar pedidos: {e}")


        


    def adicionar_pedido(self):
        try:
            # Verifica se o comboBox_cliente foi inicializado corretamente
            if self.comboBox_cliente is None:
                print("comboBox_cliente não foi inicializado corretamente")
                QMessageBox.critical(self, 'Erro', 'Erro: comboBox_cliente não foi inicializado.')
                return

            # Verifica se o cliente foi selecionado
            cliente = self.comboBox_cliente.currentText().strip()
            if not cliente or cliente == "Selecione um cliente":  
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um cliente.')
                return

            # Verifica os outros campos
            descricao = self.lineEdit_pedido_descricao.text().strip()
            if not descricao:
                QMessageBox.warning(self, 'Erro', 'Por favor, insira uma descrição.')
                return
            
            valor_und_text = self.lineEdit_valor_und.text().strip()
            if not valor_und_text:
                QMessageBox.warning(self, 'Erro', 'Por favor, insira o valor unitário.')
                return
            
            quantidade_text = self.lineEdit_pedidos_quantidade.text().strip()
            if not quantidade_text:
                QMessageBox.warning(self, 'Erro', 'Por favor, insira a quantidade.')
                return
            
            valor_total_text = self.lineEdit_valor_total.text().strip()
            if not valor_total_text:
                QMessageBox.warning(self, 'Erro', 'Por favor, insira o valor total.')
                return
            
            data_entrega = self.lineEdite_data_de_entrega.text().strip()
            if not data_entrega:
                QMessageBox.warning(self, 'Erro', 'Por favor, insira a data de entrega.')
                return

            # Conversão para float e int após garantir que os campos não estão vazios
            valor_und = float(valor_und_text)
            quantidade = int(quantidade_text)
            valor_total = float(valor_total_text)

            # Insere o pedido no banco de dados
            self.db.insert_order(cliente, descricao, valor_und, quantidade, valor_total, data_entrega)

            # Limpar os campos após a inserção
            self.lineEdit_pedido_descricao.clear()
            self.lineEdit_valor_und.clear()
            self.lineEdit_pedidos_quantidade.clear()
            self.lineEdit_valor_total.clear()
            self.lineEdite_data_de_entrega.clear()

            # Atualizar a tabela de pedidos
            self.carregar_pedidos()

            # Mostrar uma mensagem de sucesso
            QMessageBox.information(self, 'Sucesso', 'Pedido adicionado com sucesso!')

        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira valores numéricos válidos para a quantidade e o valor unitário.')
        except Exception as e:
            print(f"Erro ao adicionar pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao adicionar o pedido.')






    
    def alterar_pedido(self):
        try:
            selected_items = self.table_pedidos.selectedItems()
            if selected_items:
                id_pedido = selected_items[0].text()  # Assumindo que o ID do pedido está na primeira coluna
                cliente = self.comboBox_cliente.currentText().strip()
                descricao = self.lineEdit_pedido_descricao.text().strip()
                valor_und_text = self.lineEdit_valor_und.text().strip()
                quantidade_text = self.lineEdit_pedidos_quantidade.text().strip()
                valor_total_text = self.lineEdit_valor_total.text().strip()
                data_entrega = self.lineEdite_data_de_entrega.text().strip()

                if not cliente or cliente == "Selecione um cliente":
                    QMessageBox.warning(self, 'Erro', 'Por favor, selecione um cliente.')
                    return
                if not descricao:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira uma descrição.')
                    return
                if not valor_und_text:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira o valor unitário.')
                    return
                if not quantidade_text:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira a quantidade.')
                    return
                if not valor_total_text:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira o valor total.')
                    return
                if not data_entrega:
                    QMessageBox.warning(self, 'Erro', 'Por favor, insira a data de entrega.')
                    return

                valor_und = float(valor_und_text)
                quantidade = int(quantidade_text)
                valor_total = float(valor_total_text)

                self.db.update_order(id_pedido, cliente, descricao, valor_und, quantidade, valor_total, data_entrega)
                self.carregar_pedidos()
                self.limpar_campos_pedido()
                QMessageBox.information(self, 'Sucesso', 'Pedido alterado com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um pedido para alterar.')
        except ValueError:
            QMessageBox.warning(self, 'Erro', 'Por favor, insira valores numéricos válidos para os campos de valor unitário, quantidade e valor total.')
        except Exception as e:
            print(f"Erro ao alterar pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao alterar o pedido.')

    def deletar_pedido(self):
        try:
            selected_items = self.table_pedidos.selectedItems()
            if selected_items:
                id_pedido = selected_items[0].text()  # Assumindo que o ID do pedido está na primeira coluna
                self.db.remove_order(int(id_pedido))  # Remove o pedido do banco de dados
                self.carregar_pedidos()  # Atualiza a tabela de pedidos
                QMessageBox.information(self, 'Sucesso', 'Pedido removido com sucesso!')
            else:
                QMessageBox.warning(self, 'Erro', 'Por favor, selecione um pedido para remover.')
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")
            QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o pedido.')

    def limpar_campos_pedido(self):
        self.lineEdit_pedido_client.clear()
        self.lineEdit_pedido_descricao.clear()
        self.lineEdit_valor_und.clear()
        self.lineEdit_pedidos_quantidade.clear()
        self.lineEdit_valor_total.clear()
        self.lineEdite_data_de_entrega.clear()





    # def selecionar_historico(self):
    #     # Altere o índice do QStackedWidget para a página de histórico
    #     self.Pages.setCurrentWidget(self.pg_historico)  # Ajuste 'pg_historico' conforme o nome da sua página

    #     # Selecione o item do ToolBox para a página de histórico
    #     self.toolBox.addItem(self.frame_historico, "Histórico")
    #     self.toolBox.setCurrentIndex(0)  # Ajuste o índice conforme necessário

    #     # Conecte a mudança do ToolBox ao método de seleção do histórico
    #     self.toolBox.currentChanged.connect(self.selecionar_historico)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


# window = Login()






# PRODUTO





    # def carregar_produtos(self):
    #     try:
    #         cn = sqlite3.connect('system.db')
    #         result = pd.read_sql_query("SELECT * FROM produtos", cn)
    #         cn.close()

    #         # Define o número de linhas e colunas da tabela
    #         self.table_produtos.setRowCount(len(result))
    #         self.table_produtos.setColumnCount(len(result.columns))
    #         self.table_produtos.setHorizontalHeaderLabels(result.columns)

    #         # Preenche as células da tabela com os dados
    #         for row_idx, row in result.iterrows():
    #             for col_idx, value in enumerate(row):
    #                 self.table_produtos.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

    #         # Ajusta o tamanho das colunas
    #         for i in range(len(result.columns)):
    #             self.table_produtos.resizeColumnToContents(i)

    #     except Exception as e:
    #         print(f"Erro ao carregar produtos: {e}")

    # def adicionar_produto(self):
    #     try:
    #         nome = self.lineEdit_nome_produto.text().strip()  # Remover espaços em branco
    #         quantidade = self.lineEdit_quantidade_produto.text().strip()

    #         if nome and quantidade.isdigit():  # Verifica se quantidade é um número válido
    #             self.db.insert_product(nome, int(quantidade))  # Insere o produto no banco de dados
    #             self.carregar_produtos()  # Atualiza a tabela de produtos
    #             self.lineEdit_nome_produto.clear()  # Limpa o campo de nome
    #             self.lineEdit_quantidade_produto.clear()  # Limpa o campo de quantidade
    #             QMessageBox.information(self, 'Sucesso', 'Produto cadastrado com sucesso!')
    #         else:
    #             QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos corretamente.')

    #     except Exception as e:
    #         print(f"Erro ao adicionar produto: {e}")
    #         QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao cadastrar o produto.')


    # def deletar_produto(self):
    #     try:
    #         selected_items = self.table_produtos.selectedItems()
    #         if selected_items:
    #             id_produto = selected_items[0].text()  # Assumindo que o ID do produto está na primeira coluna
    #             self.db.remove_product(int(id_produto))  # Remove o produto do banco de dados
    #             self.carregar_produtos()  # Atualiza a tabela de produtos
    #         else:
    #             QMessageBox.warning(self, 'Erro', 'Por favor, selecione um produto para remover.')
    #     except Exception as e:
    #         print(f"Erro ao remover produto: {e}")
    #         QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao remover o produto.')

    # def alterar_produto(self):
    #     try:
    #         selected_items = self.table_produtos.selectedItems()
    #         if selected_items:
    #             id_produto = selected_items[0].text()  # Assumindo que o ID do produto está na primeira coluna
    #             nome = self.lineEdit_nome_produto.text().strip()
    #             nova_quantidade = self.lineEdit_quantidade_produto.text().strip()

    #             if nome and nova_quantidade.isdigit():
    #                 nova_quantidade = int(nova_quantidade)
    #                 self.db.update_product(int(id_produto), nome, nova_quantidade)  # Atualiza o produto no banco de dados
    #                 self.carregar_produtos()  # Atualiza a tabela de produtos
    #                 self.lineEdit_quantidade_produto.clear()  # Limpa o campo de quantidade
    #                 QMessageBox.information(self, 'Sucesso', 'Produto alterado com sucesso!')
    #             else:
    #                 QMessageBox.warning(self, 'Erro', 'Por favor, preencha todos os campos corretamente.')

    #     except ValueError:
    #         QMessageBox.warning(self, 'Erro', 'A quantidade deve ser um número inteiro!')
    #     except Exception as e:
    #         print(f"Erro ao alterar produto: {e}")
    #         QMessageBox.critical(self, 'Erro', 'Ocorreu um erro ao alterar o produto.')

