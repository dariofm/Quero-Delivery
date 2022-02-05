
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
urlbase          = caminho.URL_SITE
head_c           = caminho.HEAD
categoriaId        = caminho.CATEGORIA
data             = Tratamento.RetornaData(datetime.now(),'.')   




conn = firebirdsql.connect(user="SYSDBA",password="masterkey",database=hostDataBase,host=deliveryServidor,charset="latin1")
cursor = conn.cursor()

conn_delivery = firebirdsql.connect(user="SYSDBA",password="masterkey",database=deliveryDataBase,host=deliveryServidor,charset="latin1")
cursor_delivery = conn_delivery.cursor()

class ApiDelivery:
    def __init__(self):
        self.placeId = placeId
        self.h = {'authorization':head_c}
    
    def recuperaGrupo(self):
        cursor.execute('select ID_PRODUTO,BARRAS,PRODUTO from PRODUTOS')

        for i in cursor.fetchall():
            codigoInterno = i[0]
            barras        = i[1]
            descricao     = i[2]
   

            url = f'{urlbase}/produto?placeId={self.placeId}&codigoBarras={barras}'

            r = requests.get(url=url,headers=self.h).json()
     
            try:
                idCategoria = r["data"]["produtoCategoriaId"]
            except:
                idCategoria = ''
            url = f'{urlbase}/categoria/search?placeId={self.placeId}&categoriaId={idCategoria}'

            rCat = requests.get(url=url,headers=self.h).json()  
            try:  
                CodigoID = TratamentoBanco.retornaGrupoIdQuero(rCat["data"]["nome"])
                
            except:
                CodigoID = ''
                pass    
       
            try:
                cursor.execute(f"update PRODUTOS set GRUPO  = '{CodigoID}' where ID_PRODUTO = '{codigoInterno}'")
                conn.commit()
                print(f'Recuperando Grupo: {CodigoID} do Produto: {descricao}')
            except firebirdsql.OperationalError as erro:
                pass
  




    def cadastrarProduto(self):
        url = f'{urlbase}/produto?placeId={self.placeId}'
        
        cursor.execute(f"select BARRAS,ID_PRODUTO,PRODUTO,VALOR_VENDA,GRUPO from PRODUTOS where DT_CADASTRO ='{data}' AND SECAO IS NULL")
     
        for i in cursor.fetchall(): 
            Barras        = i[0]
            CodigoInterno = i[1]
            descricao     = i[2]
            preco         = i[3]
        
            Produto = {
                "codigoInterno":str(CodigoInterno),
                "codigoBarras":Barras,
                "nome": descricao,
                "categoriaId": categoriaId,#"619f66d6f1f55a001dc05e6a",
                "status": "ATIVO",
                "preco": float(preco),
                "precoAntigo": 0,
                "isPesavel": False,
                "isPromocao":False,
                "isSazonal": False,
                "imagem": {
                "publicId": "querodelivery/default/avatar-nova-marca",
                "src": "http://res.cloudinary.com/neetocode/querodelivery/default/avatar-nova-marca.png",
                "version": "1576609571"
                        }
                } 
            if Barras == None or Barras == '' :
                Produto.pop('codigoBarras')
                print('Sem Barras')
        
            print(requests.post(url=url,headers=self.h,json=Produto).json())
            print(f'Cadastrando Novo Produtos: {descricao}')
            
            cursor.execute(f"update PRODUTOS set SECAO = 'QD' where ID_PRODUTO = '{CodigoInterno}'")
            conn.commit()
        
        #Lançando Quantidade
        cursor.execute(f"select ESTOQUE from PRODUTOS where DT_CADASTRO ='{data}' and SECAO = 'QD'")    
        for i in cursor.fetchall():    
            qtd = i[0]
            url_b = f'{urlbase}/produto/lancar-estoque?placeId={self.placeId}&codigoInterno={CodigoInterno}'
            Produto = {
                "quantidade": float(qtd)
            }

            cursor.execute(f"update PRODUTOS set SECAO = 'QUERODELIVERY' where ID_PRODUTO = '{CodigoInterno}' AND SECAO = 'QD'")
            conn.commit()
        
            print(requests.put(url=url_b,headers=self.h,json=Produto).json())
            print(f'AlteraEstoqueQueroDelivery: {qtd}') 



    def cadastrarGeralProduto(self):
        url = f'{urlbase}/produto?placeId={self.placeId}'
        
        cursor.execute(f"select BARRAS,ID_PRODUTO,PRODUTO,VALOR_VENDA,GRUPO,QUANTIDADE from PRODUTOS")
     
        for i in cursor.fetchall(): 
            Barras        = i[0]
            CodigoInterno = i[1]
            descricao     = i[2]
            preco         = i[3]
            grupo         = i[4]
            qtd           = i[5]
        
            Produto = {
                "codigoInterno":str(CodigoInterno),
                "codigoBarras":Barras,
                "nome": descricao,
                "categoriaId": categoriaId,
                "status": "ATIVO",
                "preco": float(preco),
                "precoAntigo": 0,
                "isPesavel": False,
                "isPromocao":False,
                "isSazonal": False,
                "imagem": {
                "publicId": "querodelivery/default/avatar-nova-marca",
                "src": "http://res.cloudinary.com/neetocode/querodelivery/default/avatar-nova-marca.png",
                "version": "1576609571"
                        }
                } 
            if Barras == None or Barras == '' :
                Produto.pop('codigoBarras')
                print('Sem Barras')
        
            requests.post(url=url,headers=self.h,json=Produto).json()
            print(f'Cadastrando Novo Produtos: {descricao}')
            
            

   
    def alteraPreco(self):
        cursor.execute(f"select ID_PRODUTO,BARRAS,VALOR_VENDA,PRODUTO from DELIVERY_PRODUTOS where DT_MOVIMENTO = '{data}' AND STATUS = 0")
       
        for i in cursor.fetchall(): 
            CodigoInterno  = i[0]
            barras         = i[1]  
            preco          = i[2] 
            descricao      = i[3]
            
            Produto = {
                        "preco": float(preco),
                        "precoAntigo":0
                    }

            if  barras == None or barras == '':       
                url = f'{urlbase}/produto/preco/?placeId={self.placeId}&codigoInterno={CodigoInterno}'
                requests.put(url=url,headers=self.h,json=Produto).json()
                
            if  barras != None or barras != '':       
                url = f'{urlbase}/produto/preco/?placeId={self.placeId}&codigoBarras={barras}'  
                requests.put(url=url,headers=self.h,json=Produto).json()
            
            #Ao Finalizar de Alterar os Produtos é altualizado o Status da Tabela DELIVERY_PRODUTOS   
            cursor.execute(f"update DELIVERY_PRODUTOS set STATUS = 1 where ID_PRODUTO = '{CodigoInterno}'")   
            conn.commit() 
            print(f'Alterando Produtos: {descricao}')
    
    def AlteraEstoqueQueroDelivery(self,id_produto,estoque):
        url = f'{urlbase}/produto/lancar-estoque?placeId={self.placeId}&codigoInterno={id_produto}'
        
        Produto = {
            "quantidade": float(estoque)
        }
        

        requests.put(url=url,headers=self.h,json=Produto).json()
        print(f'AlteraEstoqueQueroDelivery: {estoque}')             
        
    def InativoProdutosZerados(self,id_produto):
        url = f'{urlbase}/produto/status?placeId={self.placeId}&codigoInterno={id_produto}'
        
        inativa = {
            "status":"EM_FALTA"
        }
        
        requests.put(url=url,headers=self.h,json=inativa).json()
        print(f'AlteraEstoqueQueroDelivery: {id_produto}')              

    def AtivaProdutosZerados(self,id_produto):
        url = f'{urlbase}/produto/status?placeId={self.placeId}&codigoInterno={id_produto}'
        
        inativa = {
            "status":"ATIVO"
        }
        
        requests.put(url=url,headers=self.h,json=inativa).json()
        print(f'AlteraEstoqueQueroDelivery: {id_produto}')              
                                            
        


    def listarCategoria(self):
        url = f'{urlbase}/categoria/?placeId={self.placeId}&limit=50'

        resposta = requests.get(url=url,headers=self.h)
        print(resposta.json())
        i = 1

        for x in range(i):
            try:
                idCategoria     = resposta.json()["data"]["result"][x]["_id"]
                nomeCategoria   = resposta.json()["data"]["result"][x]["nome"]
                statusCategoria = resposta.json()["data"]["result"][x]["isAtivo"]
                idGrupo         = Tratamento.ProximoID('GEN_PRODUTOS_GRUPO')
            except IndexError as erro:
                print(f'Erro de Array: {erro}')
                exit()
                    
      
            try:
                cursor_delivery.execute(f"insert into CATEGORIA (ID,DESCRICAO,ATIVO) values ('{idCategoria}','{nomeCategoria}','{statusCategoria}')")
                conn_delivery.commit()
                

            except firebirdsql.IntegrityError as erro:
                nomeCategoria = nomeCategoria[0:19]
                
                cursor_delivery.execute(f"Update CATEGORIA set DESCRICAO = '{nomeCategoria}',ATIVO = '{statusCategoria}' where ID = '{idCategoria}'")
                conn_delivery.commit()     
                pass
             

