import urllib.parse as up
import psycopg2
from decimal import *
from datetime import *
import tkinter as tk
from tkinter import messagebox
import random
import string

def conectar_bd():
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")            
    return conn

def salvarDados(self):
        # Cria a conexão com o banco de dados
        up.uses_netloc.append("postgres")
        conn = psycopg2.connect(database="mnlfnrwe", 
                                user="mnlfnrwe", 
                                password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                                host="kesavan.db.elephantsql.com", 
                                port="5432")
        
        # Cria um cursor(objeto) para manipular o BD
        cur = conn.cursor()
        # O metodo .execute("[Codigo SQL]") manipula o BD
        cur.execute("INSERT INTO investimentos VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (self.__codigo_transacao, self.__codigo, self.__data,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao, self.__imposto, self.__valor_total))
        # Confirma as alterações no BD
        conn.commit()
        # Encerra a conexão o BD
        cur.close()
        conn.close()
        
def pesquisarAtivo():
    # global ativo_entry, chama a variável referente ao código
    # atv = ativo_entry.get(), recebe o valor da variável global
    
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    
    cur = conn.cursor()
    ativo = 'PETR4'
    cur.execute("SELECT * FROM investimentos WHERE cod_ativo = %s", (ativo,))
    
    dados = cur.fetchall()
    tabela_janela = tk.Toplevel()
    tabela_janela.geometry('1920x1080')
    tabela_janela.title("Investimentos")
    tabela = tk.Label(tabela_janela, text="Investimentos", font=("Helvetica", 16, "bold"))
    tabela.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
    
    # Criando as colunas
    colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total"]
    for i in range(len(colunas)):
        coluna_label = tk.Label(tabela_janela, text=colunas[i], font=("Helvetica", 12, "bold"))
        coluna_label.grid(row=1, column=i, padx=10, pady=10)

    # Exibe os dados na tabela
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            if j == 2:
                data = datetime.strftime(dados[i][j], '%d/%m/%Y')
                dado_label = tk.Label(tabela_janela, text=data, font=("Helvetica", 12))
            else:
                dado_label = tk.Label(tabela_janela, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+2, column=j, padx=10, pady=5)
            
            
    # Encerra a conexão com o banco de dados
    cur.close()
    conn.close()

    tabela_janela.mainloop()
    
    
def pesquisarTransacao():
    # global codigo_entry, chama a variável referente ao código
    # transacao = codigo_entry.get(), recebe o valor da variável global
    
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    
    cur = conn.cursor()
    transacao = 'P5L3WIQ9UG'
    cur.execute("SELECT * FROM investimentos WHERE cod_transacao = %s", (transacao,))
    
    dados = cur.fetchall()
    tabela_janela = tk.Toplevel()
    tabela_janela.geometry('1920x1080')
    tabela_janela.title("Investimentos")
    tabela = tk.Label(tabela_janela, text="Investimentos", font=("Helvetica", 16, "bold"))
    tabela.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
    
    # Criando as colunas
    colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total"]
    for i in range(len(colunas)):
        coluna_label = tk.Label(tabela_janela, text=colunas[i], font=("Helvetica", 12, "bold"))
        coluna_label.grid(row=1, column=i, padx=10, pady=10)

    # Exibe os dados na tabela
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            if j == 2:
                data = datetime.strftime(dados[i][j], '%d/%m/%Y')
                dado_label = tk.Label(tabela_janela, text=data, font=("Helvetica", 12))
            else:
                dado_label = tk.Label(tabela_janela, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+2, column=j, padx=10, pady=5)
            
            
    # Encerra a conexão com o banco de dados
    cur.close()
    conn.close()

    tabela_janela.mainloop()

def visualizar_historico():
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    # Cria um cursor(objeto) para manipular o BD
    cur = conn.cursor()
    # O método .execute("[Codigo SQL]") manipula o BD
    cur.execute("SELECT * FROM investimentos ORDER BY dt_transacao ASC")
    # Obtém os dados do banco de dados
    dados = cur.fetchall()

    # Cria uma nova janela para exibir a tabela
    tabela_janela = tk.Toplevel()
    tabela_janela.geometry('1920x1080')
    tabela_janela.title("Investimentos")
    
    # Criando uma tabela
    tabela = tk.Label(tabela_janela, text="Investimentos", font=("Helvetica", 16, "bold"))
    tabela.grid(row=0, column=0, columnspan=6, padx=10, pady=10)
    
    # Criando as colunas
    colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total"]
    for i in range(len(colunas)):
        coluna_label = tk.Label(tabela_janela, text=colunas[i], font=("Helvetica", 12, "bold"))
        coluna_label.grid(row=1, column=i, padx=10, pady=10)

    # Exibe os dados na tabela
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            if j == 2:
                data = datetime.strftime(dados[i][j], '%d/%m/%Y')
                dado_label = tk.Label(tabela_janela, text=data, font=("Helvetica", 12))
            else:
                dado_label = tk.Label(tabela_janela, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+2, column=j, padx=10, pady=5)
            
            
    # Encerra a conexão com o banco de dados
    cur.close()
    conn.close()

    tabela_janela.mainloop()
    
    def precoMedio(self):
        up.uses_netloc.append("postgres")
        conn = psycopg2.connect(database="mnlfnrwe", 
                                user="mnlfnrwe", 
                                password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                                host="kesavan.db.elephantsql.com", 
                                port="5432")
        cur = conn.cursor()
        
        cur.execute("SELECT preco_medio, quantidade_acoes FROM ativo WHERE cod_ativo = %s", (self.codigo,))
        dados = cur.fetchall()
        
        numerador = Decimal(self.valor_total)
        denominador = Decimal(self.quantidade)
        
        if dados and dados[0][0] is not None and dados[0][1] is not None:
            numerador += Decimal(self.quantidade) * Decimal(dados[0][0]).quantize(Decimal('.00'), rounding=ROUND_DOWN)
            denominador += Decimal(dados[0][1])
            cur.execute("UPDATE ativo SET quantidade_acoes = %s + %s WHERE cod_ativo = %s", (dados[0][1], self.quantidade, self.codigo)) 
        else:
            cur.execute("UPDATE ativo SET quantidade_acoes = %s + %s WHERE cod_ativo = %s", (0, self.quantidade, self.codigo))     
            
        pm = Decimal(numerador / denominador).quantize(Decimal('.00'), rounding=ROUND_DOWN)
        cur.execute("UPDATE ativo SET preco_medio = %s WHERE cod_ativo = %s", (pm, self.codigo))
        conn.commit()
        
        conn.close()    
        cur.close()
        
def retorno_ativo(cod_ativo):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute('SELECT retorno from investimentos WHERE cod_ativo = %s', (cod_ativo,))
    dados = cur.fetchall()
    retorno = Decimal(0).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    for i in range(len(dados)):
        retorno += Decimal(dados[i][0])
    print(retorno)
    conn.close()    
    cur.close()
    
    
    

def main():
    #pesquisarAtivo()
    #pesquisarTransacao()
    #visualizar_historico()
    retorno_ativo('PETR4')
    pass
    
if __name__ == '__main__':
    main()
