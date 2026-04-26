from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta

usuarios = []
transacoes = [] 
lixeira = [] 

amarelo = "#f1c40f"
verde = "#2ecc71"
vermelho = "#e74c3c"
preto = "#121212"
branco = "#ffffff"
cinza = "#2c3e50"
azul = "#3498db"
laranja = "#e67e22"
cinza_recuperacao = "#95a5a6"

def mostrar_cadastro():
    frame_login.pack_forget()
    frame_dashboard.pack_forget()
    frame_esqueci_senha.pack_forget()
    frame_cadastro.pack(expand=True)

def mostrar_login():
    frame_cadastro.pack_forget()
    frame_dashboard.pack_forget()
    frame_esqueci_senha.pack_forget()
    frame_login.pack(expand=True)
    msg_login.config(text="")

def mostrar_esqueci_senha():
    frame_login.pack_forget()
    frame_esqueci_senha.pack(expand=True)
    msg_esqueci.config(text="")

def mostrar_dashboard(nome_usuario):
    frame_login.pack_forget()
    frame_cadastro.pack_forget()
    frame_esqueci_senha.pack_forget()
    lbl_boas_vindas.config(text=f"👤 Usuário: {nome_usuario}")
    atualizar_interface()
    frame_dashboard.pack(fill=BOTH, expand=True)

def cadastrar():
    nome, email, senha = entry_nome.get(), entry_email_cad.get(), entry_senha_cad.get()
    if not nome or not email or not senha:
        msg_cadastro.config(text="❌ Preencha todos os campos", fg=vermelho)
        return
    usuarios.append({"nome": nome, "email": email, "senha": senha})
    msg_cadastro.config(text="✔ Cadastro Realizado!", fg=verde)

def login():
    email, senha = entry_email.get(), entry_senha.get()
    for user in usuarios:
        if user["email"] == email and user["senha"] == senha:
            mostrar_dashboard(user["nome"])
            return
    msg_login.config(text="❌ Email ou senha incorretos", fg=vermelho)

def redefinir_senha():
    email = entry_email_recup.get()
    nova_senha = entry_nova_senha.get()
    
    if not email or not nova_senha:
        msg_esqueci.config(text="❌ Preencha todos os campos", fg=vermelho)
        return

    for user in usuarios:
        if user["email"] == email:
            user["senha"] = nova_senha
            msg_esqueci.config(text="✔ Senha atualizada com sucesso!", fg=verde)
            entry_email_recup.delete(0, END)
            entry_nova_senha.delete(0, END)
            return
            
    msg_esqueci.config(text="❌ E-mail não encontrado no sistema", fg=vermelho)

def recuperar_dados():
    if lixeira:
        item = lixeira.pop()
        transacoes.append(item)
        atualizar_interface()
    else:
        messagebox.showinfo("Recuperar", "Não há transações apagadas para recuperar.")

def adicionar_transacao(tipo):
    try:
        valor = float(entry_valor.get())
        desc = entry_desc.get()
        if not desc: raise ValueError
        
        transacoes.append({
            "tipo": tipo, 
            "valor": valor, 
            "desc": desc, 
            "data": datetime.now() 
        })
        
        entry_valor.delete(0, END)
        entry_desc.delete(0, END)
        atualizar_interface()
    except ValueError:
        messagebox.showerror("Erro", "Insira um valor numérico e uma descrição!")

def excluir_selecionado():
    try:
        indice = lista_transacoes.curselection()[0]
        item_para_lixeira = transacoes.pop(indice)
        lixeira.append(item_para_lixeira)
        atualizar_interface()
    except (IndexError, Exception):
        messagebox.showwarning("Aviso", "Selecione uma movimentação válida para excluir!")

