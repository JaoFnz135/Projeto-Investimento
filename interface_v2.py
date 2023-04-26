import tkinter as tk

def abrir_formulario():
    formulario = tk.Toplevel(root)
    formulario.title("Formulário")
    # cria os campos do formulário e adiciona na janela "formulario"
    # ...
    tk.Label(formulario, text="Código:").grid(row=0, column=0)
    codigo_entry = tk.Entry(formulario, width=10)
    codigo_entry.grid(row=0, column=1)
    
    tk.Label(formulario, text="Data:").grid(row=1, column=0)
    data_entry = tk.Entry(formulario, width=10)
    data_entry.grid(row=1, column=1)
    
    tk.Label(formulario, text="Quantidade:").grid(row=2, column=0)
    quantidade_entry = tk.Entry(formulario, width=10)
    quantidade_entry.grid(row=2, column=1)
    
    tk.Label(formulario, text="Valor da unidade:").grid(row=3, column=0)
    valor_entry = tk.Entry(formulario, width=10)
    valor_entry.grid(row=3, column=1)
    
    tk.Label(formulario, text="Tipo de operação:").grid(row=4, column=0)
    tipo_operacao_var = tk.StringVar(value="Compra")
    tipo_operacao_radio_compra = tk.Radiobutton(formulario, text="Compra", variable=tipo_operacao_var, value="Compra")
    tipo_operacao_radio_compra.grid(row=4, column=2, sticky=tk.W)
    tipo_operacao_radio_venda = tk.Radiobutton(formulario, text="Venda", variable=tipo_operacao_var, value="Venda")
    tipo_operacao_radio_venda.grid(row=4, column=1, sticky=tk.E)
    
    tk.Label(formulario, text="Taxa de corretagem:").grid(row=5, column=0)
    taxa_entry = tk.Entry(formulario, width=10)
    taxa_entry.grid(row=5, column=1)
    
    # adiciona o botão "Cadastrar" no formulário
    cadastrar_btn = tk.Button(formulario, text="Finalizar")
    cadastrar_btn.grid(row=6, column=0, columnspan=2, pady=10)



def abrir_historico():
    historico_janela = tk.Toplevel(root)
    historico_janela.title("Histórico")

    # adiciona um rótulo com o texto "Histórico"
    historico_lbl = tk.Label(historico_janela, text="Histórico")
    historico_lbl.pack(pady=10)

def abrir_pesquisar_ativo():
    pesquisar_ativo_janela = tk.Toplevel(root)
    pesquisar_ativo_janela.title("Pesquisar Ativo")

    # adiciona uma caixa de texto para inserir o nome do ativo
    ativo_entry = tk.Entry(pesquisar_ativo_janela)
    ativo_entry.pack(pady=10)

    # adiciona um botão de pesquisa
    pesquisar_btn = tk.Button(pesquisar_ativo_janela, text="Pesquisar")
    pesquisar_btn.pack(pady=10)

def abrir_pesquisar_transacao():
    pesquisar_transacao_janela = tk.Toplevel(root)
    pesquisar_transacao_janela.title("Pesquisar Transação")

    # adiciona uma caixa de texto para inserir o número da transação
    transacao_entry = tk.Entry(pesquisar_transacao_janela)
    transacao_entry.pack(pady=10)

    # adiciona um botão de pesquisa
    pesquisar_btn = tk.Button(pesquisar_transacao_janela, text="Pesquisar")
    pesquisar_btn.pack(pady=10)


def abrir_visualizar():
    visualizar_janela = tk.Toplevel(root)
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
root.geometry('600x600')  # define as dimensões da janela

frame = tk.Frame(root)
frame.pack(side='top', fill='both', expand=True)

# cria o botão "Cadastrar" e centraliza na janela
cadastrar_btn = tk.Button(frame, text="Cadastrar", command=abrir_formulario)
cadastrar_btn.place(relx=0.5, rely=0.45, anchor='center')

# cria o botão "Visualizar" e centraliza na janela
visualizar_btn = tk.Button(frame, text="Visualizar", command=abrir_visualizar)
visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')


root.mainloop()
