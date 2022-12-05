from tkinter import*
from tkinter import Tk, StringVar, ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv


co0 = "#2e2d2b" # Preta
co1 = "#feffff" # branca
co2 = "#4fa882" # verde
co3 = "#38576b" # valor
co4 = "#403d3d" # letra
co5 = "#e06636" # - profit
co6 = "#038cfc" # azul
co7 = "#3fbfb9" # verde
co8 = "#263238" # + verde
co9 = "#e9edf5" # + verde


arqTecnicos = 'tecnicos.csv'
arqFerramentas= 'ferramentas.csv'
tecnicos    = []
ferramentas = []

global tree
global treeFer

def hideShow(frame):
    frameTecnico.grid_forget()
    frameInicial.grid_forget()
    frameFerramentas.grid_forget()
    if frame == 'tec':
        frameTecnico.grid()
        limparCampos()
        criaTabela()
    elif frame == 'fer':
        frameFerramentas.grid()
        limparCamposFer()
        criaTabelaFer()
        e_idFer['state'] = 'disabled'

    else:
        frameInicial.grid()

def salvarTecnicos(tec):
    mydict = tec
    fields = ['cpf', 'nome', 'fone', 'turno', 'equipe'] 
    filename = arqTecnicos
    with open(filename, 'w+') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        writer.writerows(mydict) 

def salvarFerramentas(fer):
    mydict = fer
    fields = ['ID','Desc','Fabr','Volt','PN','Tam','UM','Tipo','Mat','Tempo'] 
    filename = arqFerramentas
    with open(filename, 'w+') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
        writer.writeheader() 
        writer.writerows(mydict) 

def adicionarTecnico():
    if not cpfValido(e_cpf.get()):
        messagebox.showerror('Erro', 'CPF inválido')
        e_cpf.focus()
        return

    tecnico = {'cpf':e_cpf.get(),'nome':e_nome.get(),'fone':e_telefone.get(),'turno':e_turno.get(),'equipe':e_equipe.get()}
    for campo in tecnico.values():
        if campo == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
            return
    tecnicos.append(tecnico)
    salvarTecnicos(tecnicos)
    criaTabela()
    limparCampos()

def adicionarFerramentas():
    listFer = []
    idx = 0
    for fer in ferramentas:
       listFer.append(fer['ID']) 
    
    idx = proxID(listFer)
    
    ferramenta = {'ID': str(idx),'Desc':e_descFer.get(),'Fabr':e_fabricante.get(),'Volt':e_voltUso.get(),'PN':e_partNumber.get(),'Tam':e_tamanho.get(),'UM':e_unidadeMedida.get(),'Tipo':e_tipoFerramenta.get(),'Mat':e_matFerramenta.get(),'Tempo':e_tempoMax.get()}
    for campo in ferramenta.values():
        if campo == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
            return
    ferramentas.append(ferramenta)
    salvarFerramentas(ferramentas)
    criaTabelaFer()
    limparCamposFer()

def carregarDados(arq, lista):
    with open(arq) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            lista.append(dict(row))

def limparCampos():
    e_cpf['state']='normal'
    e_cpf.delete(0,'end')
    e_nome.delete(0,'end')
    e_telefone.delete(0,'end')
    e_equipe.delete(0,'end')
    e_turno.delete(0,'end')
    botao_atualizar['state']='disabled'
    botao_deletar['state']='disabled'
    botao_inserir['state']='normal'
    e_cpf.focus()

def limparCamposFer():
    e_idFer['state']='normal'
    e_idFer.delete(0,'end')
    e_descFer.delete(0,'end')
    e_fabricante.delete(0,'end')
    e_voltUso.delete(0,'end')
    e_partNumber.delete(0,'end')
    e_tamanho.delete(0,'end')
    e_unidadeMedida.delete(0,'end')
    e_tipoFerramenta.delete(0,'end')
    e_matFerramenta.delete(0,'end')
    e_tempoMax.delete(0,'end')
    botao_atualizarFer['state']='disabled'
    botao_deletarFer['state']='disabled'
    botao_inserirFer['state']='normal'
    e_descFer.focus()

