from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
import selenium.webdriver.firefox
from selenium.webdriver.firefox.options import Options as fireOptions
from time import sleep
import threading
import json
import schedule
from datetime import datetime
# Importar a classe WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
# Importar a classe que contém as funções e aplicar um alias
from selenium.webdriver.support import expected_conditions as EC
# Importar classe para ajudar a localizar os elementos
from selenium.webdriver.common.by import By
import os
import requests

# Parameters
WP_LINK = 'https://web.whatsapp.com'

# XPATHS
CONTACTS = '//*[@id="main"]/header/div[2]/div[2]/span'
SEND = '//*[@id="main"]/footer/div[1]/div[3]'
MESSAGE_BOX = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
NEW_CHAT = '//*[@id="side"]/header/div[2]/div/span/div[2]/div'
FIRST_CONTACT = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div'
SEARCH_CONTACT = '//*[@id="app"]/div/div/div[2]/div[1]/span/div/span/div/div[1]/div/label/div/div[2]'
SEARCH_OR_INI_CHAT = "//*[contains(@class, '_3FRCZ')]"
CLIP_ICON = "//div[@title='Anexar']"
IMAGE_BUTTON = "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"
SEND_IMAGE = "//*[contains(@class, '_6TTaR')]"


class WhatsApp:
    def __init__(self):
        with open(os.path.join('data', 'groups.json'), 'r') as json_file:
            self.groups = json.load(json_file)

        # campanhas agendadas
        self.scheduled_campaigns = []

        self.driver = self._setup_driver()
        self.driver.get(WP_LINK)
        print("Por favor faça a leitura do QR Code")
        # input()

    @staticmethod
    def _setup_driver():
        # chrome_options = Options()
        # chrome_options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # chrome_options.add_argument('lang=pt-br')
        # chrome_options.add_argument(
        #     f'--user-data-dir=C:\\Users\\mario\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 1')
        # chrome_options.add_argument("disable-infobars")
        # driver = webdriver.Chrome(
        # chrome_options=chrome_options, executable_path=r'.\\chromedriver.exe')
        fire_profile = os.environ['APPDATA'] + \
            '\\Mozilla\\Firefox\\Profiles\\gc36qc2n.default-release'
        firefox_options = fireOptions()
        firefox_options.headless = False
        driver = webdriver.Firefox(fire_profile, executable_path=(
            os.path.dirname(os.path.realpath(__file__)) + '\\geckodriver'), options=firefox_options)
        return driver

    def _get_element(self, xpath, attempts=5, _count=0):
        '''Safe get_element method with multiple attempts'''
        try:
            element = self.driver.find_element_by_xpath(xpath)
            #print('Found element!')
            return element
        except Exception as e:
            if _count < attempts:
                sleep(1)
                #print(f'Attempt {_count}')
                self._get_element(xpath, attempts=attempts, _count=_count+1)
            else:
                print("Element not found")

    def _click(self, xpath):
        el = self._get_element(xpath)
        el.click()

    def _send_keys(self, xpath, message):
        el = self._get_element(xpath)
        el.send_keys(message)

    def write_message(self, message):
        '''Write message in the text box but not send it'''
        self._click(MESSAGE_BOX)
        self._send_keys(MESSAGE_BOX, message)

    def _paste(self):
        el = self._get_element(MESSAGE_BOX)
        el.send_keys(Keys.SHIFT, Keys.INSERT)

    def _newline(self):
        el = self._get_element(MESSAGE_BOX)
        el.send_keys(Keys.SHIFT, Keys.ENTER)

    def send_message(self, message):
        '''Write and send message'''
        self.write_message(message)
        self._click(SEND)

    def get_group_numbers(self):
        '''Get phone numbers from a whatsapp group'''
        try:
            el = self.driver.find_element_by_xpath(CONTACTS)
            return el.text.split(',')
        except Exception as e:
            print("Group header not found")

    def search_contact(self, keyword):
        '''Write and send message'''
        self._click(NEW_CHAT)
        self._send_keys(SEARCH_CONTACT, keyword)
        sleep(1)
        try:
            self._click(FIRST_CONTACT)
        except Exception as e:
            print("Contact not found")

    def get_all_messages(self):
        all_messages_element = self.driver.find_elements_by_class_name(
            '_12pGw')
        all_messages_text = [e.text for e in all_messages_element]
        return all_messages_text

    def get_last_message(self):
        all_messages = self.get_all_messages()
        return all_messages[-1]

    def hasXpath(self, xpath):
        try:
            self.driver.find_element_by_xpath(xpath)
            return True
        except:
            return False

    def CriaGrupo(self):
        # with open(os.path.join('data', 'groups.json'), 'r') as json_file:
        #     self.groups = json.load(json_file)
        # for grp in self.groups:
        # self.PesquisaContatoOuGrupo(grp['name'])

        wait = WebDriverWait(self.driver, 1800)
        # Nome do grupo no topo
        # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'DP7CM')]//span[text()='{}']".format(grp['name']))))
        # Apareça Você na lista de membros do grupo

        # Menu de opções
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[@title='Mais opções']")))
        self._click("//*[@title='Mais opções']")

        # Novo grupo
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[text()='Novo grupo']")))
        self._click("//div[text()='Novo grupo']")

        # Pesquisa de contato
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_17ePo')]")))
        self._click("//*[contains(@class, '_17ePo')]")

        # Digitando o Nome do contato
        self._send_keys("//*[contains(@class, '_17ePo')]",
                        "Mário Guimarães Beta")
        self._send_keys("//*[contains(@class, '_17ePo')]", Keys.ENTER)

        # Botão de próximo
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_3y5oW')]")))
        self._click("//*[contains(@class, '_3y5oW')]")

        # Nome do contato
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_3WjMU')]//*[contains(@class, '_3FRCZ')]")))
        self._click(
            "//*[contains(@class, '_3WjMU')]//*[contains(@class, '_3FRCZ')]")

        # Imagem do grupo
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_2H1bg')]")))
        self._click("//*[contains(@class, '_2H1bg')]")

        # Carregar foto
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, 'I4jbF')]/li[2]")))
        self._get_element("//*[contains(@class, '_3X-61')]/input").send_keys(
            r"E:\1-Projetos\FUNIL PRODUTO\Lançamentos\Semana Riqueza Digital\Identidade Visual\grupo-whatsapp.png")

        # Send image
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_3qMYG')]")))
        self._click("//*[contains(@class, '_3qMYG')]")

        # Digitando o Nome do grupo
        self._send_keys(
            "//*[contains(@class, '_3WjMU')]//*[contains(@class, '_3FRCZ')]", "RIQUEZA DIGITAL a")
        self._send_keys(
            "//*[contains(@class, '_3WjMU')]//*[contains(@class, '_3FRCZ')]", Keys.ENTER)

        # parei aqui

        # Selecionar o grupo no topo
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(@class, '_33QME')]")))
        self._click("//*[contains(@class, '_33QME')]")

    # def MudarNomeGrupo(self):
    #     for grp in self.groups:
    #         # Recuperando o grupo (clicando)
    #         grupo = self.driver.find_element_by_xpath(f"//*[@title='{grp.name}']")
    #         sleep(1)
    #         grupo.click()

    #         # Nome do grupo na parte superior
    #         grupo = self.driver.find_element_by_xpath(f"//*[contains(@class, 'DP7CM')]//span[text()='{grp.name}']")
    #         sleep(1)
    #         grupo.click()

    #         # Botão lápis editar nome do grupo
    #         grupo = self.driver.find_element_by_xpath(f"//*[@title='Editar']/span")
    #         sleep(1)
    #         grupo.click()

    #         # Recuperando a área para digitar o texto
    #         group_name = self.driver.find_element_by_xpath(f"//div[text()='{grp.name}']")
    #         sleep(1)
    #         group_name.click()
    #         group_name.clear()
    #         # Digita o novo nome
    #         action = ActionChains(self.driver)
    #         action.send_keys(Keys.BACKSPACE)
    #         action.perform()
    #         sleep(1)
    #         group_name.send_keys('Keys.BACKSPACE')
    #         # Clicar no icone confirmar
    #         btn_send = self.driver.find_element_by_xpath("//*[@title='Clique para salvar, Esc para cancelar']")
    #         sleep(1)
    #         btn_send.click()
    #         # Esperar 5 segundos para passar para o próximo grupo
    #         sleep(2)

    def PesquisaContatoOuGrupo(self, nome):
        # campo de pesquisa
        wait = WebDriverWait(self.driver, 1800)
        wait.until(EC.element_to_be_clickable((By.XPATH, SEARCH_OR_INI_CHAT)))
        # encontrar o contato / grupo
        self._send_keys(SEARCH_OR_INI_CHAT, nome)
        self._send_keys(SEARCH_OR_INI_CHAT, Keys.ENTER)

    def Campain(self, campain):
        print('campain = {}'.format(campain['id']))
        send = campain['send']
        for group in self.groups:
            if group['id'] in campain['to']:
                self.PesquisaContatoOuGrupo(group['name'])

                wait = WebDriverWait(self.driver, 1800)
                # Aguarda a Caixa de envio de mensagem estar pronta para ser utilizada
                wait.until(EC.element_to_be_clickable((By.XPATH, MESSAGE_BOX)))

                messageBox = self._get_element(MESSAGE_BOX)
                for content in send:
                    if content['type'] == 'text':
                        messageBox.click()
                        for text in content['text']:
                            messageBox.send_keys(text, Keys.SHIFT, Keys.ENTER)
                        self._click(SEND)
                    if content['type'] == 'group_key':
                        value = group['keys'][content['key']]
                        messageBox.click()
                        messageBox.send_keys(value)
                        self._click(SEND)
                    if content['type'] in ['image', 'document', 'video', 'audio']:
                        path = content['path']
                        self._click(CLIP_ICON)
                        self._get_element(IMAGE_BUTTON).send_keys(path)
                        wait.until(EC.element_to_be_clickable(
                            (By.XPATH, SEND_IMAGE)))
                        self._click(SEND_IMAGE)

        return schedule.CancelJob

    def Campains(self):
        with open(os.path.join('data', 'campains.json'), 'r') as json_file:
            self.campains = json.load(json_file)
        today = datetime.today().strftime('%d/%m/%Y')
        for campain in self.campains:
            if (not campain['id'] in self.scheduled_campaigns) and (campain['date'] == today):
                now = datetime.now()
                hour_minute = campain['time'].split(':')
                time_to_execute = now.replace(hour=int(hour_minute[0]), minute=int(
                    hour_minute[1]), second=0, microsecond=0)
                if now < time_to_execute:
                    schedule.every().day.at(campain['time']).do(
                        self.Campain, campain)
                    self.scheduled_campaigns.append(campain['id'])

    def EnviarMensagemSuporte(self):
        self.search_contact('Mário Guimarães Beta')
        sleep(2)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.send_message("Current Time = " + current_time)

    def EnviarSaudacao(self):
        hora_atual = datetime.now().hour

        if hora_atual < 12:
            mensagem = 'Bom dia!'
        elif 12 <= hora_atual < 18:
            mensagem = 'Boa tarde!'
        else:
            mensagem = 'Boa noite!'

        self.send_message(mensagem)

    def EnviarMensagemBoasVindas(self):
        for grp in self.groups:
            for number in grp['new_numbers']:
                number_without_spaces = number.strip()
                # encontrar pessoa
                contact_url = "https://web.whatsapp.com/send?phone={}".format(
                    number_without_spaces.replace("+", ""))
                self.driver.get(contact_url)
                wait = WebDriverWait(self.driver, 1800)
                wait.until(EC.element_to_be_clickable((By.XPATH, MESSAGE_BOX)))
                while self.hasXpath("//*[@class='_2J60S' and contains(@title,'Carregando mensagens')]"):
                    sleep(1)

                # se nunca falei com a pessoa
                if not self.hasXpath('//*[contains(@class,"message-out focusable-list-item")]'):
                    # Bom dia! / Boa tarde! / Boa noite!
                    self.EnviarSaudacao()

                    el = self._get_element(MESSAGE_BOX)
                    # envia mensagem de boas-vindas
                    with open(os.path.join('data', 'welcome.json'), 'r') as json_file:
                        boas_vindas = json.load(json_file)
                    for message in boas_vindas:
                        el.click()
                        for text in message:
                            el.send_keys(text)
                            el.send_keys(Keys.SHIFT, Keys.ENTER)
                        self._click(SEND)

                grp['new_numbers'].remove(number)
                # atualizar o groups.json
                with open(os.path.join('data', 'groups.json'), 'w') as json_file:
                    json.dump(self.groups, json_file, indent=4)

            # encontrar o grupo para não ficar com a última pessoa ativa, dentro do chat com a pessoa
            self.PesquisaContatoOuGrupo(grp['name'])

        # self.search_contact('Mário Guimarães Beta')
        # sleep(2)

    def MonitoraGrupo(self):
        with open(os.path.join('data', 'groups.json'), 'r') as json_file:
            self.groups = json.load(json_file)
        for grp in self.groups:
            self.PesquisaContatoOuGrupo(grp['name'])

            wait = WebDriverWait(self.driver, 1800)
            # Nome do grupo no topo
            # wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'DP7CM')]//span[text()='{}']".format(grp['name']))))
            # Apareça Você na lista de membros do grupo
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//*[@class='_2ruUq _3xjAz']//span[contains(text(),'Você')]")))
            # obter números dos membros
            group_numbers = self.get_group_numbers()
            numbers_group_now = [
                number for number in group_numbers if "+" in number]

            # números que saíram do grupo
            numbers_left_the_group = list(
                set(grp['numbers_group']) - set(numbers_group_now))
            grp['numbers_left'] = grp['numbers_left'] + numbers_left_the_group

            new_numbers = list(set(numbers_group_now) -
                               set(grp['numbers_group']))
            # new_numbers = [number for number in new_numbers if "+" in number]

            grp['numbers_group'] = numbers_group_now

            grp['occuped_seats'] = len(group_numbers)
            grp['new_numbers'] = list(set(grp['new_numbers'] + new_numbers))
            grp['new_numbers'] = list(
                set(grp['new_numbers']) - set(grp['numbers_left']))
            # atualizar o groups.json
            with open(os.path.join('data', 'groups.json'), 'w') as json_file:
                json.dump(self.groups, json_file, indent=4)

    def ApiAtualizaGrupos(self):

        # Colunas que podem ser atualizadas
        # {
        #     "name": "DESTRAVAR TESTE a",        NOME DO GRUPO (MÁXIMO 25 CARACTERES)
        #     "seats": 200,                       LUGARES DISPONÍVEIS (CONTANDO COM OS ADMINS)
        #     "occuped_seats": 0                  LUGARES OCUPADOS (CONTANDO COM OS ADMINS)
        # }

        # url = "https://marioguimaraes.com.br/automation/api/wagroups/1"
        urlApi = "http://localhost/laravel-tips/adminlte/public/api/wagroups/{}"

        with open(os.path.join('data', 'groups.json'), 'r') as json_file:
            self.groups = json.load(json_file)
        for grp in self.groups:
            group_data = {
                "occuped_seats": grp['occuped_seats']
            }
            url = urlApi.format(grp['id'])
            response = requests.put(url=url, json=group_data)

            if response.status_code >= 200 and response.status_code <= 209:
                # Sucesso
                print('Status Code', response.status_code)
                print('Reason', response.reason)
                print('Texto', response.text)
                print('JSON', response.json())
            else:
                # Erros
                print('Status Code', response.status_code)
                print('Reason', response.reason)
                print('Texto', response.text)

    def scheduler_jobs(self):
        # schedule.every(1).minutes.do(self.Campains)
        schedule.every(1).minutes.do(self.MonitoraGrupo)
        schedule.every(2).minutes.do(self.EnviarMensagemBoasVindas)
        # schedule.every(5).minutes.do(self.ApiAtualizaGrupos)

        while 1:
            schedule.run_pending()
            sleep(1)

    def end(self):
        sleep(5)
        self.driver.close()


bot = WhatsApp()
wait = WebDriverWait(bot.driver, 1800)
wait.until(EC.element_to_be_clickable((By.XPATH, SEARCH_OR_INI_CHAT)))

# bot.MudarNomeGrupo()
# bot.EnviarMensagemSuporte()

# with open(os.path.join('data', 'campains.json'), 'r') as json_file:
#     campains = json.load(json_file)
# bot.Campain(campains[0])
# sleep(10)

# bot.CriaGrupo()

# # bot.Campains()
bot.MonitoraGrupo()
# bot.EnviarMensagemBoasVindas()
# # bot.ApiAtualizaGrupos()

# if __name__ == "__main__":
#     bot.scheduler_jobs()

# bot.end()
