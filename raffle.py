from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os
from time import sleep

def getKeys(file):
    f = open(file, "r")
    credentials = {}

    for i, line in enumerate(f.readlines()):
        if i == 0:
            credentials["user"] = line.strip()
        elif i == 1:
            credentials["pass"] = line.strip()
        elif i == 2:
            credentials["email"] = line.strip()
        elif i == 3:
            credentials["emailPass"] = line.strip()

    f.close()

    return credentials


def getEmail(data): #might not be possible
    try:
        driver = webdriver.Chrome("./chromedriver")
        driver.get("https://www.google.com/gmail")

        sleep(3)

        emailElement = driver.find_element_by_id("identifierId")
        nextBtn      = driver.find_element_by_xpath("//*[@id=\"identifierNext\"]/div/button/div[2]")

        sleep(2)

        emailElement.send_keys(data["email"])

        sleep(2)

        nextBtn.click()

        sleep(10)

        driver.quit()

    except:
        print("Failed")
        driver.quit()



def clickThrough(data, url):
    try:
        driver = webdriver.Chrome("./chromedriver")
        driver.get(url)

        # sleep(3)

        username = driver.find_element_by_id("steamAccountName")
        password = driver.find_element_by_id("steamPassword")
        loginBtn = driver.find_element_by_id("imageLogin")

        # sleep(2)

        username.send_keys(data["user"])
        password.send_keys(data["pass"])

        sleep(2)

        loginBtn.click()

        # sleep(3)

        #login to email and get code (NOT POSSIBLE)

        #put code into field
        codeBox    = driver.find_element_by_id("authcode")
        submitBtn  = driver.find_element_by_xpath("//*[@id=\"auth_buttonset_entercode\"]/div[1]/div[1]")
        secretCode = str(input("Enter Code:    ")) #getEmail(data))

        codeBox.send_keys(secretCode.upper())

        sleep(3)

        submitBtn.click()

        sleep(5)

        #go to main page
        proceedBox = driver.find_element_by_xpath("//*[@id=\"success_continue_btn\"]/div[1]")
        proceedBox.click()

        sleep(5)

        raffleBtn = driver.find_element_by_xpath("//*[@id=\"navbar-main\"]/ul[1]/li[2]/a")
        raffleBtn.click()

        sleep(3)

        pubRaffle = driver.find_element_by_xpath("//*[@id=\"navbar-main\"]/ul[1]/li[2]/ul/li[3]/a")
        pubRaffle.click()

        #go to older raffles (soon to end)
        sleep(3)

        soonEndTab = driver.find_element_by_xpath("//*[@id=\"pid-raffles\"]/div[4]/div[3]/nav/ul[2]/li/a")
        soonEndTab.click()

        sleep(1)

        timeLeftBtn = driver.find_element_by_xpath("//*[@id=\"pid-raffles\"]/div[4]/div[3]/nav/ul[2]/li/ul/li[2]/a")
        timeLeftBtn.click()

        sleep(5)

        #go through raffles...
        #parse through raffle ids
        #store them to a file
        #if already entered, skip


        #get total raffles not currently entered in
        rafflesIn, rafflesTotal = 0,0
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")


        stats = soup.find_all("div", {"class": "raffle-list-stat"})
        tmp = open("./tmp.txt", "w")
        for stat in stats:
            tmp.write(str(stat) + "\n")
        tmp.close()
        print("Stored in file...")

        stats        = soup.find("div", class_="raffle-list-stat").h1
        stats        = str(stats.text).split("/")
        rafflesIn    = int(stats[0])
        rafflesTotal = int(stats[1])
        print(f"\nTOTAL...\nEntered: {rafflesIn}\tTotal: {rafflesTotal}\n")


        raffleIDs_In    = []
        raffleIDs_notIn = []

        entered_Num      = len(soup.find_all("panel-raffle raffle-entered"))
        totalRaffles_Num = len(soup.find_all("panel-raffle"))

        # webpage = driver.find_element_by_tag_name("html")
        # webpage.send_keys(Keys.END)

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(0.5)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        sleep(10)

        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        entered          = soup.find_all("div", {"class": "panel-raffle raffle-entered"})
        totalRaffles     = soup.find_all("div", {"class": "panel-raffle"})
        entered_Num      = len(entered)
        totalRaffles_Num = len(totalRaffles)

        print(f"\nFINAL...\nEntered: {entered_Num}\tTotal: {totalRaffles_Num}")

        os.remove("./tmp.txt")

        print("Removed \"tmp.txt\"...")

        allIDs = []
        for raf in soup.find_all("div", {"class": "raffle-name"}):
            link = raf.a["href"]
            link = link.split("/")
            allIDs.append(link[-1])
        print(f"{len(allIDs)}, {allIDs}")

        enteredIDs = []
        for raf in soup.find_all("div", {"class": "raffle-entered"}):
            link = raf.a["href"]
            link = link.split("/")
            enteredIDs.append(link[-1])
        print(f"\n{len(enteredIDs)}, {enteredIDs}")

        #important classes:
        #    panel-raffle raffle-entered
        #    panel-raffle
        #the difference b/w these two will give us which ones we need to enter
        #store both in arrays (by raffle ID) and remove the ones found in both
        #useful for parsing with beautiful soup: https://stackoverflow.com/questions/13960326/how-can-i-parse-a-website-using-selenium-and-beautifulsoup-in-python


        sleep(20)



        # seen = {}

        #click through every raffle

        # btn = "//*[@id=\"pid-viewraffle\"]/div[4]/div/div[3]/div[5]/div[2]/button[2]"
        # btn = "//*[@id=\"pid-viewraffle\"]/div[4]/div/div[3]/div[7]/div[2]/button[2]"
        # btn = "//*[@id=\"pid-viewraffle\"]/div[4]/div/div[3]/div[5]/div[2]/button[2]"


        driver.quit()

    except Exception as e:
        print(e)
        driver.quit()



keys = getKeys("login.txt")
clickThrough(keys, "https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fscrap.tf%2Flogin&openid.realm=https%3A%2F%2Fscrap.tf&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select")
# getEmail(keys)
