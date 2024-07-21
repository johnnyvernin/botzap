from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from api import get_zap_info
import json
import re
from ai import responde
import pyperclip

#Captura QRCODE ZAP
dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/profile/zap")
driver = webdriver.Chrome(options=chrome_options2)
driver.get("https://web.whatsapp.com")
time.sleep(5)

#Trata Retorno de bolinha_notificacao
def extract_value(text):
    match = re.search(r'div\.([^:]+):', text)
    if match:
        return match.group(1)
    return None

#Código Principal do Bot
def bot():
    try:
        #Captura elementos html Zap Web
        zap_info_json = get_zap_info()
        zap_info = json.loads(zap_info_json)
        bolinha_notificacao_raw = zap_info[0]
        bolinha_notificacao = extract_value(bolinha_notificacao_raw)
        contato_cliente = zap_info[1]
        caixa_msg = zap_info[2]
        msg_cliente = zap_info[3]

        #Interage Tela Zap p/ Ler Msg
        bolinha = driver.find_element(By.CLASS_NAME,bolinha_notificacao)
        bolinha = driver.find_elements(By.CLASS_NAME,bolinha_notificacao)
        clica_bolinha = bolinha[-1]
        acao_bolinha = webdriver.ActionChains(driver)
        acao_bolinha.move_to_element_with_offset(clica_bolinha,0,-20)
        acao_bolinha.click()
        acao_bolinha.perform()
        acao_bolinha.click()
        acao_bolinha.perform()

        #Lê novas mensagens
        todas_as_msg = driver.find_elements(By.CLASS_NAME,msg_cliente)
        todas_as_msg_texto = [e.text for e in todas_as_msg]
        msg = todas_as_msg_texto[-1]

        #Interage com Openai
        resposta = responde(msg)

        # Copia a resposta para a área de transferência
        pyperclip.copy(resposta)

        #Responde no Zap e Fecha o chat
        campo_de_texto = driver.find_element(By.XPATH,caixa_msg)
        campo_de_texto.click()
        time.sleep(2)
        campo_de_texto.send_keys(Keys.CONTROL, 'v')
        time.sleep(1)
        campo_de_texto.send_keys(Keys.ENTER)
        time.sleep(2)

        #Fecha o contato
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
    except:
        pass

while True:
    bot()