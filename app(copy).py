import urllib.parse as up
import psycopg2
from decimal import Decimal, ROUND_DOWN, ROUND_UP
from datetime import *
import tkinter as tk
from tkinter import messagebox, StringVar, ttk
# tkcalendar é uma biblioteca, tem que baixar
from tkcalendar import Calendar, DateEntry
import random
import string

class investimentos:
    def __init__(self, codigo_transacao ,codigo, data, quantidade, valor_unit, taxa_corretagem, tipo_transacao, valor_operacao=0.0,  imposto=0.0, valor_total=0.0, retorno = 0):
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
        self.__retorno = retorno

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
    @property
    def retorno_lp(self):
        return self.__retorno

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
        cur.execute("INSERT INTO investimentos VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s)", (self.__codigo_transacao, self.__codigo, self.__data,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao, self.__imposto, self.__valor_total, 0.00 ,self.__retorno))

        # Confirma as alterações no BD
        conn.commit()
        # Encerra a conexão o BD
        cur.close()
        conn.close()
        
    def atualizarDados(self):     
        up.uses_netloc.append("postgres")
        conn = psycopg2.connect(database="mnlfnrwe", 
                                user="mnlfnrwe", 
                                password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                                host="kesavan.db.elephantsql.com", 
                                port="5432")
        cur = conn.cursor()

        # Atualiza as informações da transação com base no código da transação
        cur.execute("UPDATE investimentos SET cod_ativo = %s, dt_transacao = %s, quantidade = %s, valor_unit = %s, taxa_corretagem = %s, tipo_transacao = %s, valor_operacao = %s, imposto = %s, valor_total = %s WHERE cod_transacao = %s",
                    (self.__codigo, self.__data,self.__quantidade, self.__valor_unit, self.__taxa_corretagem, self.__tipo_transacao, self.__valor_operacao, self.__imposto, self.__valor_total, self.__codigo_transacao,))
        
        # Commita as mudanças no banco de dados
        conn.commit()

        # Encerra a conexão com o banco de dados
        cur.close()
        conn.close()
    
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
            numerador = Decimal(numerador)+Decimal(dados[0][1]) * Decimal(dados[0][0]).quantize(Decimal('.00'), rounding=ROUND_DOWN)
            denominador += Decimal(dados[0][1])
            cur.execute("UPDATE ativo SET quantidade_acoes = quantidade_acoes + %s WHERE cod_ativo = %s", ( self.__quantidade, self.__codigo)) 
            cur.execute("UPDATE ativo SET acoes_compradas = acoes_compradas + %s WHERE cod_ativo = %s", ( self.__quantidade, self.__codigo)) 
        else:
            cur.execute("UPDATE ativo SET quantidade_acoes = %s + %s WHERE cod_ativo = %s", (0, self.__quantidade, self.__codigo))     
            cur.execute("UPDATE ativo SET acoes_compradas = %s + %s WHERE cod_ativo = %s", (0,self.__quantidade, self.__codigo)) 
            
        pm = Decimal(numerador / denominador).quantize(Decimal('.00'), rounding=ROUND_DOWN)
        cur.execute("UPDATE ativo SET preco_medio = %s WHERE cod_ativo = %s", (pm, self.codigo))
        cur.execute("UPDATE investimentos SET pm = %s WHERE cod_transacao = %s", (pm, self.codigo_transacao))
        conn.commit()
        
        conn.close()    
        cur.close()

        
    def retorno(self):
        up.uses_netloc.append("postgres")
        conn = psycopg2.connect(database="mnlfnrwe", 
                                user="mnlfnrwe", 
                                password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                                host="kesavan.db.elephantsql.com", 
                                port="5432")
        cur = conn.cursor()
        
        cur.execute("select preco_medio, acoes_vendidas from ativo where cod_ativo = %s", (self.codigo,))
        dados = cur.fetchall()
        
        self.__retorno = (Decimal(self.__valor_total) - (Decimal(self.__quantidade) * Decimal(dados[0][0]))).quantize(Decimal('.00'), rounding=ROUND_DOWN)
        if dados and dados[0][0] is not None and dados[0][1] is not None:
            cur.execute("UPDATE ativo SET quantidade_acoes = quantidade_acoes - %s, acoes_vendidas = acoes_vendidas + %s WHERE cod_ativo = %s", (self.__quantidade, self.__quantidade, self.__codigo)) 
            conn.commit()
        else:
            cur.execute("UPDATE ativo SET quantidade_acoes = quantidade_acoes - %s, acoes_vendidas = %s + %s WHERE cod_ativo = %s", (self.__quantidade, 0,self.__quantidade, self.__codigo))           
            conn.commit()
        
        conn.close()
        cur.close()
        
