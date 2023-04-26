import urllib.parse as up
import psycopg2
from decimal import *
from datetime import *
import tkinter as tk
from tkinter import messagebox
import random
import string

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
    # 
    inv = investimentos(codigo_transacao, codigo_entry.get(), data_entry.get(), quantidade_entry.get(), valor_unit, taxa_corretagem, tipo_op)
    
    if tipo_op == 'Compra':
        inv.compra()
    else:
        inv.venda()
        
    # Salva os dados no banco de dados    
    inv.salvarDados()

    # Feche o formulário
    formulario.destroy()
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")

# Aperfeiçoar
def visualizar_dados():
    conn = psycopg2.connect(database="mnlfnrwe", 
                            user="mnlfnrwe", 
                            password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                            host="kesavan.db.elephantsql.com", 
                            port="5432")
    # Cria um cursor(objeto) para manipular o BD
    cur = conn.cursor()
    # O método .execute("[Codigo SQL]") manipula o BD
    cur.execute("SELECT * FROM investimentos")
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
            dado_label = tk.Label(tabela_janela, text=str(dados[i][j]), font=("Helvetica", 12))
            dado_label.grid(row=i+2, column=j, padx=10, pady=5)
            
            
    # Encerra a conexão com o banco de dados
    cur.close()
    conn.close()

    tabela_janela.mainloop()


def abrir_formulario():
    global formulario
    global codigo_entry
    global data_entry
    global quantidade_entry
    global valor_entry
    global tipo_operacao_var
    global taxa_entry

    formulario = tk.Toplevel(root)
    formulario.geometry('1920x1080')
    formulario.title("Formulário")

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
    
root = tk.Tk()
def main():
    # Abre a janela principal do programa
    root.geometry('1920x1080')
    root.title("Programinha")

    frame = tk.Frame(root)
    frame.pack(side='top', fill='both', expand=True)
    # Configura o botão cadastrar para abri a função abrir_formulario() 
    cadastrar_btn = tk.Button(frame, text="Cadastrar", command=abrir_formulario)
    cadastrar_btn.place(relx=0.5, rely=0.45, anchor='center')

    visualizar_btn = tk.Button(frame, text="Visualizar", command=visualizar_dados)
    visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')

    root.mainloop()
    
if __name__ == '__main__':
    main()
