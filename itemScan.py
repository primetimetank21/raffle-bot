from selenium import webdriver
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

    f.close()

    return credentials


def search(data, creds, url):
    try:
        print("Terms searching for:")
        for term in data:
            if term != data[-1]:
                print(f"{term},", end=" ")
            else:
                print(f"{term}\n")

        try:
            driver = webdriver.Firefox()
        except:
            driver = webdriver.Chrome("./chromedriver")
        driver.get(url)

        username = driver.find_element_by_id("steamAccountName")
        password = driver.find_element_by_id("steamPassword")
        loginBtn = driver.find_element_by_id("imageLogin")

        username.send_keys(creds["user"])
        password.send_keys(creds["pass"])

        loginBtn.click()

        sleep(3)

        codeBox    = driver.find_element_by_id("authcode")
        submitBtn  = driver.find_element_by_xpath("//*[@id=\"auth_buttonset_entercode\"]/div[1]/div[1]")
        secretCode = str(input("Enter Code:    ")) #getEmail(data))

        codeBox.send_keys(secretCode.upper())

        sleep(3)

        submitBtn.click()
        print("Logged in...")

        sleep(5)

        #go to main page
        print("Navigating to raffle page...")
        proceedBox = driver.find_element_by_xpath("//*[@id=\"success_continue_btn\"]/div[1]")
        proceedBox.click()

        sleep(15)

        raffleBtn = driver.find_element_by_xpath("//*[@id=\"navbar-main\"]/ul[1]/li[2]/a")
        raffleBtn.click()

        sleep(1)

        pubRaffle = driver.find_element_by_xpath("//*[@id=\"navbar-main\"]/ul[1]/li[2]/ul/li[3]/a")
        pubRaffle.click()

        print("Getting raffle info...")
        sleep(5)

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

        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")

        allIDs = []
        for raf in soup.find_all("div", {"class": "raffle-name"}):
            link = raf.a["href"]
            link = link.split("/")
            allIDs.append(link[-1])

        enteredIDs = []
        for raf in soup.find_all("div", {"class": "raffle-entered"}):
            link = raf.a["href"]
            link = link.split("/")
            enteredIDs.append(link[-1])

        for id in enteredIDs:
            if id in allIDs:
                allIDs.remove(id)

        interestingRaffles = {}
        for searchTerm in data:
            interestingRaffles[searchTerm] = []

        #if the raffle has at least one of the terms searching for, add it to list of urls we want to enter
        print("Searching for interesting raffles...")
        matches = 0
        for id in allIDs:
            try:
                cur     = soup.find("div", {"onclick": f"ScrapTF.Raffles.RedirectToRaffle('{id}')"})
                items   = cur.find("div", {"class": "items-container"})
                itemStr = str(items)

                for searchTerm in data:
                    if searchTerm in itemStr:
                        # print(f"{searchTerm} found!")
                        interestingRaffles[searchTerm].append(f"https://scrap.tf/raffles/{id}")
                        matches += 1
                        break
                # print(f"Success @ {id}")
                # print(str(items))
                # print()

            except:
                print(f"Failed @ {id}...")

        driver.quit()
        print(f"Completed search with {matches} matches...\n")

        print("Raffles to join:")
        f = open("./raffles_to_join.txt", "w")
        f.write("Raffles:\n")
        for key in interestingRaffles.keys():
            print(f"\t{key}")
            f.write(f"\t{key}\n")
            for raffle in interestingRaffles[key]:
                print(f"\t    {raffle}")
                f.write(f"\t    {raffle}\n")
            print()
            f.write("\n")
        f.close()
    except Exception as e:
        print(e)
        driver.quit()


def main():
    credentials = getKeys("./login.txt")
    terms = ["Unusual", "Mann Co. Supply Crate Key", "Strange", "Refined Metal"]

    # #if want to enter additional terms manually to search for
    # term = ""
    # while term != "done":
    #     term = str(input("Enter term to search:\t"))
    #     term = term.strip()
    #     if term != "done" and term != "":
    #         terms.append(term)
    search(terms, credentials, "https://steamcommunity.com/openid/login?openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.mode=checkid_setup&openid.return_to=https%3A%2F%2Fscrap.tf%2Flogin&openid.realm=https%3A%2F%2Fscrap.tf&openid.ns.sreg=http%3A%2F%2Fopenid.net%2Fextensions%2Fsreg%2F1.1&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select")


if __name__ == "__main__":
    main()