def retorno_geral():
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute('SELECT retorno FROM ativo')
    dados = cur.fetchall()
    retorno = Decimal(0)
    for i in range(len(dados)):
        retorno += Decimal(dados[i][0])
    print(retorno)
    conn.close()    
    cur.close()    
    return retorno

def atualizar_lucro_prejuizo():
    lucro_prejuizo = retorno_geral()
    lucro_prejuizo_label.config(text=f"Retorno Total: R$ {lucro_prejuizo:.2f}")
    #lucro_prejuizo_label.after(1000, atualizar_lucro_prejuizo)

           
def retorno_ativo(cod_ativo):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute('SELECT retorno from investimentos WHERE cod_ativo = %s', (cod_ativo,))
    dados = cur.fetchall()
    retorno = Decimal(0).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    for i in range(len(dados)):
        retorno += Decimal(dados[i][0])
    print(retorno)
    cur.execute('UPDATE ativo SET retorno = %s WHERE cod_ativo = %s', (retorno, cod_ativo))
    conn.commit()
    conn.close()    
    cur.close()
            
def calcular_pm(cod_ativo):
    conn = conectar_bd()
    cur = conn.cursor()

    cur.execute("SELECT quantidade, valor_total, cod_transacao, tipo_transacao FROM investimentos where cod_ativo = %s ORDER BY dt_transacao asc", (cod_ativo,))
    dados = cur.fetchall()
      
    quantidade_total = Decimal(0)
    primeira_linha = True
    
    for dado in dados:  
        numerador = Decimal(dado[1]) #valor totacod_ativo
        print(f"\nFora: {numerador}")
        denominador = Decimal(dado[0]) # quantidade
        quantidade_total += Decimal(dado[0]) # quantidade
        print(f'Fora: {denominador}')
        print(f"Fora: {dado[2]}")
        if dado[3] == 'Compra':
            if primeira_linha:
                # Adiciona a quantidade de ações comprada na coluna quantidade_acoes(ações possuidas atualmente) que tem valor 0
                cur.execute("UPDATE ativo SET quantidade_acoes = %s + %s WHERE cod_ativo = %s", (0, dado[0], cod_ativo))  
                # Está adicionando a quantidade de ações comprada na coluna acoes_compradas(guarda a quantidade total de ações compradas) que tem valor 0
                cur.execute("UPDATE ativo SET acoes_compradas = %s + %s WHERE cod_ativo = %s", (0,dado[0], cod_ativo)) 
                #DOWN ou UP?
                pm = Decimal(numerador / denominador).quantize(Decimal('.00'), rounding=ROUND_UP)
                print(f"Dentro p1: {pm}")
                cur.execute("UPDATE ativo SET preco_medio = %s WHERE cod_ativo = %s", (pm, cod_ativo))
                cur.execute("UPDATE investimentos SET pm = %s WHERE cod_transacao = %s", (pm, dado[2]))
                primeira_linha = False
            # Caso possua transações anteriores
            else:
            #if dados and dados2[0][0] is not None and dados2[0][1] is not None:
                cur.execute("SELECT preco_medio, quantidade_acoes FROM ativo WHERE cod_ativo = %s", (cod_ativo,))
                dados2 = cur.fetchall()
                print(f'Numerador else: {numerador}')
                print(f'Preço médio: {dados2[0][0]}')
                print(f'Quantidade de ações: {dados2[0][1]}')
                numerador = Decimal(numerador) + (Decimal(dados2[0][1]) * Decimal(dados2[0][0])).quantize(Decimal('.00'), rounding=ROUND_DOWN)
                print(f'quantidade total: {quantidade_total}')
                print(f'Numerador else: {numerador}')
                denominador += Decimal(dados2[0][1])
                print(f'denominador: {denominador}')
                cur.execute("UPDATE ativo SET quantidade_acoes = quantidade_acoes + %s WHERE cod_ativo = %s", (dado[0], cod_ativo))
                cur.execute("UPDATE ativo SET acoes_compradas = acoes_compradas + %s WHERE cod_ativo = %s", (dado[0], cod_ativo))
                # DOWN ou UP?
                pm = Decimal(numerador / denominador).quantize(Decimal('.00'), rounding=ROUND_UP)
                print(f"Dentro p2: {pm}")
                print(f"Dentro p2: {dado[2]}")
                cur.execute("UPDATE ativo SET preco_medio = %s WHERE cod_ativo = %s", (pm, cod_ativo))
                cur.execute("UPDATE investimentos SET pm = %s WHERE cod_transacao = %s", (pm, dado[2]))
        else:  # É uma operação de venda
            cur.execute("SELECT preco_medio FROM ativo WHERE cod_ativo = %s", (cod_ativo,))
            pmed = cur.fetchone()
            print(f'Venda: {pmed}')
            quantidade_total -= denominador  # Reduz a quantidade total de ações
            print(f'Venda: {quantidade_total}')
            cur.execute("UPDATE ativo SET quantidade_acoes = quantidade_acoes - %s WHERE cod_ativo = %s", (denominador, cod_ativo))
            cur.execute("UPDATE ativo SET acoes_vendidas = acoes_vendidas + %s WHERE cod_ativo = %s", (denominador, cod_ativo))
            cur.execute("UPDATE investimentos SET pm = %s WHERE cod_transacao = %s", (pmed[0], dado[2]))  # Define o preço médio como o último calculado para operações de venda
        
    conn.commit()
    cur.close()
    conn.close()
    

