from selenium import webdriver
import sqlite3
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
import time
from collections import Counter


vall = 0

plataform = 'Pc'
conn = sqlite3.connect('documentis_html.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS documentis_html
             (id INTEGER PRIMARY KEY, url TEXT, html TEXT, plataform TEXT)''')

#iniciate the drive to navegate in web
def drive_iniciate():
    FFdriver = 'home/artur/Documentos/faculdade/RIW/gekodriver.exe'
    firefox = '/snap/firefox/2579/usr/lib/firefox/firefox'


    service = Service(executable_path = FFdriver)
    # Set up the Selenium webdriver
    driver = webdriver.Firefox(service = service, firefox_binary = firefox)

    return driver






# with the page open, get all inner html
def get_pages(vall, driver):
    # Navigate to the webpage
    driver.get(f'https://store.epicgames.com/pt-BR/browse?sortBy=releaseDate&sortDir=DESC&category=Game&count=100&start={vall}')
    time.sleep(5)
    # Extract the HTML from the webpage
    html = driver.page_source
    return html

#parse the html and gets all 'li' items
def parse_page(html):
    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')
    # jogos listados
    gameCards = soup.find_all("a","css-g3jcms")
    infos =[gameCards,soup]
    return infos

#in the list get all links
def get_all_links(infos):
    links = []
    gameCards = infos[0]
    soup = infos[1]
    for gameCard in gameCards:
        gamePageUrl = "https://store.epicgames.com/"+gameCard.get("href")
        links.append(str(gamePageUrl))
    return links

#compare twins queue to know how many links, and discard links that repeat in queue
def compare_queues(x, y):
    # Count the elements in the two queues
    counter_x = Counter(x)
    counter_y = Counter(y)

    # Find elements that appear exactly once in y
    unique_elements = []
    for element, count in counter_y.items():
         if count >= 1 and counter_x.get(element, 0) >=1:
            unique_elements.append(element)

    return unique_elements

     

#write all links in a .TXT
def write(list):

    with open('fe.txt', 'a') as f:
        for links in list:
            link = str(links)
            f.write(f'{links}\n')



#iniciate the code
def iniciate():
    i=0
    vall = 0
    while (i<19):
        driver = drive_iniciate()
        html = get_pages(vall, driver)
        infos = parse_page(html)
        links = get_all_links(infos)
        aux = links
        unique_items = compare_queues(links, aux)
        write(unique_items)
        i+=1
        vall+=100
        time.sleep(2)

        driver.quit()
    


#Close the Selenium webdriver

conn.close()