def atualizarForm(event):
    limparCampos()
    treev_dicionario = tree.item(tree.focus())
    dados = treev_dicionario['values']
    e_cpf.insert(0,str(dados[0]).zfill(11))
    e_nome.insert(0,dados[1])
    e_telefone.insert(0,dados[2])
    e_turno.insert(0,dados[3])
    e_equipe.insert(0,dados[4])
    botao_atualizar['state'] = 'normal'
    botao_deletar['state'] = 'normal'
    botao_inserir['state'] = 'disabled'
    e_cpf['state'] = 'disabled'

def apagarTecnico():
    removeu = False
    cpf = e_cpf.get()
    if cpf == '':
        messagebox.showerror('Erro', 'O campo CPF é obrigatório')
        return
    for i, tecnico in enumerate(tecnicos):
        if tecnico['cpf'] == cpf:
            tecnicos.pop(i)
            removeu = True
            messagebox.showinfo('Sucesso', 'Técnico removido do cadastro')
            #break
    if not removeu:
        messagebox.showerror('Erro', 'CPF não encontrado no cadastro')
    salvarTecnicos(tecnicos)
    criaTabela()
    limparCampos()

def apagarFerramenta():
    removeu = False
    id = e_idFer.get()
    if id == '':
        messagebox.showerror('Erro', 'O campo ID é obrigatório')
        return
    for i, ferramenta in enumerate(ferramentas):
        if ferramenta['ID'] == id:
            ferramentas.pop(i)
            removeu = True
            messagebox.showinfo('Sucesso', 'Ferramenta removida do cadastro')
            #break
    if not removeu:
        messagebox.showerror('Erro', 'ID não encontrado no cadastro')
    salvarFerramentas(ferramentas)
    criaTabelaFer()
    limparCamposFer()

def atualizarTecnico():
    tecnico = {'cpf':e_cpf.get(),'nome':e_nome.get(),'fone':e_telefone.get(),'turno':e_turno.get(),'equipe':e_equipe.get()}
    for campo in tecnico.values():
        if campo == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
            return
    for idx, tec in enumerate(tecnicos):
        if tec['cpf'] == tecnico['cpf']:
            tecnicos[idx] = tecnico
            messagebox.showinfo('Sucesso', 'Alteração efetuada')
            salvarTecnicos(tecnicos)
            criaTabela()
            e_cpf['state'] = 'normal'
            botao_inserir['state'] = 'normal'
            e_cpf.focus()
            limparCampos()
            break


def atualizarFerramenta():
    ferramenta = {'ID':e_idFer.get(),'Desc':e_descFer.get(),'Fabr':e_fabricante.get(),'Volt':e_voltUso.get(),'PN':e_partNumber.get(),'Tam':e_tamanho.get(),'UM':e_unidadeMedida.get(),'Tipo':e_tipoFerramenta.get(),'Mat':e_matFerramenta.get(),'Tempo':e_tempoMax.get()}
    for campo in ferramenta.values():
        if campo == '':
            messagebox.showerror('Erro', 'Todos os campos devem ser preenchidos')
            return
    for idx, fer in enumerate(ferramentas):
        if fer['ID'] == ferramenta['ID']:
            ferramentas[idx] = ferramenta
            messagebox.showinfo('Sucesso', 'Alteração efetuada')
            salvarFerramentas(ferramentas)
            criaTabelaFer()
            e_idFer['state'] = 'normal'
            botao_inserir['state'] = 'normal'
            e_idFer.focus()
            limparCamposFer()
            break

