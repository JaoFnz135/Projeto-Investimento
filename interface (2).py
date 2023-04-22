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

root = tk.Tk()
root.geometry('600x600')  # define as dimensões da janela

frame = tk.Frame(root)
frame.pack(side='top', fill='both', expand=True)

# cria o botão "Cadastrar" e centraliza na janela
cadastrar_btn = tk.Button(frame, text="Cadastrar", command=abrir_formulario)
cadastrar_btn.place(relx=0.5, rely=0.45, anchor='center')

# cria o botão "Visualizar" e centraliza na janela
visualizar_btn = tk.Button(frame, text="Visualizar")
visualizar_btn.place(relx=0.5, rely=0.5, anchor='center')


root.mainloop()