def calcular_estatisticas():
    receitas = [t['valor'] for t in transacoes if t['tipo'] == 'Receita']
    despesas = [t['valor'] for t in transacoes if t['tipo'] == 'Despesa']

    max_rec = max(receitas) if receitas else 0.0
    min_rec = min(receitas) if receitas else 0.0
    max_des = max(despesas) if despesas else 0.0
    min_des = min(despesas) if despesas else 0.0
    
    total_rec = sum(receitas)
    total_des = sum(despesas)

    lbl_total_rec.config(text=f"Total Receitas: R$ {total_rec:.2f}")
    lbl_extremos_rec.config(text=f"Maior: R$ {max_rec:.2f} | Menor: R$ {min_rec:.2f}")
    
    lbl_total_des.config(text=f"Total Despesas: R$ {total_des:.2f}")
    lbl_extremos_des.config(text=f"Maior: R$ {max_des:.2f} | Menor: R$ {min_des:.2f}")

def atualizar_interface():
    lista_transacoes.delete(0, END)
    receitas_soma = sum(t['valor'] for t in transacoes if t['tipo'] == 'Receita')
    despesas_soma = sum(t['valor'] for t in transacoes if t['tipo'] == 'Despesa')
    
    for t in transacoes:
        simbolo = "💰" if t['tipo'] == 'Receita' else "💸"
        data_str = t['data'].strftime("%d/%m")
        desc_limpa = t['desc'][:25]
        item_formatado = f" {data_str} | {simbolo} {desc_limpa:<25} | R$ {t['valor']:>10.2f}"
        lista_transacoes.insert(END, item_formatado)

    saldo = receitas_soma - despesas_soma
    lbl_saldo.config(text=f"Saldo: R$ {saldo:.2f}", fg=verde if saldo >= 0 else vermelho)
    calcular_estatisticas()

def gerar_grafico():
    if not transacoes:
        messagebox.showwarning("Aviso", "Não há dados para gerar o gráfico!")
        return
    rec = sum(t['valor'] for t in transacoes if t['tipo'] == 'Receita')
    des = sum(t['valor'] for t in transacoes if t['tipo'] == 'Despesa')
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie([rec, des], labels=['Receitas', 'Despesas'], colors=[verde, vermelho], autopct='%1.1f%%')
    ax.set_title("Resumo Financeiro")
    top = Toplevel()
    top.title("Gráfico de Gastos")
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.draw()
    canvas.get_tk_widget().pack()

def exibir_relatorios():
    hoje = datetime.now()
    def filtrar(dias):
        data_limite = hoje - timedelta(days=dias)
        sub_lista = [t for t in transacoes if t['data'] >= data_limite]
        rec = sum(t['valor'] for t in sub_lista if t['tipo'] == 'Receita')
        des = sum(t['valor'] for t in sub_lista if t['tipo'] == 'Despesa')
        return rec, des

    r_dia, d_dia = filtrar(1); r_sem, d_sem = filtrar(7)
    r_mes, d_mes = filtrar(30); r_ano, d_ano = filtrar(365)

    janela_rel = Toplevel()
    janela_rel.title("Relatórios Temporais")
    janela_rel.geometry("400x500")
    janela_rel.config(bg=cinza)

    def criar_bloco(titulo, rec, des):
        f = Frame(janela_rel, bg=cinza, pady=10)
        f.pack(fill=X, padx=20)
        Label(f, text=titulo, bg=cinza, fg=amarelo, font=("Arial", 12, "bold")).pack(anchor=W)
        Label(f, text=f"Receitas: R$ {rec:.2f}  |  Despesas: R$ {des:.2f}", bg=cinza, fg=branco).pack(anchor=W)
        Label(f, text=f"Saldo: R$ {rec-des:.2f}", bg=cinza, fg=verde if (rec-des)>=0 else vermelho).pack(anchor=W)
        Canvas(janela_rel, height=1, bg=branco, highlightthickness=0).pack(fill=X, padx=20)

    Label(janela_rel, text="📊 Relatório de Períodos", bg=cinza, fg=branco, font=("Arial", 16, "bold"), pady=20).pack()
    criar_bloco("Últimas 24 Horas", r_dia, d_dia)
    criar_bloco("Últimos 7 Dias", r_sem, d_sem)
    criar_bloco("Últimos 30 Dias", r_mes, d_mes)
    criar_bloco("Últimos 365 Dias", r_ano, d_ano)

