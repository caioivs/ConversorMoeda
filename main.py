import requests
import os
import time 
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
cotacao_cache = {"dados": None, "timestamp": 0}
def obterConvercao():
    agora = time.time()
    # Reutiliza o cache se tiver menos de 60 segundos
    if cotacao_cache["dados"] and (agora - cotacao_cache["timestamp"]) < 60:
        return cotacao_cache["dados"]
    
    url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,GBP-BRL,ARS-BRL"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        resposta = requests.get(url, headers=headers, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()

        resultado = {
            "dolar": float(dados["USDBRL"]["bid"]),
            "euro": float(dados["EURBRL"]["bid"]),
            "peso": float(dados["ARSBRL"]["bid"]),
            "libra": float(dados["GBPBRL"]["bid"])
        }
        cotacao_cache["dados"] = resultado
        cotacao_cache["timestamp"] = agora
        return resultado


    except Exception as e:

        print(f"Erro ao conectar: {e}")
        return None

def converter(real, cotacao):
    return real / cotacao

@app.route("/", methods=["GET", "POST"])
def index():           
        resultado = None
        moeda = None
        erro = None
        if request.method == "POST":
                valor_real = float(request.form.get("valor_real"))
                moeda = request.form.get("moeda")
                cotacoes = obterConvercao()

                if cotacoes is None:
                    resultado = "Erro ao obter cotações. Tente novamente."
                else:
                    resultado = converter(valor_real, cotacoes[moeda])
            
        return render_template("index.html", resultado=resultado, moeda=moeda, erro=erro) 
             
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
