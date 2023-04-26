import urllib.parse as up
import psycopg2
from decimal import *
from datetime import *
import tkinter as tk
from tkinter import messagebox, StringVar
import random
import string

class investimentos:
    def __init__(self, codigo_transacao ,codigo, data, quantidade, valor_unit, taxa_corretagem, tipo_transacao, valor_operacao=0.0,  imposto=0.0, valor_total=0.0):
        self.__codigo_transacao = codigo_transacao
        self.__codigo = codigo
        self.__data = data
        self.__quantidade = quantidade
        self.__valor_unit = valor_unit
        self.__taxa_corretagem = taxa_corretagem #
        self.__tipo_transacao = tipo_transacao
        # Os atributos abaixo são dados pelo programa, não pelo usuário
        self.__imposto = imposto 
        self.__valor_operacao = valor_operacao 
        self.__valor_total = valor_total 

    @property
    def codigo_transacao(self):
        return self.__codigo_transacao        
    @property
    def codigo(self):
        return self.__codigo
    @property
    def data(self):
        return self.__data
    @property
    def quantidade(self):
        return self.__quantidade
    @property
    def valor_unit(self):
        return self.__valor_unit
    @property
    def taxa_corretagem(self):
        return self.__taxa_corretagem
    @property
    def tipo_transacao(self):
        return self.__tipo_transacao
    @property
    def imposto(self):
        return self.__imposto
    @property
    def valor_operacao(self):
        return self.__valor_operacao
    @property
    def valor_total(self):
        return self.__valor_total

    def compra(self):
        self.__valor_operacao = Decimal(self.__valor_unit) * Decimal(self.__quantidade)
        self.__imposto = Decimal(self.__valor_operacao) * (Decimal(0.03) / 100)
        self.__valor_total = self.__valor_operacao + Decimal(self.__taxa_corretagem) + self.__imposto

    def venda(self):
        self.__valor_operacao = Decimal(self.__valor_unit) * Decimal(self.__quantidade)
        self.__imposto = Decimal(self.__valor_operacao) * (Decimal(0.03) / 100)
        self.__valor_total = self.__valor_operacao - Decimal(self.__taxa_corretagem) - self.__imposto
    
    
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
        
def gerar_codigo():
    # Define os caracteres válidos
    caracteres_validos = string.ascii_uppercase + string.digits
    # Gera um código aleatório de 10 caracteres
    codigo = ''.join(random.choice(caracteres_validos) for _ in range(10))
    return codigo

def cadastrar_dados():
    # chama as variaveis globais
    global formulario
    global codigo_entry
    global data_entry
    global quantidade_entry
    global valor_entry
    global tipo_operacao_var
    global taxa_entry
    # Formata os valores das variáveis globais para decimal
    valor_unit = Decimal(valor_entry.get()).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    taxa_corretagem = Decimal(taxa_entry.get()).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    tipo_op = tipo_operacao_var.get()
    # Cria o código da transação, que também é a chave primária do banco
    codigo_transacao = gerar_codigo()
    dt_transac = datetime.strptime(data_entry.get(), '%d/%m/%Y').strftime('%Y/%m/%d')

    # 
    inv = investimentos(codigo_transacao, codigo_entry.get(), dt_transac, quantidade_entry.get(), valor_unit, taxa_corretagem, tipo_op)
    
    if tipo_op == 'Compra':
        inv.compra()
    else:
        inv.venda()
        
    # Salva os dados no banco de dados    
    inv.salvarDados()

    # Feche o formulário
    formulario.destroy()
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

# Formulario de Cadastro do investimento
def abrir_formulario():
    # Cria as variáveis globais
    global formulario
    global codigo_entry
    global data_entry
    global quantidade_entry
    global valor_entry
    global tipo_operacao_var
    global taxa_entry

    formulario = tk.Toplevel(root)
    formulario.geometry('1920x1080')
    formulario.title("Cadastro")

    container = tk.Frame(formulario, bd=5)
    container.place(relx=0.5, rely=0.5, anchor='center')

    # Cria o input do código 
    tk.Label(container, text="Código:").grid(row=0, column=0)
    codigo_entry = tk.Entry(container, width=10)
    codigo_entry.grid(row=0, column=1)

    # Cria o input da data
    tk.Label(container, text="Data:").grid(row=1, column=0)
    data_entry = tk.Entry(container, width=10)
    data_entry.grid(row=1, column=1)

    # Cria o input da quantidade
    tk.Label(container, text="Quantidade:").grid(row=2, column=0)
    quantidade_entry = tk.Entry(container, width=10)
    quantidade_entry.grid(row=2, column=1)

    # Cria o input do valor de cada unidade
    tk.Label(container, text="Valor da unidade:").grid(row=3, column=0)
    valor_entry = tk.Entry(container, width=10)
    valor_entry.grid(row=3, column=1)

    # Cria uma seleção onde o usuário escolhe o tipo da operação
    tk.Label(container, text="Tipo de operação:").grid(row=4, column=0)
    tipo_operacao_var = tk.StringVar(value="Compra")
    tipo_operacao_radio_compra = tk.Radiobutton(container, text="Compra", variable=tipo_operacao_var, value="Compra")
    tipo_operacao_radio_compra.grid(row=4, column=2, sticky=tk.W)
    tipo_operacao_radio_venda = tk.Radiobutton(container, text="Venda", variable=tipo_operacao_var, value="Venda")
    tipo_operacao_radio_venda.grid(row=4, column=1, sticky=tk.E)

    # Cria o input da taxa de corretagem
    tk.Label(container, text="Taxa de corretagem:").grid(row=5, column=0)
    taxa_entry = tk.Entry(container, width=10)
    taxa_entry.grid(row=5, column=1)

    # Botão de cadastro
    cadastrar_button = tk.Button(container, text="Cadastrar", command=cadastrar_dados)
    cadastrar_button.grid(row=6, columnspan=2)
    