def conectar_bd():
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")            
    return conn

def informacao_ativo(cod,tp = True):
    conn = conectar_bd()
    cur = conn.cursor()
    cur.execute("select empresa, cod_ativo, preco_medio from ativo where cod_ativo = %s", (cod,))
    dados = cur.fetchall()
    cur.close()
    conn.close()
    if tp:    
        return messagebox.showinfo("Cadastro Concluído", f"Empresa: {dados[0][0]}\nCódigo Ativo: {dados[0][1]}\nPreço Médio: {dados[0][2]}")

    else:
        return messagebox.showinfo("Cadastro Concluído", f"Empresa: {dados[0][0]}\nCódigo Ativo: {dados[0][1]}\nPreço Médio: {dados[0][2]}")
#    return messagebox.showinfo("Sucesso", f"Código Ativo: {dados[0][0]}\nEmpresa: {dados[0][1]}\nAções Possuídas: {dados[0][2]}\nAções Compradas: {dados[0][3]}\nAções Vendidas: {dados[0][4]}\nPreço Médio: {dados[0][5]}")
    
def gerar_codigo():
    # Define os caracteres válidos
    caracteres_validos = string.ascii_uppercase + string.digits
    # Gera um código aleatório de 10 caracteres
    codigo = ''.join(random.choice(caracteres_validos) for _ in range(4))
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
    inv = investimentos(codigo_transacao, codigo_entry.get().upper(), dt_transac, quantidade_entry.get(), valor_unit, taxa_corretagem, tipo_op)    
    
    if tipo_op == 'Compra':
        inv.compra()
        inv.salvarDados()
        calcular_pm(inv.codigo)
        formulario.destroy()
        informacao_ativo(inv.codigo)
    else:
        inv.venda()
        inv.retorno()
        inv.salvarDados()
        # Feche o formulário
        formulario.destroy()
        retorno_ativo(inv.codigo)
        atualizar_lucro_prejuizo()
        informacao_ativo(inv.codigo)
    

