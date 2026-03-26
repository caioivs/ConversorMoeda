import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

def obterConvercao():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,ARS-BRL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        dados = resposta.json()

        return {
            "dolar": float(dados["USDBRL"]["bid"]),
            "euro": float(dados["EURBRL"]["bid"]),
            "peso": float(dados["ARSBRL"]["bid"]),
            "libra": float(dados["GBPBRL"]["bid"])
        }
    except Exception as e:
        print(f"Erro ao conectar: {e}")
        return None

def converter(real, cotacao):
    return real / cotacao

@app.route("/", methods=["GET", "POST"])

def index():           
        resultado = None
        moeda = None
        if request.method == "POST":
                valor_real = float(request.form.get("valor_real"))
                moeda = request.form.get("moeda")
                cotacoes = obterConvercao()
                resultado = converter(valor_real, cotacoes[moeda])
            
        return render_template("index.html", resultado=resultado, moeda=moeda) 
             
        
import os

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