def abrir_historico():
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
    tabela_janela.title("Histórico de Transações")
    
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
            # Formata a data para 'ano/mes/dia'
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
def pesquisarAtivo():
    global ativoSearch_var
    
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM investimentos WHERE cod_ativo = %s", (ativoSearch_var.get(),))
    
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
    
def abrir_pesquisar_ativo():
    global ativoSearch_var
    pesquisar_ativo_janela = tk.Toplevel(root)
    pesquisar_ativo_janela.title("Pesquisar Ativo")
    
    codigo_label = tk.Label(pesquisar_ativo_janela, text="Ativo:")
    codigo_label.pack(pady=10)
    
    ativoSearch_var = StringVar()  
    ativo_entry = tk.Entry(pesquisar_ativo_janela, textvariable=ativoSearch_var) 
    ativo_entry.pack(pady=10)

    # Adiciona um botão de pesquisa
    pesquisar_btn = tk.Button(pesquisar_ativo_janela, text="Pesquisar", command=pesquisarAtivo)
    pesquisar_btn.pack(pady=10)
    
def pesquisarTransacao():
    global codigoSearch_var
    # transacao = codigo_entry.get(), recebe o valor da variável global
    
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    
    cur = conn.cursor()

    cur.execute("SELECT * FROM investimentos WHERE cod_transacao = %s ORDER BY dt_transacao ASC", (codigoSearch_var.get(),))
    
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

def abrir_pesquisar_transacao():
    global codigoSearch_var
    pesquisar_transacao_janela = tk.Toplevel(root)
    pesquisar_transacao_janela.title("Pesquisar Transação")

    # Adiciona um label
    codigo_label = tk.Label(pesquisar_transacao_janela, text="Código:")
    codigo_label.pack(pady=10)

    # Adiciona uma caixa de texto para inserir o número da transação
    codigoSearch_var = StringVar()  # Cria uma variável do tipo StringVar()
    transacao_entry = tk.Entry(pesquisar_transacao_janela, textvariable=codigoSearch_var, width=10)  # Passa a variável como argumento para a caixa de texto
    transacao_entry.pack()

    # Adiciona um botão de pesquisa
    pesquisar_btn = tk.Button(pesquisar_transacao_janela, text="Pesquisar", command=pesquisarTransacao)
    pesquisar_btn.pack(pady=10)

# Abre o menu de exibição com as opções de vosualização dos dados cadastrados
def abrir_menuExibicao():
    visualizar_janela = tk.Toplevel(root)
    visualizar_janela.geometry('1980x1080')
    visualizar_janela.title("Visualizar")

    # adiciona botão para visualizar histórico
    historico_btn = tk.Button(visualizar_janela, text="Histórico", command=abrir_historico)
    historico_btn.pack(pady=10)

    # adiciona botão para pesquisar ativo
    ativo_btn = tk.Button(visualizar_janela, text="Pesquisar Ativo", command=abrir_pesquisar_ativo)
    ativo_btn.pack(pady=10)

    # adiciona botão para pesquisar transação
    transacao_btn = tk.Button(visualizar_janela, text="Pesquisar Transação", command=abrir_pesquisar_transacao)
    transacao_btn.pack(pady=10)

    
root = tk.Tk()
def main():
    # Abre a janela principal do programa
    root.geometry('1920x1080')
    root.title("Controle de ações")

    frame = tk.Frame(root)
    frame.pack(side='top', fill='both', expand=True)
    # Configura o botão cadastrar para abri a função abrir_formulario() 
    cadastrar_btn = tk.Button(frame, text="Cadastrar", command=abrir_formulario)
    cadastrar_btn.place(relx=0.5, rely=0.45, anchor='center')

    visualizar_btn = tk.Button(frame, text="Visualizar", command=abrir_menuExibicao)
    visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')

    root.mainloop()
    
if __name__ == '__main__':
    main()
