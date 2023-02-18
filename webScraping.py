import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


'''
É necessario instalar a versão mais recente do ChromeDriver em:
https://chromedriver.chromium.org/

Deixe na pasta raiz do projeto
'''

def get_quotes(url, max_len_quote=120):
    quotes = []
    page_number = 1

    chrome_options = Options()
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)

    
    while True:
        current_url = f"{url}/{page_number}/"
        driver.get(current_url)
        time.sleep(1)

        # Caso não há mais páginas, o site irá para a primeira página, logo terminou o seu processo
        if page_number > 1 and driver.current_url != current_url:
            break

        # Pegando as tags
        html = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div[2]')
        soup = BeautifulSoup(html.get_attribute('outerHTML'), 'html.parser')

        quote_tags = soup.find_all('p', class_='frase fr')
        author_tags = soup.find_all('span', class_='author-name')

        # Caso não encontre nenhuma tag, a página deste autor não existe
        if len(quote_tags) <= 0 or len(author_tags) <= 0:
            return False

        for quote, author in zip(quote_tags, author_tags):
            #Tirando as frases longas
            if not(max_len_quote) or len(quote.text) <= max_len_quote:
                quotes.append({
                    'frase': quote.text,
                    'autor': author.text
                })
        page_number += 1

    driver.quit()
    return quotes


def main():
    autor = input('Digite o nome do autor: ')
    url = f'''https://www.pensador.com/autor/{'_'.join(autor.lower().split(" "))}'''
    filename = url.split('/')[-1]
    quotes = get_quotes(url)

    if quotes:
        with open(f'json/{filename}.json', 'w') as f:
            json.dump(quotes, f)
        print(f'--------\n{autor} Completo\n--------')
    else:
        print('Nome de autor não encontrado :(')

if __name__ == "__main__":
    while True:
        main()