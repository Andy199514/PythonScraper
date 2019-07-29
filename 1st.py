# -*- coding: utf-8 x

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from textblob import TextBlob

optionsWD = webdriver.ChromeOptions()
optionsWD.add_argument("--incognito")
browser = webdriver.Chrome('C:/Users/Andy/.spyder-py3/chromedriver.exe',options=optionsWD)
browser.get("https://www.imdb.com/title/tt8364368/reviews")

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

html = browser.page_source
soup = BeautifulSoup(html, 'html5lib')

i = 1
j = 1
comment_polar = 0.0
RateValueAdj = 0

for content in soup.find_all('div', attrs={"class":"actions text-muted"}):
    content.replace_with('')
comments = soup.find_all('div', attrs={"class":"content"})
for comment in comments:
         comments = comment.text
         with open("comments.txt", "a", encoding="utf-8") as file:
             file.write(comments)
         file.close()
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
         print("Pocet : ", i,"Upravene : ", RateValueAdj)
         i += 1

for ratingValue in soup.find_all('span', attrs={'class': 'point-scale'}):
             ratingValue.replace_with('')
for rating in soup.find_all('div', attrs={'class': 'ipl-ratings-bar'}):
             ratingText = rating.text
             rateInt = int(ratingText)
             print("PocetPV", j,"PageValue: ",rateInt)
             j+=1
             
browser.quit() 
print("Done.")
""" 


Created on Thu Oct  4 22:46:02 2018

@author: Andrej
"""

