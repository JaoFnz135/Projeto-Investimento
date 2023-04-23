import tkinter as tk
from tkinter import messagebox
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

    # Gera um código aleatório de 8 caracteres
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
    
    # Faz as variaveis abaixo receberem os valores das variaveis globais
    codigo_transacao = gerar_codigo()
   
    up.uses_netloc.append("postgres")
    conn = psycopg2.connect(database="mnlfnrwe", 
                                user="mnlfnrwe", 
                                password="RnSYVKvtLjKAF5SqXPJlll0AuNveFDO_", 
                                host="kesavan.db.elephantsql.com", 
                                port="5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO investimentos VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (codigo_transacao, codigo_entry.get(), data_entry.get(), quantidade_entry.get(), valor_entry.get(), taxa_entry.get(), tipo_operacao_var.get(), 100.00, 0.90, 2000.00))
    
    conn.commit()
    cur.close()
    conn.close()

    # Crie uma instância da classe investimentos com os dados do formulário
    #investimento = investimentos(codigo_transacao, codigo, data, quantidade, valor_unit, taxa_corretagem)

    # Verifique o tipo de operação selecionado e chame o método apropriado
    #if tipo_operacao == "Compra":
        #investimento.comprar()
    #else:
        #investimento.vender()

    # Salve os dados no banco de dados
    #investimento.salvarDados()

    # Feche o formulário
    formulario.destroy()
    messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")


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

    tk.Label(container, text="Código:").grid(row=0, column=0)
    codigo_entry = tk.Entry(container, width=10)
    codigo_entry.grid(row=0, column=1)

    tk.Label(container, text="Data:").grid(row=1, column=0)
    data_entry = tk.Entry(container, width=10)
    data_entry.grid(row=1, column=1)

    tk.Label(container, text="Quantidade:").grid(row=2, column=0)
    quantidade_entry = tk.Entry(container, width=10)
    quantidade_entry.grid(row=2, column=1)

    tk.Label(container, text="Valor da unidade:").grid(row=3, column=0)
    valor_entry = tk.Entry(container, width=10)
    valor_entry.grid(row=3, column=1)

    tk.Label(container, text="Tipo de operação:").grid(row=4, column=0)
    tipo_operacao_var = tk.StringVar(value="Compra")
    tipo_operacao_radio_compra = tk.Radiobutton(container, text="Compra", variable=tipo_operacao_var, value="Compra")
    tipo_operacao_radio_compra.grid(row=4, column=2, sticky=tk.W)
    tipo_operacao_radio_venda = tk.Radiobutton(container, text="Venda", variable=tipo_operacao_var, value="Venda")
    tipo_operacao_radio_venda.grid(row=4, column=1, sticky=tk.E)

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

    visualizar_btn = tk.Button(frame, text="Visualizar")
    visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')

    root.mainloop()
    
if __name__ == '__main__':
    main()
