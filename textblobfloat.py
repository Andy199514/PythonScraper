# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob
import matplotlib.pyplot as plt
import pandas as pd


## NASTAVENIA 
optionsWD = webdriver.ChromeOptions()
optionsWD.add_argument("--incognito")
browser = webdriver.Chrome('C:/Users/Andy/.spyder-py3/chromedriver.exe',options=optionsWD)
browser.get("https://www.imdb.com/title/tt8364368/reviews")

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
    print("Loading...")

def analyze(soup):
   i = 1
   j = 1
   comment_polar = 0.0
   RateValueAdj = 0
   List_Of_Values = []
   comments = []
   TBValues = []
   userValues = []
   review_no = []
   for content in soup.find_all('div', attrs={"class":"actions text-muted"}):
         content.replace_with('')
   comments = soup.find_all('div', attrs={"class":"content"})
   for comment in comments:
         comments = comment.text
         sentAnalysis = TextBlob(comments)
         comment_polar = sentAnalysis.sentiment.polarity
         if comment_polar >= -1.0 and comment_polar < -0.8 :
            RateValueAdj=0
         elif comment_polar >= -0.8 and comment_polar < -0.6 :
            RateValueAdj=1
         elif comment_polar >= -0.6 and comment_polar < -0.4 :
            RateValueAdj=2
         elif comment_polar >= -0.4 and comment_polar < -0.2 :
            RateValueAdj=3
         elif comment_polar >= -0.2 and comment_polar < 0.0 :
            RateValueAdj=4
         elif comment_polar == 0.0 :
            RateValueAdj=5
         elif comment_polar >= 0.0 and comment_polar < 0.2 :
            RateValueAdj=6
         elif comment_polar >= 0.2 and comment_polar < 0.4 :
            RateValueAdj=7
         elif comment_polar >= 0.4 and comment_polar < 0.6 :
            RateValueAdj=8
         elif comment_polar >= 0.6 and comment_polar < 0.8 :
            RateValueAdj=9
         else :
            RateValueAdj=10
         TBValues.append(RateValueAdj)
      ##   print("Pocet : ", i,"Upravene : ", RateValueAdj)
         i += 1
   for removeScale in soup.find_all('span', attrs={'class': 'point-scale'}):
             removeScale.replace_with('') 
   List_Of_Values = soup.find_all('div', attrs={'class': 'lister-item-content'})
   for ratingValue in List_Of_Values:
             userRate=ratingValue.next_element
             userRate1=userRate.next_element
             try:
              uR1_to_int=int(userRate1.text)
              userValues.append(uR1_to_int)
             except:
                  uR1_to_int = 0
                  userValues.append(uR1_to_int)
                  continue
             finally:
          ##    print("PocetPV", j,"PageValue: ",uR1_to_int)
              j+=1
              review_no.append(j)
            ##  print(len(review_no), len(userValues))
             
              
   graphData = {'x' : review_no, 'y1' : userValues, 'y2' : TBValues }          

   df = pd.DataFrame(data=graphData)

   plt.plot('x', 'y1', data=df, marker='o', linewidth=2)
   plt.plot('x', 'y2', data=df, linewidth=4)
   plt.legend()
   plt.savefig('test.png', dpi=100)
##TELO PROGRAMU
loadMore()
html = browser.page_source
'''
with open("page_source.txt","a",encoding="utf-8") as ps:
    ps.write(html)
ps.close()
'''
soup = BeautifulSoup(html, 'html.parser')
analyze(soup)
browser.quit() 
print("Done.")

                        