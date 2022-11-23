from conectSQL import *
from datetime import *
from tkinter import *

def f_cadastrar_pessoas(nome,cpf,tel,username,senha,logradouro,numero,cep,boxtl,boxcidade,boxbairro,complemento, tpPessoa, root, teste):
    
    try:
        int(numero)
    except ValueError:
        messagebox.showinfo('NÚMERO', 'Por favor,\ndigite apenas números para o campo "NÚMERO"')
    except TypeError:
        messagebox.showinfo('NÚMERO', 'Por favor,\ndigite números para o campo "NÚMERO"')

    if(logradouro == '' or len(logradouro) > 100):
        messagebox.showinfo('LOGRADOURO', 'O logradouro ultrapassa 100 caracteres ou se encontra vazio!!')
    elif(cep == '' or len(cep) > 9):
        messagebox.showinfo('CEP', 'O cep ultrapassa 9 caracteres ou se encontra vazio!!')
    elif(complemento == '' or len(complemento) > 100):
        messagebox.showinfo('COMPLEMENTO', 'O complemento ultrapassa 100 caracteres ou se encontra vazio!!')
    else:
        dicp = {}
        dicp["username"] = username
        dicp["nome"] = nome
        dicp["telefone"] = tel
        dicp["cpf"] = cpf
        dicp["senha"] = senha
        dicp["fk_endereco_codigo"] = f_cadastrar_endereco(cep,logradouro,numero,boxbairro,boxcidade,boxtl,complemento, teste)
        f_inserirDados("PESSOA",dicp,"username")

        if(tpPessoa == 0):
            dicC = {}
            dicC["fk_pessoa_username"] = username
            f_inserirDados("FUNCIONARIO", dicC, "codigo")

        elif(tpPessoa == 1):
            dicC = {}
            dicC["fk_pessoa_username"] = username
            f_inserirDados("ENTREGADOR", dicC, "codigo")

        elif(tpPessoa == 2):
            dicC = {}
            dicC["fk_pessoa_username"] = username
            f_inserirDados("CLIENTE", dicC, "codigo")
        root.destroy()
        return 0

def f_cadastrar_endereco(cep,logradouro,numero,boxbairro,boxcidade,boxtl,complemento, teste):
    dice = {}
    dice["cep"] = cep
    dice["logradouro"] = logradouro
    dice["numero"] = numero
    if(teste[2] == 0):
        dice["bairro"] = f_cadastrar_bairro(boxbairro)
    else:
        dice["bairro"] = teste[2]

    if(teste[1] == 0):
        dice["cidade"] = f_cadastrar_cidade(boxcidade)
    else:
        dice["cidade"] = teste[1]

    if(teste[0] == 0):
        dice["tipo_logradouro"] = f_cadastrar_tl(boxtl)
    else:
        dice["tipo_logradouro"] = teste[0]
        
    dice["complemento"] = complemento


    return f_inserirDados("endereco",dice,"codigo")

def f_cadastrar_bairro(boxbairro):
    dicb = {}
    dicb["descricao"] = boxbairro
  
    return str(f_inserirDados("BAIRRO",dicb,"codigo"))

def f_cadastrar_cidade(boxcidade):
    dicc = {}
    dicc["descricao"] = boxcidade
    
    return str(f_inserirDados("CIDADE",dicc,"codigo"))

def f_cadastrar_tl(boxtl):
    dictl = {}
    dictl["descricao"] = boxtl
    
    return str(f_inserirDados("TIPO_LOGRADOURO",dictl,"codigo"))
    
    
def f_cadastrar_produto(nome,tpProduto, valor, descricao, new, cod_func):
    try:
        float(valor)
    except ValueError:
        messagebox.showinfo('VALOR', 'Digite um valor válido!!')
    except TypeError:
        messagebox.showinfo('Valor', 'Digite um valor válido!!')

    if(nome == "" or len(nome) > 80):
        messagebox.showinfo('NOME', 'O nome ultrapassa 80 caracteres ou se encontra vazio!!')
    elif(descricao == "" or len(descricao) > 255):
        messagebox.showinfo('DESCRICAO', 'O descricao ultrapassa 255 caracteres ou se encontra vazio!!')
    else:
        dicP = {}
        dicP["nome"] = nome
        dicP["descricao"] = descricao
        dicP["valor"] = valor
        if(new == 0):
            dicP["fk_tipo_produto_tipo_produto_pk"] = f_cadastar_tpProduto(tpProduto)
        else:
            dicP["fk_tipo_produto_tipo_produto_pk"] = new

        cod_produto = f_inserirDados("PRODUTO", dicP, "codigo")

        dicAdm = {}
        dicAdm['fk_funcionario_codigo'] = cod_func
        dicAdm['fk_produto_codigo'] = cod_produto

        f_inserirDados("ADMINISTRA", dicAdm, "fk_produto_codigo")



