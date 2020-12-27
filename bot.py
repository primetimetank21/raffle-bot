from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
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


def clickThrough(data, url):
    try:
        driver = webdriver.Chrome("./chromedriver")
        driver.get(url)

        username = driver.find_element_by_id("steamAccountName")
        password = driver.find_element_by_id("steamPassword")
        loginBtn = driver.find_element_by_id("imageLogin")

        username.send_keys(data["user"])
        password.send_keys(data["pass"])

        loginBtn.click()

        sleep(3)

        raffleBtn = driver.find_element_by_xpath("//*[@id=\"navbar-main\"]/ul[1]/li[2]/a")
        raffleBtn.click()

        sleep(1)

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

        #get total raffles not currently entered in
        rafflesIn, rafflesTotal = 0,0
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        stats        = soup.find("div", class_="raffle-list-stat").h1
        stats        = str(stats.text).split("/")
        rafflesIn    = int(stats[0])
        rafflesTotal = int(stats[1])
        print(f"\nTOTAL...\nEntered: {rafflesIn}\tTotal: {rafflesTotal}\n")

        entered_Num      = len(soup.find_all("panel-raffle raffle-entered"))
        totalRaffles_Num = len(soup.find_all("panel-raffle"))

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
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
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

        successes,fails = 0,0
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

                row = driver.find_element_by_class_name("enter-raffle-btns")
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
                if count <=4 :
                    successes+=1
                else:
                    fails+=1
                sleep(7.5)

            except Exception as e:
                print(f"Failed at {id}: {e}")
                fails+=1
                continue

        driver.quit()
        print("Finished!")
        print(f"Successes: {successes}\nFails: {fails}")

    except Exception as e:
        print(e)
        driver.quit()



keys = getKeys("login.txt")
clickThrough(keys, "https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fscrap.tf%2Flogin&openid.realm=https%3A%2F%2Fscrap.tf&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select")
# getEmail(keys)