def criaTabela():
    tabela_head = ['CPF','Nome','Telefone','Turno', 'Equipe']

    lista_itens=[]
    tecnicos.sort(key=lambda tecnico: tecnico['cpf'])
    
    for tecnico in tecnicos:
        lista_itens.append(list(tecnico.values()))

    global tree

    tree = ttk.Treeview(frameTabela, selectmode="extended",
                        columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(
        frameTabela, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(
        frameTabela, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    frameTabela.grid_rowconfigure(0, weight=12)

    hd=["w","w","w","center","center"]
    h=[100,240,190,100,200]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        tree.column(col, width=h[n],anchor=hd[n])
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)
    
    tree.bind('<<TreeviewSelect>>', atualizarForm)

def atualizarFormFerramentas(event):
    limparCamposFer()
    treev_dicionario = treeFer.item(treeFer.focus())
    dados = treev_dicionario['values']
    e_idFer.insert(0,dados[0])
    e_descFer.insert(0,dados[1])
    e_fabricante.insert(0,dados[2])
    e_voltUso.insert(0,dados[3])
    e_partNumber.insert(0,dados[4])
    e_tamanho.insert(0,dados[5])
    e_unidadeMedida.insert(0,dados[6])
    e_tipoFerramenta.insert(0,dados[7])
    e_matFerramenta.insert(0,dados[8])
    e_tempoMax.insert(0,dados[9])
    botao_atualizarFer['state'] = 'normal'
    botao_deletarFer['state'] = 'normal'
    botao_inserirFer['state'] = 'disabled'
    e_idFer['state'] = 'disabled'

def criaTabelaFer():
    tabela_headFer = ['ID','Descrição','Fabricante','Voltagem', 'Part Number', 'Tam', 'U. Med.', 'Tipo', 'Matl', 'Tempo']

    lista_ferramentas=[]
    ferramentas.sort(key=lambda ferramenta: ferramenta['ID'])
    
    for ferramenta in ferramentas:
        lista_ferramentas.append(list(ferramenta.values()))

    global treeFer

    treeFer = ttk.Treeview(frameTabelaFer, selectmode="extended",
                        columns=tabela_headFer, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(
        frameTabelaFer, orient="vertical", command=treeFer.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(
        frameTabelaFer, orient="horizontal", command=treeFer.xview)

    treeFer.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    treeFer.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    frameTabelaFer.grid_rowconfigure(0, weight=12)

    hd=["w","w","w","w","w", "e", "w", "w", "w", "e"]
    h=[20,250,110,80,80,40,50,80,70,50]
    n=0

    for colFer in tabela_headFer:
        treeFer.heading(colFer, text=colFer.title(), anchor=CENTER)
        treeFer.column(colFer, width=h[n],anchor=hd[n])
        n+=1

    for item in lista_ferramentas:
        treeFer.insert('', 'end', values=item)
    
    treeFer.bind('<<TreeviewSelect>>', atualizarFormFerramentas)

def limitaTamanho(campo, qtd):
    if len(campo.get()) > qtd:
        campo.set(campo.get()[:qtd])        

def proxID(lista):
    max_value = 0
    for num in lista:
        num = int(num)
        if(max_value is None or num > max_value):
            max_value = num
    return max_value + 1

def limitaNum(campo, qtd = None):
    if campo.get() != '':
        try:
            int(campo.get())
        except ValueError:
            messagebox.showerror('Erro', 'Este campo só aceita números')
            campo.set(campo.get()[:-1])
        if qtd:
            limitaTamanho(campo, qtd) 

def cpfValido(cpf):
     # tamanho igual a 11
    if len(str(cpf)) != 11:
        return False
    
    # palíndromo
    pal = True
    for n in range(0,int(len(cpf)/2)):
        if cpf[n] != cpf[(len(cpf) - n) - 1]:
            pal = False
            break
    if pal:
        return False

    #primeiro digito verificador        
    i = 0
    soma = 0
    for n in range(10,1,-1):
        soma += int(cpf[i]) * n
        i += 1
    resto = (soma * 10 % 11)
    if resto == 10:
        resto = 0
    if resto != int(cpf[9]):
        return False

    #segundo digito verificador        
    i = 0
    soma = 0
    for n in range(11,1,-1):
        soma += int(cpf[i]) * n
        i += 1
    resto = (soma * 10 % 11)
    if resto == 10:
        resto = 0
    if resto != int(cpf[10]):
        return False

    return True

janela = Tk( )
janela.title("Gerenciamento de Ferramentas")
janela.geometry('850x600')
janela.configure(background=co9)
janela.resizable(width=FALSE, height=FALSE)
style = ttk.Style(janela)
style.theme_use("clam")



#================Frame Inicial==================
frameInicial = Frame(janela,width=1043, height=800, relief="flat")
frameInicial.grid(row=0, column=0)

# Botao Tecnicos
img_tec  = Image.open('img\\tecnico.png')
img_tec = img_tec.resize((20, 20))
img_tec = ImageTk.PhotoImage(img_tec)
botao_tecnicos = Button(frameInicial, command=lambda:hideShow('tec'),image=img_tec, compound=LEFT, anchor=NW, text="   Técnicos".upper(), width=105, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_tecnicos.place(x=250, y=300)

# Botao Ferramentas
img_fer  = Image.open('img\\ferramenta.png')
img_fer = img_fer.resize((20, 20))
img_fer = ImageTk.PhotoImage(img_fer)
botao_ferramentas = Button(frameInicial, command=lambda:hideShow('fer'),image=img_fer, compound=LEFT, anchor=NW, text="Ferramentas".upper(), width=105, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_ferramentas.place(x=470, y=300)


#================Frame Ferramentas==================

frameFerramentas = Frame(janela,width=1043, height=50, relief="flat")

frameCabecalhoFer = Frame(frameFerramentas, width=1043, height=50, bg=co5,  relief="flat")
frameCabecalhoFer.grid(row=0, column=0)

frameDadosFer = Frame(frameFerramentas,width=1043, height=333,bg=co1, pady=20, relief="flat")
frameDadosFer.grid(row=1, column=0,pady=1, padx=0, sticky=NSEW)

frameTabelaFer = Frame(frameFerramentas,width=1043, height=300,bg=co1, relief="flat")
frameTabelaFer.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

app_imgFer = Image.open('img\\ferramenta.png')
app_imgFer = app_imgFer.resize((50, 50))
app_imgFer = ImageTk.PhotoImage(app_imgFer)

app_logoFer = Label(frameCabecalhoFer, image=app_imgFer, text="Cadastro de Ferramentas", width=850, compound=LEFT, relief=RAISED, anchor=N, font=('System 15 bold'),bg=co1, fg=co4 )
app_logoFer.place(x=0, y=0)

l_idFer = Label(frameDadosFer, text="ID Ferramenta", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_idFer.place(x=10, y=10)
e_idFer = Entry(frameDadosFer, width=30, justify='left',relief="solid")
e_idFer.place(x=280, y=11)

e_descFer_sv = StringVar()
e_descFer_sv.trace('w', lambda *args: limitaTamanho(e_descFer_sv, 60))
l_descFer = Label(frameDadosFer, text="Descrição da Ferramenta", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_descFer.place(x=10, y=40)
e_descFer = Entry(frameDadosFer, textvariable=e_descFer_sv, width=30, justify='left',relief="solid")
e_descFer.place(x=280, y=41)

e_fabricante_sv = StringVar()
e_fabricante_sv.trace('w', lambda *args: limitaTamanho(e_fabricante_sv, 30))
l_fabricante = Label(frameDadosFer, text="Fabricante", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_fabricante.place(x=10, y=70)
e_fabricante = Entry(frameDadosFer, textvariable=e_fabricante_sv, width=30, justify='left',relief="solid")
e_fabricante.place(x=280, y=71)

e_voltUso_sv = StringVar()
e_voltUso_sv.trace('w', lambda *args: limitaTamanho(e_voltUso_sv, 15))
l_voltUso = Label(frameDadosFer, text="Voltagem", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_voltUso.place(x=10, y=100)
e_voltUso = Entry(frameDadosFer, textvariable=e_voltUso_sv, width=30, justify='left',relief="solid")
e_voltUso.place(x=280, y=101)

e_partNumber_sv = StringVar()
e_partNumber_sv.trace('w', lambda *args: limitaTamanho(e_partNumber_sv, 25))
l_partNumber = Label(frameDadosFer, text="Part Number", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_partNumber.place(x=10, y=130)
e_partNumber = Entry(frameDadosFer, textvariable=e_partNumber_sv, width=30, justify='left',relief="solid")
e_partNumber.place(x=280, y=131)

e_tamanho_sv = StringVar()
e_tamanho_sv.trace('w', lambda *args: limitaNum(e_tamanho_sv, 20))
l_tamanho = Label(frameDadosFer, text="Tamanho", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_tamanho.place(x=10, y=160)
e_tamanho = Entry(frameDadosFer, textvariable=e_tamanho_sv, width=30, justify='left',relief="solid")
e_tamanho.place(x=280, y=161)

e_unidadeMedida_sv = StringVar()
e_unidadeMedida_sv.trace('w', lambda *args: limitaTamanho(e_unidadeMedida_sv, 15))
l_unidadeMedida = Label(frameDadosFer, text="Unidade de Medida", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_unidadeMedida.place(x=10, y=190)
e_unidadeMedida = Entry(frameDadosFer, textvariable=e_unidadeMedida_sv, width=30, justify='left',relief="solid")
e_unidadeMedida.place(x=280, y=191)

e_tipoFerramenta_sv = StringVar()
e_tipoFerramenta_sv.trace('w', lambda *args: limitaTamanho(e_tipoFerramenta_sv, 15))
l_tipoFerramenta = Label(frameDadosFer, text="Tipo de Ferramenta", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_tipoFerramenta.place(x=10, y=220)
e_tipoFerramenta = Entry(frameDadosFer, textvariable=e_tipoFerramenta_sv, width=30, justify='left',relief="solid")
e_tipoFerramenta.place(x=280, y=221)

e_matFerramenta_sv = StringVar()
e_matFerramenta_sv.trace('w', lambda *args: limitaTamanho(e_matFerramenta_sv, 15))
l_matFerramenta = Label(frameDadosFer, text="Material da Ferramenta", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_matFerramenta.place(x=10, y=250)
e_matFerramenta = Entry(frameDadosFer, textvariable=e_matFerramenta_sv, width=30, justify='left',relief="solid")
e_matFerramenta.place(x=280, y=251)

e_tempoMax_sv = StringVar()
e_tempoMax_sv.trace('w', lambda *args: limitaNum(e_tempoMax_sv))
l_tempoMax = Label(frameDadosFer, text="Tempo Maximo", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_tempoMax.place(x=10, y=280)
e_tempoMax = Entry(frameDadosFer, textvariable=e_tempoMax_sv, width=30, justify='left',relief="solid")
e_tempoMax.place(x=280, y=281)

# Botao Adicionar
img_addFer  = Image.open('img\\add.png')
img_addFer = img_addFer.resize((20, 20))
img_addFer = ImageTk.PhotoImage(img_addFer)
botao_inserirFer = Button(frameDadosFer, command=adicionarFerramentas,image=img_addFer, compound=LEFT, anchor=NW, text="   Adicionar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_inserirFer.place(x=580, y=10)

# Botao Atualizar
img_updateFer  = Image.open('img\\update.png')
img_updateFer = img_updateFer.resize((20, 20))
img_updateFer = ImageTk.PhotoImage(img_updateFer)
botao_atualizarFer = Button(frameDadosFer, command=atualizarFerramenta,image=img_updateFer, compound=LEFT, anchor=NW, text="   Atualizar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_atualizarFer.place(x=580, y=50)
botao_atualizarFer['state'] = 'disabled'

# Botao Deletar
img_deleteFer  = Image.open('img\\delete.png')
img_deleteFer = img_deleteFer.resize((20, 20))
img_deleteFer = ImageTk.PhotoImage(img_deleteFer)
botao_deletarFer = Button(frameDadosFer, command=apagarFerramenta,image=img_deleteFer, compound=LEFT, anchor=NW, text="   Deletar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_deletarFer.place(x=580, y=90)
botao_deletarFer['state'] = 'disabled'

#Botão Voltar
img_backFer  = Image.open('img\\back.png')
img_backFer = img_backFer.resize((20, 20))
img_backFer = ImageTk.PhotoImage(img_backFer)
botao_imprimirFer = Button(frameDadosFer, command=lambda:hideShow('ini'),image=img_backFer, compound=LEFT, anchor=NW, text="   Voltar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_imprimirFer.place(x=580, y=130)


#================Frame Técnicos==================
frameTecnico = Frame(janela,width=1043, height=50, relief="flat")

frameCabecalho = Frame(frameTecnico, width=1043, height=50, bg=co5,  relief="flat")
frameCabecalho.grid(row=0, column=0)

frameDados = Frame(frameTecnico,width=1043, height=303,bg=co1, pady=20, relief="flat")
frameDados.grid(row=1, column=0,pady=1, padx=0, sticky=NSEW)

frameTabela = Frame(frameTecnico,width=1043, height=300,bg=co1, relief="flat")
frameTabela.grid(row=2, column=0, pady=0, padx=1, sticky=NSEW)

app_img = Image.open('img\\tecnico.png')
app_img = app_img.resize((50, 50))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCabecalho, image=app_img, text="Cadastro de técnicos", width=850, compound=LEFT, relief=RAISED, anchor=N, font=('System 15 bold'),bg=co1, fg=co4 )
app_logo.place(x=0, y=0)

e_cpf_sv = StringVar()
e_cpf_sv.trace('w', lambda *args: limitaNum(e_cpf_sv, 11))
l_cpf = Label(frameDados, text="CPF", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_cpf.place(x=10, y=10)
e_cpf = Entry(frameDados, textvariable=e_cpf_sv, width=30, justify='left',relief="solid")
e_cpf.place(x=200, y=11)

e_nome_sv = StringVar()
e_nome_sv.trace('w', lambda *args: limitaTamanho(e_nome_sv, 40))
l_nome = Label(frameDados, text="Nome", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_nome.place(x=10, y=40)
e_nome = Entry(frameDados, textvariable=e_nome_sv, width=30, justify='left',relief="solid")
e_nome.place(x=200, y=41)

e_telefone_sv = StringVar()
e_telefone_sv.trace('w', lambda *args: limitaNum(e_telefone_sv, 9))
l_telefone = Label(frameDados, text="Telefone", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_telefone.place(x=10, y=70)
e_telefone = Entry(frameDados, textvariable=e_telefone_sv, width=30, justify='left',relief="solid")
e_telefone.place(x=200, y=71)

e_turno_var = StringVar()
l_turno = Label(frameDados, text="Turno", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_turno.place(x=10, y=100)
e_turno = ttk.Combobox(frameDados, textvariable=e_turno_var)
e_turno['values'] = ('Manhã','Tarde','Noite')
e_turno.place(x=200, y=101)

e_equipe_sv = StringVar()
e_equipe_sv.trace('w', lambda *args: limitaTamanho(e_equipe_sv, 30))
l_equipe = Label(frameDados, text="Equipe", height=1,anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_equipe.place(x=10, y=130)
e_equipe = Entry(frameDados, textvariable=e_equipe_sv, width=30, justify='left',relief="solid")
e_equipe.place(x=200, y=131)

# Botao Inserir
img_add  = Image.open('img\\add.png')
img_add = img_add.resize((20, 20))
img_add = ImageTk.PhotoImage(img_add)
botao_inserir = Button(frameDados, command=adicionarTecnico,image=img_add, compound=LEFT, anchor=NW, text="   Adicionar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_inserir.place(x=530, y=10)

# Botao Atualizar
img_update  = Image.open('img\\update.png')
img_update = img_update.resize((20, 20))
img_update = ImageTk.PhotoImage(img_update)
botao_atualizar = Button(frameDados, command=atualizarTecnico,image=img_update, compound=LEFT, anchor=NW, text="   Atualizar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_atualizar.place(x=530, y=50)
botao_atualizar['state'] = 'disabled'

# Botao Deletar
img_delete  = Image.open('img\\delete.png')
img_delete = img_delete.resize((20, 20))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frameDados, command=apagarTecnico,image=img_delete, compound=LEFT, anchor=NW, text="   Deletar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_deletar.place(x=530, y=90)
botao_deletar['state'] = 'disabled'

# Botao Voltar
img_back  = Image.open('img\\back.png')
img_back = img_back.resize((20, 20))
img_back = ImageTk.PhotoImage(img_back)
botao_imprimir = Button(frameDados, command=lambda:hideShow('ini'),image=img_back, compound=LEFT, anchor=NW, text="   Voltar".upper(), width=95, overrelief=RIDGE,  font=('ivy 8'),bg=co1, fg=co0 )
botao_imprimir.place(x=530, y=130)

carregarDados(arqTecnicos, tecnicos)
carregarDados(arqFerramentas, ferramentas)
criaTabela()
criaTabelaFer()


janela.mainloop()