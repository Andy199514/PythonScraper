# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob

## NASTAVENIA 
optionsWD = webdriver.ChromeOptions()
optionsWD.add_argument("--incognito")
browser = webdriver.Chrome('C:/Users/Andy/.spyder-py3/chromedriver.exe',options=optionsWD)
browser.get("https://www.imdb.com/title/tt6343314/reviews")

##FUNKCIE 
def loadMore():
    x = True
    wait = WebDriverWait(browser, 5)
    while x == True: 
        try:
            wait.until(EC.element_to_be_clickable((By.ID, 'load-more-trigger')))
            buttons = browser.find_elements_by_xpath("//button[@id='load-more-trigger']")
            for button in buttons:
                wait.until(EC.element_to_be_clickable((By.ID, 'load-more-trigger')))
                if button.text == "Load More":
                   button.click()
                elif button.text != "Load More" :
                    x = False
        except Exception as e:
            print(e)
            break
    print("Load More:", x)
    
def analyze(soup):
    i = 1
    for comment in soup.find_all('div', attrs={"class":"text show-more__control"}):
        comments = "\n".join(comment.find_all(text=True))
        sentAnalysis = TextBlob(comments)
        with open("comments.txt", "a", encoding="utf-8") as file:
            file.write(comments)
        file.close()
        print(i, sentAnalysis.sentiment)
        i += 1
    
##TELO PROGRAMU
loadMore()
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
analyze(soup)
browser.quit() 
print("Done.")
