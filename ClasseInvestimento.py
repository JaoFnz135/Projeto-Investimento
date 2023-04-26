import urllib.parse as up
import psycopg2
from decimal import *
from datetime import *
import tkinter as tk
from tkinter import messagebox
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