def f_cadastar_tpProduto(tpProduto):
	dicTp = {}
	dicTp["descricao"] = tpProduto

	return f_inserirDados("TIPO_PRODUTO", dicTp, "tipo_produto_pk")

def f_cadastar_compra(username, subTotal, dicProdutos, root, tpPagamentoCombo):
	if(tpPagamentoCombo == 0):
		messagebox.showinfo('Tp. Pagamento', 'Escolha uma forma de pagamento!!')
	else:
		dicCompra = {}

		timestamp = datetime.now().astimezone(timezone(timedelta(hours=-3)))
		data_hora = timestamp.strftime('%Y-%m-%d %H:%M:%S')

		dicCompra["data_hora"] = data_hora
		dicCompra["estado"] = 'Realizado'
		dicCompra["fk_entregador_codigo"] = 1
		cod_compra =  f_inserirDados("COMPRA", dicCompra, "codigo")

		cod_cliente = f_retornaEspc(['codigo'], 'cliente', username, 'fk_pessoa_username')
		cod_cliente = cod_cliente[0][0]
		
		dicCliente_compra = {}
		dicCliente_compra['fk_compra_codigo'] = cod_compra
		dicCliente_compra['fk_cliente_codigo'] = cod_cliente
		f_inserirDados("CLIENTE_COMPRA", dicCliente_compra, "fk_compra_codigo")

		total = 0
		for i,list in dicProdutos.items():
			dicCompra_produto = {}
			dicCompra_produto['qtd'] = list[0]
			dicCompra_produto['fk_compra_codigo'] = cod_compra
			dicCompra_produto['fk_produto_codigo'] = list[2]
			f_inserirDados("COMPRA_PRODUTO", dicCompra_produto, "qtd")
			total += (list[0]) * (list[1])
		
		dicPagamento = {}
		dicPagamento['fk_tipo_pagamento_tipo_pagamento_pk'] = tpPagamentoCombo
		dicPagamento['valor'] = total
		cod_pagamento = f_inserirDados("PAGAMENTO", dicPagamento, "codigo")

		dicCompra_pagamento = {}
		dicCompra_pagamento['fk_compra_codigo'] = cod_compra
		dicCompra_pagamento['fk_pagamento_codigo'] = cod_pagamento
		f_inserirDados("COMPRA_PAGAMENTO", dicCompra_pagamento, 'fk_compra_codigo')
		root.destroy()
		return 0

def f_validaUser(username, senha, label):
    users = f_retornaInfo(['username', 'senha'], "PESSOA",'fk_endereco_codigo')

    for i in users:
        if(username in i and senha in i):
            tela = f_verificaTela(username)
            return tela
        else:
            label.config(text="Usuário não está no sistema", foreground="red")
            tela = None

    if(len(users) == 0):
        label.config(text="Nenhum usuário cadastrado no sistema", foreground="red")
        tela = None
    
    return tela

def f_verificaTela(user):
    tela = -1
    users = f_retornaInfo(['fk_pessoa_username'], "CLIENTE",'codigo')
    for i in users:
        if (user in i):
            tela = 2

    users = f_retornaInfo(['fk_pessoa_username'], "ENTREGADOR",'codigo')
    for i in users:
        if (user in i):
            tela = 1

    users = f_retornaInfo(['fk_pessoa_username'], "FUNCIONARIO",'codigo')
    for i in users:
        if (user in i):
            tela = 0
    
    return tela

def f_editar_pessoa(username):
    info = f_retornaEspc(['nome','telefone','cpf','username','senha','fk_endereco_codigo'],'PESSOA',username, 'username')
    return info

