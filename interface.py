from tkinter import *
from tkinter import messagebox

from logica import *
from dados import transacoes

# ================= CORES =================

preto = "#121212"
verde = "#2ecc71"
vermelho = "#e74c3c"
amarelo = "#f1c40f"
branco = "#ffffff"

# ================= FUNÇÕES =================

def tela_dashboard(nome_usuario):

    frame_login.pack_forget()

    lbl_usuario.config(
        text=f"👤 Usuário: {nome_usuario}"
    )

    atualizar_lista()

    frame_dashboard.pack(fill=BOTH, expand=True)


def login():

    email = entry_email.get()
    senha = entry_senha.get()

    ok, resposta = fazer_login(email, senha)

    if ok:

        tela_dashboard(resposta)

    else:

        msg_login.config(
            text=resposta,
            fg=vermelho
        )


def cadastrar():

    ok, resposta = cadastrar_usuario(
        entry_nome.get(),
        entry_email_cad.get(),
        entry_senha_cad.get()
    )

    msg_cadastro.config(
        text=resposta,
        fg=verde if ok else vermelho
    )


def adicionar(tipo):

    ok, msg = adicionar_transacao(
        tipo,
        entry_valor.get(),
        entry_desc.get()
    )

    if ok:

        entry_desc.delete(0, END)
        entry_valor.delete(0, END)

        atualizar_lista()

    else:

        messagebox.showerror("Erro", msg)


def atualizar_lista():

    lista.delete(0, END)

    for t in transacoes:

        data = t["data"].strftime("%d/%m %H:%M")

        lista.insert(
            END,
            f"{data} | {t['tipo']} | {t['desc']} | R$ {t['valor']:.2f}"
        )

    receitas, despesas, saldo = calcular_saldo()

    lbl_saldo.config(
        text=f"Saldo: R$ {saldo:.2f}",
        fg=verde if saldo >= 0 else vermelho
    )


def excluir():

    try:

        indice = lista.curselection()[0]

        if excluir_transacao(indice):
            atualizar_lista()

    except:

        messagebox.showwarning(
            "Aviso",
            "Selecione uma transação"
        )


def recuperar():

    if recuperar_transacao():

        atualizar_lista()

    else:

        messagebox.showinfo(
            "Recuperar",
            "Nada para recuperar"
        )


# ================= JANELA =================

janela = Tk()

janela.title("Controle Financeiro")

janela.config(bg=preto)

janela.state("zoomed")

# ================= LOGIN =================

frame_login = Frame(janela, bg=preto)

frame_login.pack(expand=True)

Label(
    frame_login,
    text="💰 Controle Financeiro",
    bg=preto,
    fg=verde,
    font=("Arial", 24, "bold")
).pack(pady=20)

Label(
    frame_login,
    text="Email",
    bg=preto,
    fg=branco
).pack()

entry_email = Entry(frame_login, width=40)

entry_email.pack(pady=5)

Label(
    frame_login,
    text="Senha",
    bg=preto,
    fg=branco
).pack()

entry_senha = Entry(
    frame_login,
    width=40,
    show="*"
)

entry_senha.pack(pady=5)

Button(
    frame_login,
    text="Entrar",
    bg=verde,
    width=20,
    command=login
).pack(pady=10)

msg_login = Label(
    frame_login,
    text="",
    bg=preto
)

msg_login.pack()

# ================= CADASTRO =================

Label(
    frame_login,
    text="Criar Conta",
    bg=preto,
    fg=amarelo,
    font=("Arial", 14, "bold")
).pack(pady=10)

entry_nome = Entry(frame_login, width=40)

entry_nome.pack(pady=3)

entry_email_cad = Entry(frame_login, width=40)

entry_email_cad.pack(pady=3)

entry_senha_cad = Entry(
    frame_login,
    width=40,
    show="*"
)

entry_senha_cad.pack(pady=3)

Button(
    frame_login,
    text="Cadastrar",
    bg=amarelo,
    command=cadastrar
).pack(pady=10)

msg_cadastro = Label(
    frame_login,
    text="",
    bg=preto
)

msg_cadastro.pack()

# ================= DASHBOARD =================

frame_dashboard = Frame(
    janela,
    bg=preto
)

lbl_usuario = Label(
    frame_dashboard,
    text="",
    bg=preto,
    fg=branco,
    font=("Arial", 14)
)

lbl_usuario.pack(pady=10)

lbl_saldo = Label(
    frame_dashboard,
    text="Saldo: R$ 0.00",
    bg=preto,
    fg=verde,
    font=("Arial", 24, "bold")
)

lbl_saldo.pack(pady=10)

frame_inputs = Frame(
    frame_dashboard,
    bg=preto
)

frame_inputs.pack(pady=10)

entry_desc = Entry(
    frame_inputs,
    width=30
)

entry_desc.grid(row=0, column=0, padx=5)

entry_valor = Entry(
    frame_inputs,
    width=15
)

entry_valor.grid(row=0, column=1, padx=5)

Button(
    frame_inputs,
    text="Receita",
    bg=verde,
    command=lambda: adicionar("Receita")
).grid(row=0, column=2, padx=5)

Button(
    frame_inputs,
    text="Despesa",
    bg=vermelho,
    command=lambda: adicionar("Despesa")
).grid(row=0, column=3, padx=5)

lista = Listbox(
    frame_dashboard,
    width=90,
    height=15
)

lista.pack(pady=10)

Button(
    frame_dashboard,
    text="Excluir",
    bg=vermelho,
    fg=branco,
    command=excluir
).pack(pady=5)

Button(
    frame_dashboard,
    text="Recuperar",
    bg=amarelo,
    command=recuperar
).pack(pady=5)

janela.mainloop()