janela = Tk()
janela.title("Sistema de Controle Financeiro")
janela.config(bg=preto)
try: janela.attributes('-zoomed', True)
except: janela.state('zoomed')

frame_login = Frame(janela, bg=preto)
frame_login.pack(expand=True)
Label(frame_login, text="💰 Controle Inteligente", bg=preto, fg=verde, font=("Arial", 25, "bold")).pack(pady=20)
Label(frame_login, text="📧 Email", bg=preto, fg=branco).pack()
entry_email = Entry(frame_login, width=40); entry_email.pack(pady=5)
Label(frame_login, text="🔒 Senha", bg=preto, fg=branco).pack()
entry_senha = Entry(frame_login, show="*", width=40); entry_senha.pack(pady=5)
Button(frame_login, text="Entrar", width=25, bg=verde, fg=preto, command=login, font=("Arial", 10, "bold")).pack(pady=10)
Button(frame_login, text="Criar Conta", width=25, bg=amarelo, fg=preto, command=mostrar_cadastro).pack(pady=5)
Button(frame_login, text="Esqueci minha senha", bg=preto, fg=azul, bd=0, command=mostrar_esqueci_senha, font=("Arial", 9, "underline"), cursor="hand2").pack(pady=5)
msg_login = Label(frame_login, text="", bg=preto); msg_login.pack(pady=10)

frame_cadastro = Frame(janela, bg=preto)
Label(frame_cadastro, text="👤+\nCriar Conta", bg=preto, fg=amarelo, font=("Arial", 22, "bold"), justify=CENTER).pack(pady=20)
Label(frame_cadastro, text="👤 Nome Completo", bg=preto, fg=branco).pack()
entry_nome = Entry(frame_cadastro, width=40); entry_nome.pack(pady=5)
Label(frame_cadastro, text="📧 Email", bg=preto, fg=branco).pack()
entry_email_cad = Entry(frame_cadastro, width=40); entry_email_cad.pack(pady=5)
Label(frame_cadastro, text="🔒 Senha", bg=preto, fg=branco).pack()
entry_senha_cad = Entry(frame_cadastro, width=40, show="*"); entry_senha_cad.pack(pady=5)
Button(frame_cadastro, text="Salvar Cadastro", width=25, bg=amarelo, fg=preto, command=cadastrar).pack(pady=10)
Button(frame_cadastro, text="Voltar para Login", width=25, bg=branco, fg=preto, command=mostrar_login).pack()
msg_cadastro = Label(frame_cadastro, text="", bg=preto); msg_cadastro.pack(pady=10)

frame_esqueci_senha = Frame(janela, bg=preto)
Label(frame_esqueci_senha, text="🔑 Recuperar Acesso", bg=preto, fg=azul, font=("Arial", 22, "bold")).pack(pady=20)
Label(frame_esqueci_senha, text="Confirme seu E-mail cadastrado:", bg=preto, fg=branco).pack()
entry_email_recup = Entry(frame_esqueci_senha, width=40); entry_email_recup.pack(pady=5)
Label(frame_esqueci_senha, text="Nova Senha:", bg=preto, fg=branco).pack()
entry_nova_senha = Entry(frame_esqueci_senha, width=40, show="*"); entry_nova_senha.pack(pady=5)
Button(frame_esqueci_senha, text="Atualizar Senha", width=25, bg=azul, fg=branco, command=redefinir_senha, font=("Arial", 10, "bold")).pack(pady=10)
Button(frame_esqueci_senha, text="Voltar ao Login", width=25, bg=branco, fg=preto, command=mostrar_login).pack()
msg_esqueci = Label(frame_esqueci_senha, text="", bg=preto); msg_esqueci.pack(pady=10)

