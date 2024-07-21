Previsão do Tempo e Envio Diário por Email
Este projeto em Python utiliza Selenium para obter a previsão do tempo de um site e envia um email diário com as informações coletadas.

Requisitos
Python 3.x
Selenium
Decouple
schedule
Instalação
Clone o repositório:

bash
Copiar código
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
Crie e ative um ambiente virtual:

bash
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Configure suas credenciais de email criando um arquivo .env na raiz do projeto:

makefile
Copiar código
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha
RECIPIENT_EMAIL=email_destinatario@gmail.com
Uso
Execute o script principal:
bash
Copiar código
python script.py
O script será executado diariamente às 8:00 AM, coletando a previsão do tempo e enviando um email com as informações.

Estrutura do Código
iniciar_driver(): Inicializa o driver do Chrome com opções específicas.
obter_previsao_tempo(driver): Coleta a previsão do tempo atual.
rolar_pagina(driver, posicao): Rola a página para a posição especificada.
obter_temperaturas_dia(driver, dia): Coleta as temperaturas máxima e mínima dos próximos dias.
envio_de_email(previsao, temperatura, temperaturas_dias): Envia um email com a previsão do tempo.
main(): Função principal que orquestra a coleta de dados e envio de email.
Agendamento diário com schedule.
Licença
Este projeto está licenciado sob a MIT License.
