from datetime import datetime
from dados import usuarios, transacoes, lixeira

# ================= LOGIN =================

def cadastrar_usuario(nome, email, senha):

    if not nome or not email or not senha:
        return False, "Preencha todos os campos"

    usuarios.append({
        "nome": nome,
        "email": email,
        "senha": senha
    })

    return True, "Cadastro realizado com sucesso"


def fazer_login(email, senha):

    for usuario in usuarios:

        if usuario["email"] == email and usuario["senha"] == senha:
            return True, usuario["nome"]

    return False, "Email ou senha incorretos"


def redefinir_senha(email, nova_senha):

    if not email or not nova_senha:
        return False, "Preencha todos os campos"

    for usuario in usuarios:

        if usuario["email"] == email:
            usuario["senha"] = nova_senha
            return True, "Senha atualizada"

    return False, "Email não encontrado"


# ================= TRANSAÇÕES =================

def adicionar_transacao(tipo, valor, descricao):

    try:
        valor = float(valor)

        if descricao == "":
            return False, "Descrição inválida"

        transacoes.append({
            "tipo": tipo,
            "valor": valor,
            "desc": descricao,
            "data": datetime.now()
        })

        return True, "Transação adicionada"

    except:
        return False, "Valor inválido"


def excluir_transacao(indice):

    try:
        item = transacoes.pop(indice)

        lixeira.append(item)

        return True

    except:
        return False


def recuperar_transacao():

    if lixeira:

        item = lixeira.pop()

        transacoes.append(item)

        return True

    return False


# ================= ESTATÍSTICAS =================

def calcular_saldo():

    receitas = sum(
        t["valor"]
        for t in transacoes
        if t["tipo"] == "Receita"
    )

    despesas = sum(
        t["valor"]
        for t in transacoes
        if t["tipo"] == "Despesa"
    )

    saldo = receitas - despesas

    return receitas, despesas, saldo
