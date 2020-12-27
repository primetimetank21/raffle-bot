from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
# import os
from time import sleep

def getKeys(file):
    f = open(file, "r")
    credentials = {}

    for i, line in enumerate(f.readlines()):
        if i == 0:
            credentials["user"] = line.strip()
        elif i == 1:
            credentials["pass"] = line.strip()
        # elif i == 2:
        #     credentials["email"] = line.strip()
        # elif i == 3:
        #     credentials["emailPass"] = line.strip()

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

        sleep(8)

        #go through raffles...
        #parse through raffle ids
        #store them to a file
        #if already entered, skip


        #get total raffles not currently entered in
        rafflesIn, rafflesTotal = 0,0
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")


        # stats = soup.find_all("div", {"class": "raffle-list-stat"})
        # tmp = open("./tmp.txt", "w")
        # for stat in stats:
        #     tmp.write(str(stat) + "\n")
        # tmp.close()
        # print("Stored in file...")

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
            driver.execute_script("window.scrollTo(0, 0);")
            sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            sleep(0.5)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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

        # os.remove("./tmp.txt")

        # print("Removed \"tmp.txt\"...")

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

        sleep(5)

        for id in enteredIDs:
            if id in allIDs:
                allIDs.remove(id)
            # driver.get(f"https://scrap.tf/raffles/{id}")
            # sleep(7.5)
            # print(f"Visited {id}")

        for id in allIDs:
            try:
                driver.get(f"https://scrap.tf/raffles/{id}")
                sleep(5)
                driver.execute_script("window.scrollTo(0, 0);")
                sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                sleep(2)

                action = ActionChains(driver)

                # row = driver.find_element_by_class_name("col-xs-7 enter-raffle-btns")
                row = driver.find_element_by_class_name("enter-raffle-btns")

                # width = driver.execute_script("return document.body.scrollWidth")
                # action.move_to_element_with_offset(row, int(width) * 0.65, 32).click().perform()
                action.move_to_element(row).click().perform()
                
                enterBtn = driver.find_element_by_id("raffle-enter")
                text = enterBtn.get_attribute("data-loading-text")
                count = 0
                while text != "Leaving..." and count > 4:
                    try:
                        enterBtn = driver.find_element_by_id("raffle-enter")
                        text = enterBtn.get_attribute("data-loading-text")
                        driver.execute_script("window.scrollTo(0, 0);")
                        sleep(2)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2.5);")
                        sleep(2)
                        row = driver.find_element_by_class_name("enter-raffle-btns")
                        sleep(0.5)
                        action.move_to_element(row).click().perform()

                        print(f"Clicked at {id} ({count+1})...")
                        sleep(3)
                    except Exception as e:
                        print(f"Sumn happened: {e}")
                        text = enterBtn.get_attribute("data-loading-text")
                        print(f"Failed at {id} ({count+1})...")
                        sleep(3)
                    
                    count+=1
                
                print(f"Count was {count}...")
                sleep(7.5)

            except Exception as e:
                print(f"Failed at {id}: {e}")
                continue

        driver.quit()
        print("Finished!")

    except Exception as e:
        print(e)
        driver.quit()



keys = getKeys("login.txt")
clickThrough(keys, "https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fscrap.tf%2Flogin&openid.realm=https%3A%2F%2Fscrap.tf&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select")
# getEmail(keys)
