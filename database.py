import sqlite3

class data_base:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def Conecta(self):
        try:
            self.conn = sqlite3.connect('system.db')
            self.cursor = self.conn.cursor()
            print("Conexão estabelecida com o banco de dados.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def close_connection(self):
        try:
            if self.conn:
                self.conn.close()
                print("Conexão com o banco de dados fechada.")
        except Exception as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")


    # PRODUTO

    def insert_product(self, nome, quantidade):
        try:
            self.cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
            self.conn.commit()
            print(f"Produto '{nome}' adicionado com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")

    def remove_product(self, nome):
        try:
            self.cursor.execute("DELETE FROM produtos WHERE nome=?", (nome,))
            self.conn.commit()
            print(f"Produto '{nome}' removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover produto: {e}")

    def update_product(self, nome, nova_quantidade):
        try:
            self.cursor.execute("UPDATE produtos SET quantidade=? WHERE nome=?", (nova_quantidade, nome))
            self.conn.commit()
            print(f"Produto '{nome}' atualizado com a nova quantidade {nova_quantidade}.")
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")

    def get_products(self):
        try:
            self.cursor.execute("SELECT * FROM produtos")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar produtos: {e}")
            return []


    # CLIENTE

    def get_clients(self):
        try:
            # Seleciona o ID, nome e contato de cada cliente
            self.cursor.execute("SELECT id, nome, contato FROM cliente")
            return self.cursor.fetchall()  # Retorna uma lista de tuplas (id, nome, contato)
        except Exception as e:
            print(f"Erro ao obter clientes: {e}")
            return []

    def insert_client(self, nome, contato):
        try:
            # Insere apenas o nome e o contato. O ID será autoincrementado
            self.cursor.execute("INSERT INTO cliente (nome, contato) VALUES (?, ?)", (nome, contato))
            self.conn.commit()  # Commit para salvar a inserção no banco de dados
        except Exception as e:
            print(f"Erro ao adicionar cliente: {e}")

    def update_client(self, id_cliente, nome, contato):
        try:
            # Atualiza o nome e o contato do cliente baseado no ID
            self.cursor.execute("UPDATE cliente SET nome = ?, contato = ? WHERE id = ?", (nome, contato, id_cliente))
            self.conn.commit()  # Commit para salvar as alterações no banco de dados
        except Exception as e:
            print(f"Erro ao atualizar cliente: {e}")


    def remove_client(self, id_cliente):
        try:
            # Deleta o cliente com base no ID
            self.cursor.execute("DELETE FROM cliente WHERE id = ?", (id_cliente,))
            self.conn.commit()  # Commit para salvar a exclusão no banco de dados
        except Exception as e:
            print(f"Erro ao remover cliente: {e}")



    # PEDIDOS

    def insert_order(self, cliente, descricao, valor_und, quantidade, valor_total, data_de_entrega):
        try:
            self.cursor.execute(''' 
                INSERT INTO Pedidos ("Nome do Cliente", "Descrição", "Detalhes", "Valor Und", "Quantidade", "Valor Total", "Data de Entrega")
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (cliente, descricao, valor_und, quantidade, valor_total, data_de_entrega))
            self.conn.commit()
        except sqlite3.IntegrityError:
            raise Exception(f'Já existe um pedido para o cliente: {cliente}')
        except Exception as e:
            print(f"Erro ao adicionar pedido: {e}")

    def remove_order(self, nome_cliente):
        try:
            self.cursor.execute('''
                DELETE FROM Pedidos WHERE "Nome do Cliente" = ?
            ''', (nome_cliente,))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")

    def update_order(self, nome_cliente, descricao, valor_und, quantidade, valor_total, data_de_entrega):
        try:
            self.cursor.execute('''
                UPDATE Pedidos
                SET "Descrição" = ?, "Valor Und" = ?, "Quantidade" = ?, "Valor Total" = ?, "Data de Entrega" = ?
                WHERE "Nome do Cliente" = ?
            ''', (descricao, valor_und, quantidade, valor_total, data_de_entrega, nome_cliente))
            self.conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar pedido: {e}")


    # HISTORICO

    def insert_historico(self, cliente, descricao, valor_und, quantidade, valor_total, data_entrega, data_historico, hora_historico):
        try:
            self.cursor.execute('''
                INSERT INTO historico (cliente, descricao, valor_und, quantidade, valor_total, data_entrega, data_historico, hora_historico)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cliente, descricao, valor_und, quantidade, valor_total, data_entrega, data_historico, hora_historico))
            self.conn.commit()
            print(f"Registro de histórico para o cliente '{cliente}' inserido com sucesso.")
        except Exception as e:
            print(f"Erro ao inserir no histórico: {e}")

    def update_historico(self, id_historico, cliente, descricao, valor_und, quantidade, valor_total, data_entrega, data_historico, hora_historico):
        try:
            self.cursor.execute('''
                UPDATE historico
                SET cliente = ?, descricao = ?, valor_und = ?, quantidade = ?, valor_total = ?, data_entrega = ?, data_historico = ?, hora_historico = ?
                WHERE id = ?
            ''', (cliente, descricao, valor_und, quantidade, valor_total, data_entrega, data_historico, hora_historico, id_historico))
            self.conn.commit()
            print(f"Registro de histórico com ID {id_historico} atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar o histórico: {e}")

    def remove_historico(self, id_historico):
        try:
            self.cursor.execute('''
                DELETE FROM historico WHERE id = ?
            ''', (id_historico,))
            self.conn.commit()
            print(f"Registro de histórico com ID {id_historico} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover o histórico: {e}")

    def get_historico(self):
        try:
            self.cursor.execute("SELECT * FROM historico")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar histórico: {e}")
            return []
