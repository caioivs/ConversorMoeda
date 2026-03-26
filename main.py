import requests
import os
import time 
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
cotacao_cache = {"dados": None, "timestamp": 0}
def obterConvercao():
    agora = time.time()
    if cotacao_cache["dados"] and (agora - cotacao_cache["timestamp"]) < 60:
        return cotacao_cache["dados"]
    
    url = "https://open.er-api.com/v6/latest/USD"

    try:
        resposta = requests.get(url, timeout=15)
        resposta.raise_for_status()
        dados = resposta.json()
        usd_brl = float(dados["rates"]["BRL"])

        cotacao = {
            "dolar": usd_brl,
            "euro":  usd_brl / float(dados["rates"]["EUR"]),
            "peso":  usd_brl / float(dados["rates"]["ARS"]),
            "libra": usd_brl / float(dados["rates"]["GBP"])
        }
        cotacao_cache["dados"] = cotacao
        cotacao_cache["timestamp"] = agora
        return cotacao


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
