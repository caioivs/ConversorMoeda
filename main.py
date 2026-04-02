import requests
import os
import time 
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")
cotacao_cache = {"dados": None, "timestamp": 0}
# Busca as cotações mais recentes e cache para evitar requisão 
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
            "real": 1.0,
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
    
# Real para moeda estrangeira
def converter(valor, cotacao_origem, cotacao_destino):
    return valor * (cotacao_origem / cotacao_destino)


#Renderiza o template com base nos dados digitados pelo usuario
@app.route("/", methods=["GET", "POST"])
def index():           
    resultado = None
    erro = None
    moeda_destino = None
    if request.method == "POST":
            valor = float(request.form.get("valor"))
            moeda_origem = request.form.get("moeda_origem")
            moeda_destino = request.form.get("moeda_destino")
            cotacoes = obterConvercao()

            if cotacoes is None:
                resultado = "Erro ao obter cotações. Tente novamente."
            else:
                resultado = converter(valor, cotacoes[moeda_origem], cotacoes[moeda_destino])
            
    return render_template("index.html", resultado=resultado, erro=erro,  moeda_destino = moeda_destino) 
             
        
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True,)
