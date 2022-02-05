
import requests
import os
import firebirdsql
from funcao import Tratamento, TratamentoBanco
from datetime import datetime
import caminho


deliveryServidor = caminho.SERVIDOR_DELIVERY
deliveryDataBase = caminho.SERVIDOR_CAMINHO
hostDataBase     = caminho.SERVIDOR_HOST
placeId          = caminho.PLACE_ID   
urlbase          = 'https://stageapi.quero.io'
head_c           = caminho.HEAD
data             = Tratamento.RetornaData(datetime.now(),'.')   




conn = firebirdsql.connect(user="SYSDBA",password="masterkey",database=hostDataBase,host=deliveryServidor,charset="latin1")
cursor = conn.cursor()

conn_delivery = firebirdsql.connect(user="SYSDBA",password="masterkey",database=deliveryDataBase,host=deliveryServidor,charset="latin1")
cursor_delivery = conn_delivery.cursor()

h = {'authorization':'Basic NWRmYjZmZWQwMDNhODgwMDcwYjBlMDg5OiA1ZGZiNmZlZDAwM2E4ODAwNzBiMGUwODk='}
url = f'{urlbase}/categoria?placeId={placeId}'


print(requests.get(url=url,headers=h).json())