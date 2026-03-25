import requests
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")

def obterConvercao():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,ARS-BRL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        dados = resposta.json()
        print(dados)
        
        return {
            "dolar": float(dados.get("USDBRL", {}).get("bid", 0)),
            "euro": float(dados.get("EURBRL", {}).get("bid", 0)),
            "peso": float(dados.get("ARSBRL", {}).get("bid", 0)),
            "libra": float(dados.get("GBPBRL", {}).get("bid", 0))
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
                valor_real = float(request.form["valor_real"])
                moeda = request.form["moeda"]
                cotacoes = obterConvercao()
                resultado = converter(valor_real, cotacoes[moeda])
            
        return render_template("index.html", resultado=resultado, moeda=moeda) 
             
if __name__ == "__main__":
    app.run(debug=True)
    
     
