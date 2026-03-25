import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

def obterConvercao():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL,GBP-BRL,ARS-BRL"
    resposta = requests.get(url)
    dados = resposta.json()

    cotacoes = {
        "dolar": float(dados["USDBRL"]["bid"]),
        "euro": float(dados["EURBRL"]["bid"]),
        "peso": float(dados["ARSBRL"]["bid"]),
        "libra": float(dados["GBPBRL"]["bid"])
    }
    return cotacoes

def converter(real, cotacao):
    return real / cotacao

@app.route("/", methods=["GET", "POST"])
def index():           
        resultado = None
        moeda = None
        if request.method == "POST":
                valor_real = float(request.form["valor_real"])
                moeda = request.form["moeda"]
                cotacoes = obterConvercao()
                resultado = converter(valor_real, cotacoes[moeda])
            
        return render_template("index.html", resultado=resultado, moeda=moeda) 
             
if __name__ == "__main__":
    app.run(debug=True)
    
     