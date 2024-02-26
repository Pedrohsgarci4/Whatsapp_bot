"""

Esse bot esta simplificado( sem funcionalidades de responder a pedidos de previsão do tempo,
valores de moedas, integrações com APIs, etc... ppois ainda estou finalizando essas funcionalidades). 
Peço desculpas por qualquer erro presente no código e se possivel gostaria de receberr feedback
sobre o bot

"""





from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time



class WhatsappBot:
    def __init__(self, path, conversas):
        
        options = webdriver.ChromeOptions()
        selenium_service = Service(path)
        options.add_argument('lang=pt-br')
        options.headless = True

        self.driver = webdriver.Chrome(service=selenium_service, options=options)
        self.driver.get('https://web.whatsapp.com/?lang=pt_BR')
        WebDriverWait(self.driver, 40).until(EC.title_contains("WhatsApp"))  
        # Aguarda até que a página do WhatsApp seja carregada
        time.sleep(3)

    def Enviar_Mensagem(self, mensagem, conversa):
    
        try:
            print("----Iniciando----")

            print(f'----Enviando mensagem para {conversa}')

            conversa = WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, f"//span[@title='{conversa}']"))
                )
            conversa.click()

            # Espera até que o campo de mensagem esteja visível
            chat_xpath = "//*[@id='main']/footer/div[1]/div/span[2]/div/div[2]/div[1]"
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, chat_xpath))
            )

            # Enviar a mensagem pressionando Enter
            chat = self.driver.find_element(By.XPATH, chat_xpath)
            chat.send_keys(mensagem + Keys.RETURN)

            # Aguarda um momento para garantir que a mensagem seja enviada
            time.sleep(2)

        except:
            print(f"Erro ao enviar mensagem para {conversa}")

        print("----Finalizando----")

    def Checa_Mensagem(self, conversas_permitidas):
        """
        conversas_permitidas -> Lista de conversas que podem ser respondidas
        """
        print("----Checando novas mensagens----")
        
        
            
        # Esperando as conversas serem carregadas
        lista = WebDriverWait(self.driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Lista de conversas"]'))
        )
        # Separando as conversas
        conversas = lista.find_elements(By.CSS_SELECTOR, '[role="listitem"]')

        # Guardando o nome das que receberam notificação 
        conversas_filtradas = [conversa.find_element(By.CLASS_NAME, "_21S-L").text for conversa in conversas if conversa.find_elements(By.CLASS_NAME, "_2H6nH") ]
        print(conversas_filtradas)
        for nome in conversas_filtradas:
            # Checando quais podem ser monitoradas
            if nome in conversas_permitidas:
                print(f'Checando conversa: {nome}')
  
                # Clicando na conversa
                elemento = self.driver.find_element(By.XPATH, f"//span[@title='{nome}']")
                elemento.click()

                # Armazenando o elemento em que estãos as mensagens
                mensagens = self.driver.find_element(By.CSS_SELECTOR, '[role="application"]')

                # Armazenando as mensagens
                mensagens = self.driver.find_elements(By.CSS_SELECTOR, 'div.row[role="row"]')

                for index, mensagem in enumerate(mensagens):
                    if mensagem.find_elements(By.CLASS_NAME, '_1Yy5A'):
                        # Armazenando novamente só as mensagens depois da notificação
                        # de nova mensagem
                        mensagens = mensagens[index+1:]

                        textos = []
                        for mensagem in mensagens:
                            try:
                                text = mensagem.find('div', class_='cm280p3y').span.span.text

                                textos.append(text)

                            except:
                                # Provavelmente fig ou midia sem msg de texto
                                pass
                                
                        return textos
                                
                            
                    


    def Enviar_midia(self, conversa, path_midia):
        
        print(f'----Enviando mensagem para {conversa}')

        elemento = self.driver.find_element(By.XPATH, f"//span[@title='{conversa}']")
        elemento.click()
        
        self.driver.find_element_by_css_selector("span[data-icon='clip']").click()  

        mensagem = self.driver.find_element_by_css_selector("input[type='file']")
        mensagem.send_keys(path_midia)          

        time.sleep(3)
        send = self.driver.find_element_by_css_selector("span[data-icon='send']")
        send.click() 

# Exemplo de uso
bot = WhatsappBot("/home/pedro/tutorials/chromedriver_linux64/chromedriver", ["Bot do zap zap"])
mensagens = bot.Checa_Mensagem("Grupo teste")

