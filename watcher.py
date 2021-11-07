from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from win10toast_click import ToastNotifier
from webbrowser import open_new_tab
from time import sleep


def open_url():
    open_new_tab(url)


url = open('link.txt').read()

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

toaster = ToastNotifier()

while True:
    driver.get(url)

    elements = []

    for i in BeautifulSoup(driver.page_source, 'lxml').find_all('div', attrs={'class': 'aditem-main--middle'}):
        element = {}
        price_tag = i.find_all('p', attrs={'class': 'aditem-main--middle--price'})
        if len(price_tag) == 1:
            element['price-tag'] = price_tag[0].text.replace('\n',
                                                             '').replace('                                         ', '')

        title = i.find_all('h2', attrs={'class': 'text-module-begin'})
        if len(title) == 1:
            element['title'] = title[0].text.replace('\n', '')
            link = title[0].find_all('a')
            if len(link) == 1:
                element['link'] = link[0].get('href')

        if element.get('price-tag') == "Zu verschenken":
            elements.append(element)

    if len(elements) != 0:
        toaster.show_toast("eBay Kleinanzeigen Watcher", "Ein kostenloses Element wurde gefunden",
                           duration=10, icon_path='images/icon.ico', threaded=True, callback_on_click=open_url)

    sleep(86400)
