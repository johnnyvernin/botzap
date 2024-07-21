import requests
import time
import json

#Cadastre-se em editacodigo.com.br gratuitamente e obtenha sua key grátis, e adicione abaixo:
editacodigo_key = ""

def get_zap_info():
    try:
        agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        api = requests.get(f"https://editacodigo.com.br/index/api-whatsapp/{editacodigo_key}", headers=agent)
        time.sleep(1)
        api = api.text
        api = api.split(".n.")
        bolinha_notificacao = api[3].strip()
        contato_cliente = api[4].strip()
        caixa_msg = api[5].strip()
        msg_cliente = api[6].strip()
        result = [bolinha_notificacao, contato_cliente, caixa_msg, msg_cliente]
        return json.dumps(result)
    except Exception as e:
        return str(e)