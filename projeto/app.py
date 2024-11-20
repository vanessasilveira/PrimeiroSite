from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Página inicial - Formulário de cadastro
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Processamento do formulário
        nome = request.form["nome"]
        email = request.form["email"]
        produto = request.form["produto"]

        # Armazenando os dados na sessão
        session['nome'] = nome
        session['email'] = email
        session['produto'] = produto

        return redirect(url_for("calculo"))  # Redireciona para a página de cálculo

    return render_template("index.html")  # Página inicial com o formulário de cadastro

# Página de cálculo - Escolha da forma de pagamento
@app.route("/calculo", methods=["GET", "POST"])
def calculo():
    resultado = None
    if request.method == "POST":
        try:
            # Obtém o valor do produto e verifica se é válido
            valor_produto = float(request.form["valorProduto"])
            if valor_produto <= 0:
                resultado = "Por favor, insira um valor válido para o produto."
            else:
                # Obtém a forma de pagamento e calcula o valor final
                forma_pagamento = int(request.form["formaPagamento"])
                if forma_pagamento < 1 or forma_pagamento > 4:
                    resultado = "Por favor, insira uma forma de pagamento válida (1, 2, 3 ou 4)."
                else:
                    if forma_pagamento == 1:
                        valor_final = valor_produto * 0.9  # 10% de desconto
                    elif forma_pagamento == 2:
                        valor_final = valor_produto * 0.95  # 5% de desconto
                    elif forma_pagamento == 3:
                        valor_final = valor_produto  # Preço normal
                    elif forma_pagamento == 4:
                        valor_final = valor_produto * 1.1  # 10% de acréscimo

                    resultado = f"O valor final do produto '{session['produto']}' é: R$ {valor_final:.2f}"
        except ValueError:
            resultado = "Por favor, insira um valor válido para o produto."
    
    return render_template("calculo.html", resultado=resultado)
if __name__ == "__main__":
    app.run(debug=True)