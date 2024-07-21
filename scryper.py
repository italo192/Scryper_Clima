from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
import schedule
import time
from decouple import config

def iniciar_driver():
    chrome_options = Options()
    arguments = ['--lang=pt-BR', '--window-size=800,600', '--incognito']
    for argument in arguments:
        chrome_options.add_argument(argument)
        
    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
    })

    driver = webdriver.Chrome(options=chrome_options)
    return driver

def obter_previsao_tempo(driver):
    driver.get('https://www.tempo.com/cascavel.htm')
    sleep(10)
    
    try:
        condicao_atual = driver.find_element(By.CSS_SELECTOR, 'span[class="descripcion"]')
        forecast = condicao_atual.text
        print(f"A previsão do tempo é: {forecast}")
        
        temperatura = driver.find_element(By.CSS_SELECTOR, 'span[class="dato-temperatura changeUnitT"]')
        graus = temperatura.text
        print(f"A temperatura atual é: {graus}")
        
        return forecast, graus
        
    except NoSuchElementException as e:
        print(f"Erro ao obter dados: {e}")
        return None, None

def rolar_pagina(driver, posicao):
    driver.execute_script(f"window.scrollTo(0, {posicao});")

def obter_temperaturas_dia(driver, dia):
    try:
        parent_element = driver.find_element(By.CSS_SELECTOR, f'li.grid-item.dia.d{dia}')
        dia_element = parent_element.find_element(By.CSS_SELECTOR, 'span[class="text-0"]')
        dia_texto = dia_element.text
        
        max_temp_element = parent_element.find_element(By.CSS_SELECTOR, 'span.max.changeUnitT')
        min_temp_element = parent_element.find_element(By.CSS_SELECTOR, 'span.min.changeUnitT')

        max_temp = max_temp_element.text
        min_temp = min_temp_element.text

        print(f"Temperatura máxima do dia {dia_texto}: {max_temp}")
        print(f"Temperatura mínima do dia {dia_texto}: {min_temp}")
        return dia_texto, max_temp, min_temp
    except NoSuchElementException:
        print(f"Elemento do dia {dia} não encontrado. Verifique se o seletor CSS está correto ou se o elemento está presente na página.")
        return None, None, None

def envio_de_email(previsao, temperatura, temperaturas_dias):
    # Credenciais do email
    my_email = config('EMAIL_USER')
    my_password = config('EMAIL_PASS')
    recipient_email = config('RECIPIENT_EMAIL').split(',')

    # Configurações do servidor SMTP
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # Adicionar conteúdo HTML
    html_content = f"""<!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Previsão do Tempo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
                width: 100% !important;
                -webkit-text-size-adjust: 100%;
                -ms-text-size-adjust: 100%;
            }}
            .email-container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding: 10px 0;
            }}
            .header h1 {{
                margin: 0;
                color: #333333;
            }}
            .weather-forecast {{
                padding: 20px 0;
            }}
            .day-forecast {{
                width: 100%;
                border-bottom: 1px solid #eeeeee;
                padding: 15px 0;
            }}
            .day-forecast:last-child {{
                border-bottom: none;
            }}
            .day, .temperature, .condition {{
                padding: 5px 0;
            }}
            .footer {{
                text-align: center;
                padding: 10px 0;
                color: #999999;
                font-size: 12px;
            }}
            @media (max-width: 600px) {{
                .day-forecast {{
                    display: block;
                }}
                .day, .temperature, .condition {{
                    display: block;
                    width: 100% !important;
                    text-align: left !important;
                    padding: 5px 0;
                }}
                .condition {{
                    text-align: right !important;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Previsão do Tempo</h1>
            </div>
            <div class="weather-forecast">
                <table cellpadding="0" cellspacing="0" border="0" width="100%">
                    <tr class="day-forecast">
                        <td class="day" style="font-weight: bold; color: #333333; width: 33%;">Hoje</td>
                        <td class="temperature" style="color: #ff6600; text-align: center; width: 33%;">{temperatura}</td>
                        <td class="condition" style="color: #666666; text-align: right; width: 33%;">{previsao}</td>
                    </tr>
                    {"".join([f'<tr class="day-forecast"><td class="day" style="font-weight: bold; color: #333333; width: 33%;">{dia}</td><td class="temperature" style="color: #ff6600; text-align: center; width: 33%;">Máx: {max_temp} / Mín: {min_temp}</td><td class="condition" style="color: #666666; text-align: right; width: 33%;"></td></tr>' for dia, max_temp, min_temp in temperaturas_dias])}
                </table>
            </div>
            <div class="footer">
                © 2024 Previsão do Tempo. Destrava Dev Desafio 1.
            </div>
        </div>
    </body>
    </html>"""

    # Enviar e-mail usando Python
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(my_email, my_password)

        for recipient in recipient_email:
            message = MIMEMultipart()
            message["From"] = my_email
            message["To"] = recipient
            message["subject"] = "Enviando e-mail usando Python"
            message.attach(MIMEText(html_content, "html"))

            server.sendmail(my_email, recipient, message.as_string())
            print(f"E-mail enviado para {recipient} com sucesso")

        server.quit()
    except Exception as e:
        print(f"Erro no envio do e-mail: {e}")

def main():
    driver = iniciar_driver()
    previsao, temperatura = obter_previsao_tempo(driver)
    
    sleep(5)
    rolar_pagina(driver, 700)
    
    temperaturas_dias = []
    for dia in range(2, 5):
        dia_texto, max_temp, min_temp = obter_temperaturas_dia(driver, dia)
        temperaturas_dias.append((dia_texto, max_temp, min_temp))
    
    envio_de_email(previsao, temperatura, temperaturas_dias)
    
    # Fechar o navegador
    driver.quit()

if __name__ == "__main__":
    # Agendar o envio de e-mail diário às 8:00 AM
    schedule.every().day.at("08:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
