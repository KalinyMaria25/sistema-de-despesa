from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from logica import *
from dados import transacoes

# CORES (iguais)
amarelo = "#f1c40f"
verde = "#2ecc71"
vermelho = "#e74c3c"
preto = "#121212"
branco = "#ffffff"
cinza = "#2c3e50"
azul = "#3498db"
laranja = "#e67e22"
cinza_recuperacao = "#95a5a6"

def iniciar_sistema():
    global janela, frame_login, frame_cadastro, frame_dashboard, frame_esqueci_senha
    global entry_email, entry_senha, entry_nome, entry_email_cad, entry_senha_cad
    global entry_email_recup, entry_nova_senha
    global entry_desc, entry_valor, lista_transacoes
    global lbl_saldo, lbl_boas_vindas, msg_login, msg_cadastro, msg_esqueci
    global lbl_total_rec, lbl_total_des, lbl_extremos_rec, lbl_extremos_des

    janela = Tk()
    janela.title("Sistema de Controle Financeiro")
    janela.config(bg=preto)
    try: janela.attributes('-zoomed', True)
    except: janela.state('zoomed')

    # ================= TELAS =================

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

    def mostrar_esqueci():
        frame_login.pack_forget()
        frame_esqueci_senha.pack(expand=True)
        msg_esqueci.config(text="")

    def mostrar_dashboard(nome):
        frame_login.pack_forget()
        frame_cadastro.pack_forget()
        frame_esqueci_senha.pack_forget()
        lbl_boas_vindas.config(text=f"👤 Usuário: {nome}")
        atualizar_interface()
        frame_dashboard.pack(fill=BOTH, expand=True)

    # ================= AÇÕES =================

    def acao_cadastrar():
        if cadastrar(entry_nome.get(), entry_email_cad.get(), entry_senha_cad.get()):
            msg_cadastro.config(text="✔ Cadastro Realizado!", fg=verde)
        else:
            msg_cadastro.config(text="❌ Preencha todos os campos", fg=vermelho)

    def acao_login():
        nome = login(entry_email.get(), entry_senha.get())
        if nome:
            mostrar_dashboard(nome)
        else:
            msg_login.config(text="❌ Email ou senha incorretos", fg=vermelho)

    def acao_redefinir():
        if redefinir_senha(entry_email_recup.get(), entry_nova_senha.get()):
            msg_esqueci.config(text="✔ Senha atualizada com sucesso!", fg=verde)
        else:
            msg_esqueci.config(text="❌ E-mail não encontrado", fg=vermelho)

    def adicionar(tipo):
        try:
            valor = float(entry_valor.get())
            desc = entry_desc.get()
            if adicionar_transacao(tipo, valor, desc):
                entry_valor.delete(0, END)
                entry_desc.delete(0, END)
                atualizar_interface()
            else:
                raise ValueError
        except:
            messagebox.showerror("Erro", "Insira valor válido!")

    def excluir():
        try:
            i = lista_transacoes.curselection()[0]
            excluir_transacao(i)
            atualizar_interface()
        except:
            messagebox.showwarning("Aviso", "Selecione um item!")

    def recuperar():
        if recuperar_dados():
            atualizar_interface()
        else:
            messagebox.showinfo("Recuperar", "Nada na lixeira")

    def atualizar_interface():
        lista_transacoes.delete(0, END)

        stats = calcular_estatisticas()

        for t in transacoes:
            simbolo = "💰" if t['tipo'] == 'Receita' else "💸"
            data = t['data'].strftime("%d/%m")
            desc = t['desc'][:25]
            linha = f" {data} | {simbolo} {desc:<25} | R$ {t['valor']:>10.2f}"
            lista_transacoes.insert(END, linha)

        saldo = stats["total_rec"] - stats["total_des"]
        lbl_saldo.config(text=f"Saldo: R$ {saldo:.2f}", fg=verde if saldo >= 0 else vermelho)

        lbl_total_rec.config(text=f"Total Receitas: R$ {stats['total_rec']:.2f}")
        lbl_total_des.config(text=f"Total Despesas: R$ {stats['total_des']:.2f}")

        lbl_extremos_rec.config(text=f"Maior: R$ {stats['max_rec']:.2f} | Menor: R$ {stats['min_rec']:.2f}")
        lbl_extremos_des.config(text=f"Maior: R$ {stats['max_des']:.2f} | Menor: R$ {stats['min_des']:.2f}")

    def grafico():
        stats = calcular_estatisticas()
        fig, ax = plt.subplots()
        ax.pie([stats["total_rec"], stats["total_des"]], labels=["Receitas", "Despesas"], autopct='%1.1f%%')

        top = Toplevel()
        canvas = FigureCanvasTkAgg(fig, master=top)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # ================= LOGIN =================

    frame_login = Frame(janela, bg=preto)
    frame_login.pack(expand=True)

    Label(frame_login, text="💰 Controle Inteligente", bg=preto, fg=verde, font=("Arial", 25, "bold")).pack(pady=20)

    entry_email = Entry(frame_login, width=40)
    entry_email.pack(pady=5)

    entry_senha = Entry(frame_login, show="*", width=40)
    entry_senha.pack(pady=5)

    Button(frame_login, text="Entrar", command=acao_login).pack(pady=10)
    Button(frame_login, text="Criar Conta", command=mostrar_cadastro).pack()
    Button(frame_login, text="Esqueci senha", command=mostrar_esqueci).pack()

    msg_login = Label(frame_login, bg=preto)
    msg_login.pack()

    # ================= CADASTRO =================

    frame_cadastro = Frame(janela, bg=preto)

    entry_nome = Entry(frame_cadastro, width=40)
    entry_nome.pack(pady=5)

    entry_email_cad = Entry(frame_cadastro, width=40)
    entry_email_cad.pack(pady=5)

    entry_senha_cad = Entry(frame_cadastro, show="*", width=40)
    entry_senha_cad.pack(pady=5)

    Button(frame_cadastro, text="Salvar", command=acao_cadastrar).pack(pady=10)
    Button(frame_cadastro, text="Voltar", command=mostrar_login).pack()

    msg_cadastro = Label(frame_cadastro, bg=preto)
    msg_cadastro.pack()

    # ================= DASHBOARD =================

    frame_dashboard = Frame(janela, bg=preto)

    lbl_boas_vindas = Label(frame_dashboard, bg=preto, fg=branco)
    lbl_boas_vindas.pack()

    lbl_saldo = Label(frame_dashboard, text="Saldo: R$ 0.00", bg=preto, fg=verde, font=("Arial", 20))
    lbl_saldo.pack()

    entry_desc = Entry(frame_dashboard)
    entry_desc.pack()

    entry_valor = Entry(frame_dashboard)
    entry_valor.pack()

    lista_transacoes = Listbox(frame_dashboard, width=80, font=("Courier", 12))
    lista_transacoes.pack()

    lbl_total_rec = Label(frame_dashboard, bg=preto, fg=verde)
    lbl_total_rec.pack()

    lbl_extremos_rec = Label(frame_dashboard, bg=preto, fg=verde)
    lbl_extremos_rec.pack()

    lbl_total_des = Label(frame_dashboard, bg=preto, fg=vermelho)
    lbl_total_des.pack()

    lbl_extremos_des = Label(frame_dashboard, bg=preto, fg=vermelho)
    lbl_extremos_des.pack()

    Button(frame_dashboard, text="Receita", command=lambda: adicionar("Receita")).pack()
    Button(frame_dashboard, text="Despesa", command=lambda: adicionar("Despesa")).pack()
    Button(frame_dashboard, text="Excluir", command=excluir).pack()
    Button(frame_dashboard, text="Recuperar", command=recuperar).pack()
    Button(frame_dashboard, text="Gráfico", command=grafico).pack()

    Button(frame_dashboard, text="Sair", command=mostrar_login).pack()

    janela.mainloop()