# Formulario de Cadastro do investimento
def abrir_formulario(up):
    # Cria as variáveis globais
    global formulario
    global codigo_entry
    global data_entry
    global quantidade_entry
    global valor_entry
    global tipo_operacao_var
    global taxa_entry
    from tkinter import ttk 

    formulario = tk.Toplevel(root)
    formulario.geometry('600x500')
    if up == 'cd':
        formulario.title("Cadastro")
    if up == 'up':
        formulario.title("Atualizar Cadastro")

    container = tk.Frame(formulario, bd=5)
    container.place(relx=0.5, rely=0.5, anchor='center')

    # Cria o input do código 
    tk.Label(container, text="Código:").grid(row=0, column=0)
    codigo_entry = tk.Entry(container, width=10)
    codigo_entry.grid(row=0, column=1)
    
    # Cria o input da data
    tk.Label(container, text="Data:").grid(row=1, column=0)
    data_entry = DateEntry(container, date_pattern="dd/mm/Y", width=9)
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
    if up == 'cd':
        cadastrar_button = tk.Button(container, text="Cadastrar", command=cadastrar_dados)
        cadastrar_button.grid(row=6, column=1, padx=(0, 10))
    elif up == 'up':
        atualizar_btn = tk.Button(container, text="Confirmar atualização", command=atualizar_transacao)
        atualizar_btn.grid(row=6, column=1, padx=(0, 10))

    cancelar_btn = tk.Button(container, text='Cancelar', command=lambda: formulario.destroy())
    cancelar_btn.grid(row=7, column=1, pady=(10, 0))
    
