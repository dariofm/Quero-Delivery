
import requests
import os
import firebirdsql
import json
import decimal
from funcao import Tratamento
from datetime import datetime,date

data = Tratamento.RetornaData(datetime.now(),'.')   

os.system('cls')

conn = firebirdsql.connect(user="SYSDBA",password="masterkey",database='C:\\TSD\\Host\\HOST.FDB',host="127.0.0.1",charset="latin1")
cursor = conn.cursor()

cursor.execute(f"select BARRAS,ID_PRODUTO,PRODUTO,VALOR_VENDA from PRODUTOS where DT_CADASTRO =' {data}'")

for i in cursor.fetchall(): 
    Barras        = i[0]
    CodigoInterno = i[1]
    descricao     = i[2]
    preco         = i[3]
    
    print(type(Barras))