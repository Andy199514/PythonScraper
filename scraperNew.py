from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from textblob import TextBlob

#################### NASTAVENIA #########################
optionsWD = webdriver.ChromeOptions()
optionsWD.add_argument("--incognito")
browser = webdriver.Chrome('C:/Users/Andy/.spyder-py3/chromedriver.exe') 
browser.get("https://www.imdb.com/title/tt6343314/reviews")

#################### FUNKCIE ############################
#def loadMore():
    
    
    
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
    
#################### TELO ###############################
#loadMore()
x = 0
while x < 24: # Zmenit na kolko krat ma kliknut na Load More, True - komplet web
        try:
            WebDriverWait(browser, 5)
            buttons = browser.find_elements_by_xpath("//button[@id='load-more-trigger']")
            for button in buttons:
                WebDriverWait(browser, 5)
                if button.text == "Load More":
                   button.click()
                   x += 1
        
                
        except Exception as e:
            print(e)
            break
            
        
                   
            
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
analyze(soup)
browser.quit() 
print("Done.")