def abrir_historico():
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    # Cria um cursor(objeto) para manipular o BD
    cur = conn.cursor()
    # O método abaixo puxar todos os dados da tabela investimentos em ordem de mais antigo(em cima) para mais recente(embaixo)
    cur.execute("SELECT * FROM investimentos ORDER BY dt_transacao ASC")
    # Obtém os dados do banco de dados
    dados = cur.fetchall()
    cur.close()
    conn.close()
    # Cria uma nova janela para exibir a tabela
    tabela_janela = tk.Toplevel()
    tabela_janela.geometry('1700x800')
    tabela_janela.title("Investimentos")
    
    tabela = tk.Label(tabela_janela, text="Investimentos", font=("Helvetica", 16, "bold"))
    tabela.grid(row=0, column=0, columnspan=6, padx=10, pady=10)

    # Criando as colunas
    colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total", 'Preço Médio',"Retorno"]
    for i in range(len(colunas)):
        coluna_label = tk.Label(tabela_janela, text=colunas[i], font=("Helvetica", 12, "bold"))
        coluna_label.grid(row=1, column=i, padx=10, pady=10)

     # Exibe os dados na tabela
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            # Formata a data para 'ano/mes/dia'
            if j == 2: # Quando for o indice da data ele pega o valor vindo do banco de dados e formata no formato dd/mm/aa
                data = datetime.strftime(dados[i][2], '%d/%m/%Y')
                dado_label = tk.Label(tabela_janela, text=data, font=("Helvetica", 12))
            else:
                dado_label = tk.Label(tabela_janela, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+2, column=j, padx=10, pady=5)
            
            
    # Encerra a conexão com o banco de dados

    fechar_btn = tk.Button(tabela_janela, text='Fechar', command=lambda:tabela_janela.destroy())
    fechar_btn.place(relx=0.04, rely=0.03, anchor='center')
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
    
    cur.execute("SELECT empresa, quantidade_acoes, acoes_compradas, acoes_vendidas, preco_medio, retorno FROM ativo WHERE cod_ativo = %s", (ativoSearch_var.get().upper(),))
    empresa_info = cur.fetchone()
    
    cur.execute("SELECT * FROM investimentos WHERE cod_ativo = %s ORDER BY dt_transacao ASC", (ativoSearch_var.get().upper(),))
    dados = cur.fetchall()
    cur.close()
    conn.close()
    if empresa_info is not None:
        tabela_janela = tk.Toplevel()
        tabela_janela.title("Investimentos")
        tabela_janela.geometry('1710x800')

        # Exibir informações do ativo
        info_frame = tk.Frame(tabela_janela)
        info_frame.pack(pady=10)

        info_labels = ["Nome da Empresa:", "Quantidade de Ações Possuídas:", "Ações Compradas:", "Ações Vendidas:", "Preço Médio:", "Retorno:"]
        for i, label_text in enumerate(info_labels):
            label = tk.Label(info_frame, text=label_text, font=("Helvetica", 12, "bold"))
            label.grid(row=i, column=0, padx=10, pady=10)

            value_label = tk.Label(info_frame, text=str(empresa_info[i]), font=("Helvetica", 12))
            value_label.grid(row=i, column=1, padx=10, pady=10)

        # Criar tabela de investimentos
        tabela_frame = tk.Frame(tabela_janela)
        tabela_frame.pack(pady=10)

        # Criando as colunas
        colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total","Preço Médio", "Retorno"]
        for i in range(len(colunas)):
            coluna_label = tk.Label(tabela_frame, text=colunas[i], font=("Helvetica", 12, "bold"))
            coluna_label.grid(row=0, column=i, padx=10, pady=10)

        # Exibe os dados na tabela INVESTIMENTOS
        for i in range(len(dados)):
            for j in range(len(dados[i])):
                if j == 2:  # Quando for o índice da data ele pega o valor vindo do banco de dados e formata no formato dd/mm/aa
                    data = datetime.strftime(dados[i][j], '%d/%m/%Y')
                    dado_label = tk.Label(tabela_frame, text=data, font=("Helvetica", 12))                      
                else:
                    dado_label = tk.Label(tabela_frame, text=str(dados[i][j]), font=("Helvetica", 12))
                dado_label.grid(row=i+1, column=j, padx=10, pady=5)
 
    fechar_btn = tk.Button(tabela_janela, text='Fechar', command=lambda:tabela_janela.destroy())
    fechar_btn.place(relx=0.04, rely=0.05, anchor='center')
    tabela_janela.mainloop()
    
def abrir_pesquisar_ativo():
    global ativoSearch_var
    pesquisar_ativo_janela = tk.Toplevel(root)
    pesquisar_ativo_janela.geometry('300x150')
    pesquisar_ativo_janela.title("Pesquisar Ativo")
    
    codigo_label = tk.Label(pesquisar_ativo_janela, text="Ativo:")
    codigo_label.pack(pady=10)
    
    ativoSearch_var = StringVar()  
    ativo_entry = tk.Entry(pesquisar_ativo_janela, textvariable=ativoSearch_var) 
    ativo_entry.pack(pady=10)

    # Adiciona um botão de pesquisa
    pesquisar_btn = tk.Button(pesquisar_ativo_janela, text="Pesquisar", command=lambda: (pesquisar_ativo_janela.destroy() ,pesquisarAtivo()))
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
    # Não é necessário ordenar, mas num faz mal
    cur.execute("SELECT * FROM investimentos WHERE cod_transacao = %s ORDER BY dt_transacao ASC", (codigoSearch_var.get().upper(),))
    
    dados = cur.fetchall()
    tabela_janela = tk.Toplevel()
    tabela_janela.geometry('1710x100')
    tabela_janela.title("Transação")
    # Criando as colunas
    tabela_frame = tk.Frame(tabela_janela)
    tabela_frame.pack(pady=10)

    # Criando as colunas
    colunas = ["Cód. Transação", "Código", "Data", "Quantidade", "Valor Unitário", "Taxa de Corretagem", "Tipo Transação", "Valor Operação", "Imposto", "Valor Total", "Preço Médio", "Retorno"]
    for i in range(len(colunas)):
        coluna_label = tk.Label(tabela_frame, text=colunas[i], font=("Helvetica", 12, "bold"))
        coluna_label.grid(row=0, column=i, padx=10, pady=10)

    # Exibe os dados na tabela INVESTIMENTOS
    for i in range(len(dados)):
        for j in range(len(dados[i])):
            if j == 2:  # Quando for o índice da data ele pega o valor vindo do banco de dados e formata no formato dd/mm/aa
                data = datetime.strftime(str(dados[i][j]), '%d/%m/%Y')
                dado_label = tk.Label(tabela_frame, text=data, font=("Helvetica", 12))
            else:
                dado_label = tk.Label(tabela_frame, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+1, column=j, padx=10, pady=5)
            
    # Encerra a conexão com o banco de dados
    cur.close()
    conn.close()
    fechar_btn = tk.Button(tabela_janela, text='Fechar', command=lambda:tabela_janela.destroy())
    fechar_btn.place(relx=0.02, rely=0.06, anchor='center')
    tabela_janela.mainloop()
