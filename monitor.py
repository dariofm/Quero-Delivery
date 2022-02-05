
import firebirdsql
import caminho
import delivery


deliveryServidor = caminho.SERVIDOR_DELIVERY
hostDataBase     = caminho.SERVIDOR_HOST
deliveryDataBase = caminho.SERVIDOR_CAMINHO

qd = delivery.ApiDelivery()


conn = firebirdsql.connect(user="SYSDBA",password="masterkey",database=hostDataBase,host=deliveryServidor,charset="latin1")
cursor = conn.cursor()

conn_delivery = firebirdsql.connect(user="SYSDBA",password="masterkey",database=deliveryDataBase,host=deliveryServidor,charset="latin1")
cursor_delivery = conn_delivery.cursor()

def RetornaUltimoProduto():
    cursor.execute('select max(id_produto) from produtos')
    for i in cursor.fetchall():
        return i[0]    
    
    
def RetornaCount(Gen):

    cursor.execute(f'select gen_id({Gen},0) FROM RDB$DATABASE')
    nDav = cursor.fetchall()[0][0]
    
    cursor.execute(f"select ID from DAV where ID = {nDav}  and STATUS_VENDA = 'F'")
    for i in cursor.fetchall():
        return i[0]

def RetornaCountCompra(Gen):
    
    cursor.execute(f'select gen_id({Gen},0) FROM RDB$DATABASE')
    nCompra = cursor.fetchall()[0][0]
    
    cursor.execute(f"select ID from NOTA_COMPRA where ID = {nCompra}  and NFE_STATUS = 'Concluido'")
    for i in cursor.fetchall():
        return i[0]

    

def RetornaCountCancelados():
    cursor.execute("select count(*) from DAV where DAV.CUPOM_CANCELADO = 'S'")
    return cursor.fetchall()[0][0]    

def RetornaEstoque(Codigo):
    cursor.execute(f"select ESTOQUE from produtos where id_produto = '{Codigo}'")
    print(f'Produto: {Codigo}')
    try:
        estoque = cursor.fetchall()[0][0]
    except:
        estoque = 0
    return estoque   
        


ultimoDav     = RetornaCount('DAV_GEN')
#ultimoCompras = RetornaCountCompra('NOTA_COMPRA_GEN')
cupomCan      = RetornaCountCancelados()
ultimoProduto = RetornaUltimoProduto()
print('Monitorando...')
while True:
    if ultimoProduto != RetornaUltimoProduto():
        qd.cadastrarProduto()
        print(f'funcao: cadastrarProduto')  

        ultimoProduto = RetornaUltimoProduto()

    #Verifica as Saídas Compras
    """"
    if ultimoCompras != RetornaCountCompra('NOTA_COMPRA_GEN') and RetornaCountCompra('NOTA_COMPRA_GEN') != None:
        print(f"Nova Compra Detectada: {RetornaCountCompra('NOTA_COMPRA_GEN')}")
        cursor.execute(f"select ID_PRODUTO,QUANTIDADE from NOTA_COMPRA_DETALHE where ID_NFE = '{RetornaCountCompra('NOTA_COMPRA_GEN')}' and ID_PRODUTO <> '0'")
        
        for p in cursor.fetchall():
            Codigo     = p[0]
            Quantidade = p[1]
            print(p)
            qd.AlteraEstoqueQueroDelivery(Codigo,RetornaEstoque(Codigo))
            if RetornaEstoque(Codigo) > 0:
                qd.AtivaProdutosZerados(Codigo)    
                pass
        ultimoCompras = RetornaCountCompra('NOTA_COMPRA_GEN')    
        print('Monitorando...')    
    """
    #Verifica as Saídas DAV
    if ultimoDav != RetornaCount('DAV_GEN') and RetornaCount('DAV_GEN') != None:
        print(f"Nova Venda Detectada: {RetornaCount('DAV_GEN')}")
        cursor.execute(f"select ID_PRODUTO,QUANTIDADE from DAV_ITENS where ID_DAV = '{RetornaCount('DAV_GEN')}' and CANCELADO = 'N'")
        for p in cursor.fetchall():
            Codigo     = p[0]
            Quantidade = p[1]
            qd.AlteraEstoqueQueroDelivery(Codigo,RetornaEstoque(Codigo))
            if RetornaEstoque(Codigo) <= 0:
                qd.InativoProdutosZerados(Codigo)    
                pass
        ultimoDav = RetornaCount('DAV_GEN')    
        print('Monitorando...')
        
    #Verifica Dav cancelado
    if cupomCan != RetornaCountCancelados():
        try:
            cursor.execute(f"select ID from DAV where DAV.DATA_CANCELAMENTO = current_date")
            for c in cursor.fetchall():
                DavNumero = c[0]
                cursor.execute(f"select ID_PRODUTO,QUANTIDADE from DAV_ITENS where ID_DAV = {DavNumero} and CANCELADO = 'S'")
                for p in cursor.fetchall():
                    Codigo     = p[0]
                    Quantidade = p[1]
                    qd.AlteraEstoqueQueroDelivery(Codigo,RetornaEstoque(Codigo))
                    if Quantidade <= 0:
                        qd.InativoProdutosZerados(Codigo)    
                        pass            
                pass
        finally:
            print(f'Novo Cancelamento Detectado: {RetornaCountCancelados()}')

            cupomCan = RetornaCountCancelados()    
            print('Monitorando...')
        



    #chamando listagem de categorias
    cursor_delivery.execute('select CATEGORIA from CHAMADA where CATEGORIA = 1')
    for categoria in cursor_delivery.fetchall():
        qd.listarCategoria()
        print(f'funcao: listarCategoria')
        
        cursor_delivery.execute(f"Update CHAMADA set CATEGORIA = 0")
        conn_delivery.commit()  

    #chamando Recuperação de Categoria
    cursor_delivery.execute('select REC_CATEGORIA from CHAMADA where REC_CATEGORIA = 1')
    for categoria in cursor_delivery.fetchall():
        qd.recuperaGrupo()
        print(f'funcao: recuperaGrupo')

        cursor_delivery.execute(f"Update CHAMADA set REC_CATEGORIA = 0")
        conn_delivery.commit()  

    #chamando Cadastro de Novo Produto         
    cursor_delivery.execute('select NOVO_PRODUTO from CHAMADA where NOVO_PRODUTO = 1')
    for categoria in cursor_delivery.fetchall():
        qd.cadastrarProduto()
        print(f'funcao: cadastrarProduto')
        
        cursor_delivery.execute(f"Update CHAMADA set NOVO_PRODUTO = 0")
        conn_delivery.commit() 
        
    cursor_delivery.execute('select CARGA_GERAL from CHAMADA where CARGA_GERAL = 1')
    for categoria in cursor_delivery.fetchall():
        qd.cadastrarGeralProduto()
        print(f'funcao: cadastrarGeralProduto')
        
        cursor_delivery.execute(f"Update CHAMADA set CARGA_GERAL = 0")
        conn_delivery.commit() 

    #chamando Alteração de Produto
    cursor_delivery.execute('select EDITA_PRODUTO from CHAMADA where EDITA_PRODUTO = 1')
    for categoria in cursor_delivery.fetchall():
        qd.alteraPreco()
        print(f'funcao: alteraPreco')
        
        cursor_delivery.execute(f"Update CHAMADA set EDITA_PRODUTO = 0")
        conn_delivery.commit() 

            