def f_editar_endereco(fk_endereco_codigo):
    info = f_retornaEspc(['cep','logradouro','numero','bairro','cidade','tipo_logradouro','complemento'],'endereco',fk_endereco_codigo, 'codigo')
    return info

def f_retornaLista(t):
    p =list()
    for i in  t:
        p.append(i[0])
    return p

def f_codigo(boxtl, tpLg):
    if(boxtl.get() == ""):
        messagebox.showinfo('ComboBox', 'Escolha uma opção ou informe um valor válido')
        tp = 0
    else:
        try:
            tp = tpLg.index(boxtl.get())
        except ValueError:
            tp = 0
    return tp

def f_funcRes(username):
    cod = f_retornaEspc(['codigo'], 'FUNCIONARIO', username, 'fk_pessoa_username')
    cod = cod[0][0]

    return cod
def f_adiciona_produto(dicProdutos, subTotal, texto_subTotal, listBox, produtoCombo, pos_produto):
    preco = f_retornaEspc(['valor'], 'PRODUTO', pos_produto, 'codigo')
    if(len(preco)> 0):
        preco = preco[0][0]
        if produtoCombo[pos_produto] in dicProdutos.keys():
            dicProdutos[f'{produtoCombo[pos_produto]}'][0] += 1
        else:
            dicProdutos[f'{produtoCombo[pos_produto]}'] = [1, preco, pos_produto]
        listBox.insert(END, produtoCombo[pos_produto])

        total = 0
        for _, produto in dicProdutos.items():
            total += (produto[0]) * (produto[1])
        
        texto_subTotal.delete(0, END)
        texto_subTotal.insert(0, total)

def f_retirar_produto(listBoxCarrinho, dicProdutos, texto_subTotal, subTotal):
    if(listBoxCarrinho.curselection() != ()):
        pos = listBoxCarrinho.curselection()[0]
        if(dicProdutos[listBoxCarrinho.get(pos)][0] == 1):
            subTotal -= dicProdutos[listBoxCarrinho.get(pos)][1]
            dicProdutos.pop(listBoxCarrinho.get(pos))
        else:
            dicProdutos[listBoxCarrinho.get(pos)][0] -= 1
            subTotal -= dicProdutos[listBoxCarrinho.get(pos)][1]
        listBoxCarrinho.delete(pos)
        texto_subTotal.delete(0, END)
        texto_subTotal.insert(0, subTotal)
        
    
    return 0

def f_info_compras(compra, label_nm, label_tel, label_cp, label_log, label_num, label_comp, label_bai, label_cid, label_tp):
    if(compra.get() != ''):
        infoP = f_retornar_info_compra(compra.get())

        label_nm.config(text = infoP[0][0])
        label_tel.config(text = infoP[0][1])
        label_cp.config(text = infoP[0][2])
        label_log.config(text = infoP[0][3])
        label_num.config(text = infoP[0][4])
        label_comp.config(text = infoP[0][5]) 
        label_bai.config(text = infoP[0][6])
        label_cid.config(text = infoP[0][7])
        label_tp.config(text = infoP[0][8])
    else:
        messagebox.showinfo('Selecione uma compra', 'Por favor!! Selecione uma compra')
    return 0

def f_info_produtos(cbProduto,comboBoxTpProduto,texto_nome,texto_valor,texto_descricao):   
    infoProd = f_retornar_info_produto(cbProduto.get())
    texto_nome.delete(0,END)
    texto_nome.insert(0,infoProd[0][0])
    texto_valor.delete(0,END)
    texto_valor.insert(1,infoProd[0][1])
    texto_descricao.delete("1.0",END)
    texto_descricao.insert("1.0",infoProd[0][2])
    retornar = f_retornaInfo(['descricao'],'tipo_produto','tipo_produto_pk')
    retornar = f_retornaLista(retornar)
    retornar.insert(0,'')
    comboBoxTpProduto.current(retornar.index(infoProd[0][3]))

    return 0

def f_atualizar_entregador(username, compra, root):
    if(compra != ''):
        cod = f_retornaEspc(['codigo'], 'ENTREGADOR', username, 'fk_pessoa_username')
        cod = cod[0][0]
        f_update_compra(cod, compra)
        root.destroy()
        return 0
    else:
        messagebox.showinfo('Compra', 'Você não selecionou nenhuma compra!!')
    