def atualizar_transacao():
    global formulario
    global codigo_entry
    global data_entry
    global quantidade_entry
    global valor_entry
    global tipo_operacao_var
    global taxa_entry
    global codigoSearch_var
    # Formata os valores das variáveis globais para decimal
    valor_unit = Decimal(valor_entry.get()).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    taxa_corretagem = Decimal(taxa_entry.get()).quantize(Decimal('.00'), rounding=ROUND_DOWN)
    tipo_op = tipo_operacao_var.get()
    codigo_transacao = codigoSearch_var.get()
    dt_transac = datetime.strptime(data_entry.get(), '%d/%m/%Y').strftime('%Y/%m/%d')
    inv = investimentos(codigo_transacao, codigo_entry.get(), dt_transac, quantidade_entry.get(), valor_unit, taxa_corretagem, tipo_op)
    
    if tipo_op == 'Compra':
        inv.compra()
    else:
        inv.venda()
        
    # Salva os dados no banco de dados    
    inv.atualizarDados()
    
    formulario.destroy()
    messagebox.showinfo("Sucesso", "Transação atualizada com sucesso!")
    
def excluir_transacao():
    global codigoSearch_var
    global pesquisar_transacao_janela
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    
    cur = conn.cursor()
    
    cur.execute('DELETE FROM investimentos WHERE cod_transacao = %s', (codigoSearch_var.get().upper(),))
    messagebox.showinfo("Exclusão de transação", "Transação excluída com sucesso!")

    conn.commit()
    
    conn.close()
    cur.close()
    
def abrir_pesquisar_transacao(tp):
    global codigoSearch_var
    global pesquisar_transacao_janela
    global formulario
    pesquisar_transacao_janela = tk.Toplevel(root)
    pesquisar_transacao_janela.geometry('300x150')
    pesquisar_transacao_janela.title("Pesquisar Transação")

    # Adiciona um label
    codigo_label = tk.Label(pesquisar_transacao_janela, text="Código:")
    codigo_label.pack(pady=12)

    # Adiciona uma caixa de texto para inserir o número da transação
    codigoSearch_var = StringVar()  # Cria uma variável do tipo StringVar()
    transacao_entry = tk.Entry(pesquisar_transacao_janela, textvariable=codigoSearch_var, width=10)  # Passa a variável como argumento para a caixa de texto
    transacao_entry.pack()

    # Adiciona um botão de pesquisa
    if tp == 'search':
        pesquisar_btn = tk.Button(pesquisar_transacao_janela, text="Pesquisar", command=lambda:(pesquisarTransacao()))
        pesquisar_btn.pack(pady=10)
    elif tp == 'atualizar':
        atualizar_btn = tk.Button(pesquisar_transacao_janela, text="Atualizar", command=lambda:(pesquisar_transacao_janela.destroy(),abrir_formulario('up')))
        atualizar_btn.pack(pady=11)
    elif tp == 'Excluir':
        deletar_btn = tk.Button(pesquisar_transacao_janela, text="Exluir transação", command=lambda:(pesquisar_transacao_janela.destroy(),excluir_transacao()))
        deletar_btn.pack(pady=11)
        


