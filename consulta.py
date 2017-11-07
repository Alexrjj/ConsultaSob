from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import selenium
from selenium import webdriver

url = 'http://gomnet.ampla.com/'
username = ''
password = ''

driver = webdriver.Chrome()
if __name__ == '__main__':
    driver.get(url)
    # Faz login no sistema
    uname = driver.find_element_by_name('txtBoxLogin')
    uname.send_keys(username)
    passw = driver.find_element_by_name('txtBoxSenha')
    passw.send_keys(password)
    submit_button = driver.find_element_by_id('ImageButton_Login').click()

    # Procura o menu "Obras" e clica no submenu "Consulta de Obras"
    selenium.webdriver.common.action_chains.ActionChains(driver)
    menu = driver.find_element_by_xpath('//*[@id="ctl00_Menu_GomNetn0"]/table/tbody/tr/td[1]/a')
    hidden_submenu = driver.find_element_by_xpath('//*[@id="ctl00_Menu_GomNetn10"]/td/table/tbody/tr/td/a')
    webdriver.ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()

    # Insere o número da Sob em seu respectivo campo e realiza a busca
    sob = driver.find_element_by_id('ctl00_ContentPlaceHolder1_TextBox_NumSOB')

    with open('sobs.txt') as data:
        datalines = (line.rstrip('\r\n') for line in data)
        for line in datalines:
            driver.find_element_by_id('ctl00_ContentPlaceHolder1_TextBox_NumSOB').clear()
            sob = driver.find_element_by_id('ctl00_ContentPlaceHolder1_TextBox_NumSOB')
            sob.send_keys(line)
            driver.find_element_by_id('ctl00_ContentPlaceHolder1_ImageButton_Enviar').click()
            try:
                # Verifica se a sob está no status desejado
                vistoria = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Gridview_GomNet1"]/tbody/tr[2]/td[3][contains(text(), "Vistoria")]')
                if vistoria.is_displayed():
                    log = open("SobsVistoria.txt", "a")
                    log.write(line + "\n")
                    log.close()
            except NoSuchElementException:
                continue