"""
delivery = ApiDelivery()




#chamando listagem de categorias
cursor_delivery.execute('select CATEGORIA from CHAMADA where CATEGORIA = 1')
for categoria in cursor_delivery.fetchall():
    delivery.listarCategoria()
    
    cursor_delivery.execute(f"Update CHAMADA set CATEGORIA = 0")
    conn_delivery.commit()  

#chamando Recuperação de Categoria
cursor_delivery.execute('select REC_CATEGORIA from CHAMADA where REC_CATEGORIA = 1')
for categoria in cursor_delivery.fetchall():
    delivery.recuperaGrupo()

    cursor_delivery.execute(f"Update CHAMADA set REC_CATEGORIA = 0")
    conn_delivery.commit()  

#chamando Cadastro de Novo Produto         
cursor_delivery.execute('select NOVO_PRODUTO from CHAMADA where NOVO_PRODUTO = 1')
for categoria in cursor_delivery.fetchall():
    delivery.cadastrarProduto()
    
    cursor_delivery.execute(f"Update CHAMADA set NOVO_PRODUTO = 0")
    conn_delivery.commit() 
    
cursor_delivery.execute('select CARGA_GERAL from CHAMADA where CARGA_GERAL = 1')
for categoria in cursor_delivery.fetchall():
    delivery.cadastrarGeralProduto()
    
    cursor_delivery.execute(f"Update CHAMADA set CARGA_GERAL = 0")
    conn_delivery.commit() 

#chamando Alteração de Produto
cursor_delivery.execute('select EDITA_PRODUTO from CHAMADA where EDITA_PRODUTO = 1')
for categoria in cursor_delivery.fetchall():
    delivery.alteraPreco()
    
    cursor_delivery.execute(f"Update CHAMADA set EDITA_PRODUTO = 0")
    conn_delivery.commit() 

"""    