# Abre o menu de exibição com as opções de vIsualização dos dados cadastrados
def abrir_menuExibicao():
    visualizar_janela = tk.Toplevel()
    visualizar_janela.geometry('1000x800')
    visualizar_janela.title("Visualizar")

    # adiciona botão para visualizar histórico
    historico_btn = tk.Button(visualizar_janela, text="Histórico", command=lambda: (visualizar_janela.destroy(), abrir_historico()))
    historico_btn.place(relx=0.5, rely=0.40, anchor='center')

    # adiciona botão para pesquisar ativo
    ativo_btn = tk.Button(visualizar_janela, text="Pesquisar Ativo", command=lambda: (abrir_pesquisar_ativo(), visualizar_janela.destroy()))
    ativo_btn.place(relx=0.5, rely=0.45, anchor='center')

    # adiciona botão para pesquisar transação
    transacao_btn = tk.Button(visualizar_janela, text="Pesquisar Transação", command=lambda:(visualizar_janela.destroy(),abrir_pesquisar_transacao('search')))
    transacao_btn.place(relx=0.5, rely=0.50, anchor='center')
    
    voltar_btn = tk.Button(visualizar_janela, text='Voltar', command=lambda:visualizar_janela.destroy())
    voltar_btn.place(relx=0.5, rely=0.55, anchor='center')
    
    visualizar_janela.mainloop()

def reiniciar():
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")

    # Cria um cursor(objeto) para manipular o BD
    cur = conn.cursor()
    
    cur.execute('''
    UPDATE ativo
    Set quantidade_acoes = 0, acoes_vendidas = 0, acoes_compradas = 0, preco_medio = 0, retorno = 0
                ''')
    
    cur.execute('DELETE from investimentos')
    
    conn.commit()
    
    cur.close()
    conn.close()
    messagebox.showinfo("Feito", "Tabelas reiniciadas com Sucesso!")
             

    
root = tk.Tk()
def main():
    # Abre a janela principal do programa
    root.geometry('900x750')
    root.title("Controle de ações")

    frame = tk.Frame(root)
    frame.pack(side='top', fill='both', expand=True)
    # Configura o botão cadastrar para abri a função abrir_formulario() 
    cadastrar_btn = tk.Button(frame, text="Cadastrar", command=lambda:(abrir_formulario('cd')))
    cadastrar_btn.place(relx=0.5, rely=0.35, anchor='center')

    update_btn = tk.Button(frame, text="Editar Transação", command=lambda:(abrir_pesquisar_transacao('atualizar')))
    update_btn.place(relx=0.5, rely=0.40, anchor='center')
    deletar_btn = tk.Button(frame, text="Deletar Transação", command=lambda:(abrir_pesquisar_transacao('Excluir')))
    deletar_btn.place(relx=0.5, rely=0.45, anchor='center')

    visualizar_btn = tk.Button(frame, text="Visualizar", command=lambda:(abrir_menuExibicao()))
    visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')
    
    visualizar_btn = tk.Button(frame, text="Reiniciar BD", command=lambda:(reiniciar(), atualizar_lucro_prejuizo()))
    visualizar_btn.place(relx=0.5, rely=0.55, anchor='center')
    
    fechar_btn = tk.Button(frame, text='Fechar', command=lambda:root.destroy())
    fechar_btn.place(relx=0.5, rely=0.60, anchor='center')
    
    global lucro_prejuizo_label
    lucro_prejuizo_label = tk.Label(frame, text="Retorno Total: R$ 0.0")
    lucro_prejuizo_label.pack(anchor=tk.NE)
    atualizar_lucro_prejuizo()

    # Chamada inicial para atualizar o lucro/prejuízo total

    root.mainloop()
    

if __name__ == '__main__':
    main()

