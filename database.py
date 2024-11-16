import sqlite3
from datetime import datetime

class data_base:
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
        data_entrega = datetime.now().strftime("%d/%m/%Y")
        data_entrega = datetime.strptime(data_entrega, "%d/%m/%Y").strftime("%d/%m/%Y")




    # PRODUTO

    def insert_product(self, nome, quantidade):
        try:
            self.cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
            self.conn.commit()
            print(f"Produto '{nome}' adicionado com sucesso!")
        except Exception as e:
            print(f"Erro ao adicionar produto: {e}")

    def remove_product(self, id_produto):
        try:
            self.cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
            self.conn.commit()
            print(f"Produto com ID '{id_produto}' removido com sucesso!")
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
            self.cursor.execute("SELECT id, nome, contato FROM cliente")
            return self.cursor.fetchall()
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

    def get_pedidos(self):
        self.cursor.execute('''
            SELECT cliente, data_entrega, descricao, valor_und, quantidade, valor_total FROM pedidos
        ''')
        return self.cursor.fetchall()

    def insert_order(self, cliente, data_entrega, descricao, valor_und, quantidade, valor_total):
        try:
            self.cursor.execute('''
                INSERT INTO pedidos (cliente, data_entrega, descricao, valor_und, quantidade, valor_total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (cliente, data_entrega, descricao, valor_und, quantidade, valor_total))
            self.conn.commit()
            print(f"Pedido para o cliente '{cliente}' adicionado com sucesso!")
        except sqlite3.IntegrityError:
            raise Exception(f'Já existe um pedido para o cliente: {cliente}')
        except Exception as e:
            print(f"Erro ao adicionar pedido: {e}")

    def remove_order(self, id_pedido):
        try:
            self.cursor.execute('''
                DELETE FROM pedidos WHERE id = ?
            ''', (id_pedido,))
            self.conn.commit()
            print(f"Pedido com ID '{id_pedido}' removido com sucesso!")
        except Exception as e:
            print(f"Erro ao remover pedido: {e}")

    def update_order(self, id_pedido, cliente, data_entrega, descricao, valor_und, quantidade, valor_total):
        try:
            self.cursor.execute('''
                UPDATE pedidos
                SET cliente = ?, data_entrega = ?, descricao = ?, valor_und = ?, quantidade = ?, valor_total = ?
                WHERE id = ?
            ''', (cliente, data_entrega, descricao, valor_und, quantidade, valor_total, id_pedido))
            self.conn.commit()
            print(f"Pedido com ID '{id_pedido}' alterado com sucesso!")
        except Exception as e:
            print(f"Erro ao alterar pedido: {e}")


    # # HISTORICO


    # def get_historico(self):
    #     try:
    #         self.cursor.execute("SELECT * FROM historico")
    #         return self.cursor.fetchall()
    #     except Exception as e:
    #         print(f"Erro ao buscar histórico: {e}")
    #         return []
