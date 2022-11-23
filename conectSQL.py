import psycopg2
from config import config
from tkinter import messagebox

def f_conexao():
    conn = None
    params = config()
    conn = psycopg2.connect(**params)

    return conn

def f_verifica(a):
    if(type(a) == type(str())):
        return 1
    else:
        return 0

def f_criarInstrucao(table_name, dic, pk):
    l = str()
    z = str()
    for g,j in dic.items():
        l += g + ","

        if(f_verifica(j) == 1):
            z += "'" + str(j) + "'" + ","
        else:
            z += str(j) + ","
         
    l = l[:len(l)-1]
    z = z[:len(z)-1]
    sql = f"""INSERT INTO {table_name}({l})
            VALUES({z}) RETURNING {pk};
            """
    return sql


def f_inserirDados(table_name, dic, pk):
    sql = f_criarInstrucao(table_name, dic, pk)

    conn = f_conexao()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return id
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return None

def f_retornaInfo(campos, nome_tabela,ordem):
    ca = str()
    for i in campos:
        ca += i + ","
    ca = ca[:len(ca)-1]

    sql = f""" SELECT {ca} FROM {nome_tabela} order by {ordem}"""
    conn = f_conexao()
    cur = conn.cursor()
    cur.execute(sql)

    recset = cur.fetchall()
    values = list()

    for rec in recset:
        values.append(rec)

    cur.close()
    conn.close()

    return values

def f_retornaEspc(campos, nome_tabela,username, campo_condi):
    ca = str()
    for i in campos:
        ca += i + ","
    ca = ca[:len(ca)-1]

    sql = f""" SELECT {ca} FROM {nome_tabela} WHERE {campo_condi} = '{username}'"""
    conn = f_conexao()
    cur = conn.cursor()
    cur.execute(sql)

    recset = cur.fetchall()
    values = list()

    for rec in recset:
        values.append(rec)

    cur.close()
    conn.close()

    return values

def f_retornar_info_compra(cod_compra):
    sql = f"""select pessoa.nome, pessoa.telefone, endereco.cep, endereco.logradouro, endereco.numero, endereco.complemento, bairro.descricao, cidade.descricao, tipo_logradouro.descricao
    from pessoa
    inner join endereco
    on endereco.codigo = pessoa.fk_endereco_codigo
    inner join bairro
    on bairro.codigo = endereco.bairro
    inner join cidade
    on cidade.codigo = endereco.cidade
    inner join tipo_logradouro
    on tipo_logradouro.codigo = endereco.tipo_logradouro
    inner join cliente
    on pessoa.username = cliente.fk_pessoa_username
    inner join cliente_compra
    on cliente.codigo = cliente_compra.fk_cliente_codigo
    inner join compra
    on compra.codigo = cliente_compra.fk_compra_codigo
    where compra.codigo = {cod_compra};"""

    conn = f_conexao()
    cur = conn.cursor()
    cur.execute(sql)

    recset = cur.fetchall()
    values = list()

    for rec in recset:
        values.append(rec)

    cur.close()
    conn.close()

    return(values)

def f_retornar_info_produto(cod_produto):
    sql = f"""select produto.nome, produto.valor, produto.descricao, tipo_produto.descricao
    from produto
    inner join tipo_produto
    on produto.FK_tipo_produto_tipo_produto_PK = tipo_produto.tipo_produto_PK
    where produto.nome = '{cod_produto}';"""

    conn = f_conexao()
    cur = conn.cursor()
    cur.execute(sql)

    recset = cur.fetchall()
    values = list()

    for rec in recset:
        values.append(rec)

    cur.close()
    conn.close()

    return(values)

def f_update_compra(cod, compra):
    sql = f"""update compra set fk_entregador_codigo = {cod} where codigo = {compra}"""
    conn = f_conexao()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""update compra set estado = 'Em entrega' where codigo = {compra}"""
    conn = f_conexao()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

def f_entregar_compra():
    sql = """select codigo from compra where estado = 'Realizado'"""
    conn = f_conexao()
    cur = conn.cursor()
    try:
        cur.execute(sql)
        conn.commit()
        recset = cur.fetchall()
        values = list()

        for rec in recset:
            values.append(rec)
        cur.close()
        conn.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
    return values

def f_excluir_cliente(username):
    conn = f_conexao()
    cur = conn.cursor()

    sql = f"""select codigo from cliente where fk_pessoa_username = '{username}'"""

    try:
        cur.execute(sql)
        conn.commit()
        cod_cliente = cur.fetchone()[0]
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""delete from cliente_compra where fk_cliente_codigo = {cod_cliente}"""
    try:
        cur.execute(sql)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""delete from cliente where fk_pessoa_username = '{username}'"""
    try:
        cur.execute(sql)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
    
    sql = f"""select fk_endereco_codigo from pessoa where username = '{username}'"""

    try:
        cur.execute(sql)
        conn.commit()
        cod_endereco = cur.fetchone()[0]
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""delete from pessoa where username = '{username}'"""
    try:
        cur.execute(sql)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""delete from endereco where codigo = {cod_endereco}"""
    try:
        cur.execute(sql)
        conn.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
    return 0

def f_redefinir_senha(user, cpf, nSenha, root):

    if(user == "" or len(user) > 25):
        messagebox.showinfo('USERNAME', 'Username ultrapassa 25 caracteres ou se encontra vazio!')
    elif(cpf == "" or len(user) > 14):
        messagebox.showinfo('CPF', 'CPF ultrapassa 14 caracteres ou se encontra vazio!')
    elif(nSenha == "" or len(nSenha) > 25):
        messagebox.showinfo('SENHA', 'Senha ultrapassa 25 caracteres ou se encontra vazio!')
    else:
        conn = f_conexao()
        cur = conn.cursor()

        sql = f"""update pessoa set senha = '{nSenha}' where username = '{user}' and cpf = '{cpf}';
        select senha from pessoa where username = '{user}';"""
        try:
            cur.execute(sql)
            conn.commit()
            #print(not(cur.fetchall() == []))
            aux = cur.fetchone()
            print(aux)
            if(aux == None):
                messagebox.showinfo('Senha não alterada', 'Sua senha não foi alterada')
            elif(aux[0] == ''):
                print("None")
                messagebox.showinfo('Senha não alterada', 'Sua senha não foi alterada')
            elif(aux[0] != nSenha):
                print('senha diferente')
                messagebox.showinfo('Senha não alterada', 'Sua senha não foi alterada')
            else:
                messagebox.showinfo('Senha alterada', 'Sua senha foi alterada com sucesso!!')
                root.destroy()

        except(Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cur.close()
        
        
    return 0

def f_redefinir_produto(nome,valor,texto_descricao,codigo,new):
    conn = f_conexao()
    cur = conn.cursor()

    sql = f"""update produto set nome = '{nome}' where codigo = {codigo};"""
    try:
        cur.execute(sql)
        conn.commit()
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""update produto set descricao = '{texto_descricao}' where codigo = {codigo};"""
    try:
        cur.execute(sql)
        conn.commit()
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
    
    sql = f"""update produto set valor = {valor} where codigo = {codigo};"""
    try:
        cur.execute(sql)
        conn.commit()
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    sql = f"""update produto set FK_tipo_produto_tipo_produto_PK = {new} where codigo = {codigo};"""
    try:
        cur.execute(sql)
        conn.commit()
            
    except(Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()

    return 0
    
