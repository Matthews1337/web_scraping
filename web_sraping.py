

from selenium import webdriver
from selenium.webdriver.common.keys import Keys  #-> biblioteca para poder dar "enter"


# ABRIR O NAVEGADOR

navegador = webdriver.Chrome()



# PESQUISAR A COTAÇAO DO DOLAR

navegador.get("https://www.google.com.br/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do dolar")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)




cotacao_dolar = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')



print(cotacao_dolar)


# PESQUISAR A COTAÇAO DO EURO

navegador.get("https://www.google.com.br/")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys("cotação do euro")

navegador.find_element('xpath', '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)




cotacao_euro = navegador.find_element('xpath', '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')



print(cotacao_euro)




# PESQUISAR A COTAÇAO DO OURO

navegador.get("https://www.melhorcambio.com/ouro-hoje#:~:text=O%20valor%20do%20grama%20do,em%20R%24%20315%2C12.")

cotacao_ouro = navegador.find_element('xpath', '//*[@id="comercial"]').get_attribute('value')

cotacao_ouro = cotacao_ouro.replace(",", ".")  #-> mudar a "," pelo "."

print(cotacao_ouro)


import pandas as pd

# IMPORTAR A BASE DE DADOS E ATUALIZAR A BASE DE DADOS
  
tabela = pd.read_excel(r"excel\Produtos.xlsx")

#print(tabela)


# RECALCULAR OS VALORES DA TABELA

# atualizar a cotaçao

dolar = tabela["Moeda"] == 'Dólar'

tabela.loc[dolar, "Cotação"] = float(cotacao_dolar)


euro= tabela["Moeda"] == 'Euro'

tabela.loc[euro, "Cotação"] = float(cotacao_euro)


ouro = tabela["Moeda"] == 'Ouro'

tabela.loc[ouro, "Cotação"] = float(cotacao_ouro)



# preço de compra = cotação * preço original


tabela['Preço de Compra'] = tabela['Cotação'] * tabela['Preço Original']



# preço de venda = preço de compra * margem

tabela["Preço de Venda"] = tabela["Preço de Compra"] * tabela["Margem"]

tabela["Preço de Venda"] = tabela["Preço de Venda"].map("R$ {:.2f}".format)

print(tabela)

# EXPORTAR A BASE ATUALIZADA

tabela.to_excel(r"excel\Produtos_2.xlsx", index=False)