frame_dashboard = Frame(janela, bg=preto)
lbl_boas_vindas = Label(frame_dashboard, text="", bg=preto, fg=branco, font=("Arial", 14)); lbl_boas_vindas.pack(pady=10)
lbl_saldo = Label(frame_dashboard, text="Saldo: R$ 0.00", bg=preto, fg=verde, font=("Arial", 24, "bold")); lbl_saldo.pack(pady=10)

f_inputs = Frame(frame_dashboard, bg=preto)
f_inputs.pack(pady=10)
Label(f_inputs, text="👛 Descrição:", bg=preto, fg=branco, font=("Arial", 10, "bold")).grid(row=0, column=0)
entry_desc = Entry(f_inputs, width=25, font=("Arial", 11)); entry_desc.grid(row=0, column=1, padx=10)
Label(f_inputs, text="💵 Valor R$:", bg=preto, fg=branco, font=("Arial", 10, "bold")).grid(row=0, column=2)
entry_valor = Entry(f_inputs, width=15, font=("Arial", 11)); entry_valor.grid(row=0, column=3, padx=10)

Label(frame_dashboard, text="📜 Histórico de Movimentações", bg=preto, fg=amarelo, font=("Arial", 12, "italic")).pack(pady=5)

lista_transacoes = Listbox(frame_dashboard, width=85, height=12, bg=cinza, fg=branco, font=("Courier", 14, "bold"), borderwidth=0, highlightthickness=1)
lista_transacoes.pack(pady=5, padx=20)

f_estats = Frame(frame_dashboard, bg=preto)
f_estats.pack(pady=5)
f_rec = Frame(f_estats, bg=preto); f_rec.grid(row=0, column=0, padx=30)
lbl_total_rec = Label(f_rec, text="Total Receitas: R$ 0.00", bg=preto, fg=verde, font=("Arial", 11, "bold")); lbl_total_rec.pack()
lbl_extremos_rec = Label(f_rec, text="Maior: R$ 0.00 | Menor: R$ 0.00", bg=preto, fg=verde, font=("Arial", 9)); lbl_extremos_rec.pack()

f_des = Frame(f_estats, bg=preto); f_des.grid(row=0, column=1, padx=30)
lbl_total_des = Label(f_des, text="Total Despesas: R$ 0.00", bg=preto, fg=vermelho, font=("Arial", 11, "bold")); lbl_total_des.pack()
lbl_extremos_des = Label(f_des, text="Maior: R$ 0.00 | Menor: R$ 0.00", bg=preto, fg=vermelho, font=("Arial", 9)); lbl_extremos_des.pack()

f_botoes = Frame(frame_dashboard, bg=preto)
f_botoes.pack(pady=10)
btn_config = {"width": 12, "height": 2, "font": ("Arial", 10, "bold")}
Button(f_botoes, text="💰 Receita", bg=verde, command=lambda: adicionar_transacao("Receita"), **btn_config).grid(row=0, column=0, padx=5)
Button(f_botoes, text="💸 Despesa", bg=vermelho, command=lambda: adicionar_transacao("Despesa"), **btn_config).grid(row=0, column=1, padx=5)
Button(f_botoes, text="🗑 Excluir", bg=laranja, fg=branco, command=excluir_selecionado, **btn_config).grid(row=0, column=2, padx=5)
Button(f_botoes, text="📊 Gráfico", bg=amarelo, command=gerar_grafico, **btn_config).grid(row=0, column=3, padx=5)
Button(f_botoes, text="📋 Relat.", bg=azul, fg=branco, command=exibir_relatorios, **btn_config).grid(row=0, column=4, padx=5)
Button(f_botoes, text="🔄 Recuperar", bg=cinza_recuperacao, fg=branco, command=recuperar_dados, **btn_config).grid(row=0, column=5, padx=5)

Button(frame_dashboard, text="Sair do Sistema", bg=cinza, fg=branco, command=mostrar_login).pack(side=BOTTOM, pady=20)

janela.mainloop()
