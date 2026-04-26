from datetime import datetime, timedelta
from dados import usuarios, transacoes, lixeira

def cadastrar(nome, email, senha):
    if not nome or not email or not senha:
        return False
    usuarios.append({"nome": nome, "email": email, "senha": senha})
    return True

def login(email, senha):
    for user in usuarios:
        if user["email"] == email and user["senha"] == senha:
            return user["nome"]
    return None

def redefinir_senha(email, nova_senha):
    if not email or not nova_senha:
        return False

    for user in usuarios:
        if user["email"] == email:
            user["senha"] = nova_senha
            return True
    return False

def adicionar_transacao(tipo, valor, desc):
    if not desc:
        return False

    transacoes.append({
        "tipo": tipo,
        "valor": valor,
        "desc": desc,
        "data": datetime.now()
    })
    return True

def excluir_transacao(indice):
    try:
        item = transacoes.pop(indice)
        lixeira.append(item)
        return True
    except:
        return False

def recuperar_dados():
    if lixeira:
        transacoes.append(lixeira.pop())
        return True
    return False

def calcular_estatisticas():
    receitas = [t['valor'] for t in transacoes if t['tipo'] == 'Receita']
    despesas = [t['valor'] for t in transacoes if t['tipo'] == 'Despesa']

    return {
        "total_rec": sum(receitas),
        "total_des": sum(despesas),
        "max_rec": max(receitas) if receitas else 0,
        "min_rec": min(receitas) if receitas else 0,
        "max_des": max(despesas) if despesas else 0,
        "min_des": min(despesas) if despesas else 0
    }

def relatorio_periodo(dias):
    hoje = datetime.now()
    limite = hoje - timedelta(days=dias)

    lista = [t for t in transacoes if t['data'] >= limite]

    rec = sum(t['valor'] for t in lista if t['tipo'] == 'Receita')
    des = sum(t['valor'] for t in lista if t['tipo'] == 'Despesa')

    return rec, des
