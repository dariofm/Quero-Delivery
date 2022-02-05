from datetime import datetime,date
import firebirdsql
import caminho

deliveryServidor = caminho.SERVIDOR_DELIVERY
deliveryDataBase = caminho.SERVIDOR_CAMINHO
hostDataBase     = caminho.SERVIDOR_HOST

conn = firebirdsql.connect(user="SYSDBA",password="masterkey",database=hostDataBase,host=deliveryServidor,charset="latin1")
cursor = conn.cursor()

conn_delivery = firebirdsql.connect(user="SYSDBA",password="masterkey",database=deliveryDataBase,host=deliveryServidor,charset="latin1")
cursor_delivery = conn_delivery.cursor()

class Tratamento:
    def __init__(self, *args):
        pass

    def ProximoID(gen):
        cursor.execute(f'select gen_id({gen},1) FROM RDB$DATABASE')
        for i in cursor.fetchall():
            return i[0]

    def RetornaData(dataEntrada,simbolo):
        data = str(dataEntrada)
        ano = data[0:4]
        mes = data[5:7]
        dia = data[8:10]

        return dia +simbolo+mes+simbolo+ano
    
    
class TratamentoBanco:
    def __init__(self):
        pass
    def retornaGrupoId(Grupo):
        cursor.execute(f"select GRUPO from PRODUTOS_GRUPO where id = {Grupo}")
        for b in cursor.fetchall():
            Descricao_Grupo = b[0]
            
            cursor_delivery.execute(f"select * from CATEGORIA where DESCRICAO = '{Descricao_Grupo}'")
            
            for i in cursor_delivery.fetchall():
                return i[0]


    def retornaGrupoIdQuero(Grupo):

        cursor_delivery.execute(f"select DESCRICAO from CATEGORIA where DESCRICAO = '{Grupo}'")
        for b in cursor_delivery.fetchall():
            Descricao_Grupo = b[0]
 
            cursor.execute(f"select ID from PRODUTOS_GRUPO where GRUPO = '{Descricao_Grupo}'")
            for i in cursor.fetchall():
                return i[0]
                  


