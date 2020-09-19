from selenium import webdriver
import time,random,sqlite3,db,os,requests,urllib
from datetime import datetime,timedelta

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

db =db.dbCon()

connectToDb=True

driverChrome=webdriver.Chrome("chromedriver.exe")

def getStoryOfAccount(_link, _userId,_storyCount, driver=driverChrome):

    driver.get("https://www.storysaver.net/")
    driver.find_element_by_name("text_username").send_keys(_link)
    driver.find_element_by_id("StoryButton").click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'storyblock')))
    except TimeoutException:
        print("Loading took too much time!")
        driver.find_element_by_id("StoryButton").click()
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'storyblock')))
        except TimeoutException:
            print("Loading took too much time!")
            driver.find_element_by_id("StoryButton").click()
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'storyblock')))
            except TimeoutException:
                print("Loading took too much time!")
                driver.find_element_by_id("StoryButton").click()
    storyBlockDiv=driver.find_element_by_id("storyblock").find_elements_by_class_name("stylestory")

    if connectToDb:
        db.updateLastChecked(_userId, datetime.now())
    

    for i in reversed(storyBlockDiv):
        storyLink=i.find_element_by_id("StoryButton").get_attribute('href')
        try:
            #r=requests.get(storyLink)
            #_storySize=len(r.content)
            pass
        except :
            print("story size kontrol edilirken hata! link: "+str(storyLink))
            if connectToDb:
                db.updateLastChecked(_userId, datetime.now()-timedelta(days = 1))
        
        #isStoryExist=db.checkStoryUrlIfExsist(_storySize,_userId)
        isStoryExist=0
        if (isStoryExist==0):
            print("story kayıtlı değil")
            try:
                _storyCount+=1
                if connectToDb:
                    db.createDownloadStoryEntry(_userId,datetime.now(),storyLink,0,0)
                    db.updateStoryCountAndLastChecked(_userId, datetime.now(), _storyCount)
            except:
                print("kaydedilirken hata! userID: "+str(_userId))
                if connectToDb:
                    db.updateLastChecked(_userId, datetime.now()-timedelta(days = 1))
        else:
            print("story zaten kayıtlı amk")
 
i=0
for item in db.getAllUsers():
    lastCheckTime = datetime.strptime(item[3], "%Y-%m-%d %H:%M:%S.%f")
    i+=1
    print(str(i)+"."+str(item[0])+" "+item[2]+" kontrol ediliyor" )
    if (datetime.now()-lastCheckTime > timedelta(hours=23) or item[0]==283):
        getStoryOfAccount(item[1],item[0],item[5])
        print(str(i)+"."+str(item[0])+" "+item[2]+" kontrol edildi" )
    else:
        print(str(i)+"."+str(item[0])+" "+item[2]+ " 'in kontrolüne gerek yok" )
        
    


