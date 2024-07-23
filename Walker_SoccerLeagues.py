import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

'''
Bugs: Doesn't Export to Excel
      Opta alters data every once in a while. Excel "Country_Codes" Sheet needs to be manually updated to reflect changes if code is to work
'''

def main():

    biglist = league_info()

    create_lists(biglist)

def get_league(rando_string):
        league = ""
        a = 0
        i=""
        for i in rando_string.lstrip("<"):
            if i == ">":
                a = 1
            if a == 1:
                league = league + i
            if i == "<":
                break
        league = league.strip('<').strip('>')
        return(league)

def get_team(rando_string):
    league = ""
    a = 0
    i=''
    b=0
    for i in rando_string:
        if i == ">":
            a += 1
        if a == 6:
            league = league + i
        if i == "<":
            b+=1
        if b == 7:
            break
        #print(i)
    league = league.strip('<').strip('>')
    return(league)

def league_info():
    
    data = pd.read_excel(r"C:\Users\wlaitala25\Documents\GitHub\Cesena\Football_Team_Database.xlsx", sheet_name="Country_Codes")

    biglist = []
    for n in range(76):
        smalllist = []
        
        if data.loc[n,'Special Order:'] == "nah":
            smalllist.append(data.loc[n,'Country:'])
            smalllist.append(data.loc[n,'Flights:'])
        else:
            smalllist.append(data.loc[n,'Country:'])
            smalllist.append(data.loc[n,'Flights:'])
            smalllist.append(data.loc[n,'Special Order:'])

        biglist.append(smalllist)

    return(biglist)

def create_lists(biglist):

    chrome_service = Service(executable_path=r'C:\Users\wlaitala25\Documents\GitHub\Cesena\chromedriver-win64\chromedriver.exe')
    driver = webdriver.Chrome(service=chrome_service)
    driver.get('https://dataviz.theanalyst.com/opta-power-rankings/')

    #wprint(biglist)
    masterlist = []
    data = pd.read_excel(r"C:\Users\wlaitala25\Documents\GitHub\Cesena\Football_Team_Database.xlsx", sheet_name="Country_Codes")
    for n in range(len(biglist)):   #correctly goes to 75
        if len(biglist[n]) == 2:
            for flight in range(data.loc[n,"Flights:"]):
                country = biglist[n][0]
                flight = flight + 1
                driver.find_element(By.CLASS_NAME, "dropdown-tools").click()
                #Click Dropdown
                driver.find_element(By.XPATH, "//input[@placeholder='start typing to see suggestions']").send_keys(data.loc[n,"Country:"])
                #Type Country in
                raw_league_text = driver.find_element(By.XPATH, f"//body/div[@id='root']/div[@class='App']/div/div[@class='hXafwz_cbVF7HDOcyAH_']/div[@class='dropdown-container']/div[@class='dropdown-menu-container']/div[@class='dropdown-menu']/div[@class='dropdown-items-list']/div[{flight+2}]/div[1]").get_attribute("innerHTML")
                league = get_league(raw_league_text)
                #Extract League Name
                driver.find_element(By.XPATH, f"//body/div[@id='root']/div[@class='App']/div/div[@class='hXafwz_cbVF7HDOcyAH_']/div[@class='dropdown-container']/div[@class='dropdown-menu-container']/div[@class='dropdown-menu']/div[@class='dropdown-items-list']/div[{flight+2}]/div[1]").click()
                #Click League
                
                try:
                    for i in range(30):
                        team_name = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(2)").get_attribute("innerHTML")
                        score = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(3)").get_attribute("innerHTML")
                        rank = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(4)").get_attribute("innerHTML")
                        #masterlist.append([get_team(team_name), score, league, flight, rank, country])
                        
                        #if flight == :
                            #print(country)
                        print(get_team(team_name) + ", " + score + ", " + str(league) + ", " + str(flight) + ", " + rank + ", " + country)
                        #print(masterlist)
                except:
                    pass
                
                driver.find_element(By.XPATH, "//button[normalize-space()='Clear All']").click()
                #Clear Search
                
        elif len(biglist[n]) == 3:
            a = 0
            
            try:
                placeholder = data.loc[n,"Special Order:"].split(" ")
            except:
                placeholder = [data.loc[n,"Special Order:"]]
            
            for flight in placeholder:
                a += 1
                country = biglist[n][0]
                flight = int(flight)
                driver.find_element(By.CLASS_NAME, "dropdown-tools").click()
                #Click Dropdown
                driver.find_element(By.XPATH, "//input[@placeholder='start typing to see suggestions']").send_keys(data.loc[n,"Country:"])
                #Type Country in
                raw_league_text = driver.find_element(By.XPATH, f"//body/div[@id='root']/div[@class='App']/div/div[@class='hXafwz_cbVF7HDOcyAH_']/div[@class='dropdown-container']/div[@class='dropdown-menu-container']/div[@class='dropdown-menu']/div[@class='dropdown-items-list']/div[{flight}]/div[1]").get_attribute("innerHTML")
                league = get_league(raw_league_text)
                #Extract League Name
                driver.find_element(By.XPATH, f"//body/div[@id='root']/div[@class='App']/div/div[@class='hXafwz_cbVF7HDOcyAH_']/div[@class='dropdown-container']/div[@class='dropdown-menu-container']/div[@class='dropdown-menu']/div[@class='dropdown-items-list']/div[{flight}]/div[1]").click()
                #Click League
                
                try:
                    for i in range(100):
                    #i=1
                        team_name = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(2)").get_attribute("innerHTML")
                        score = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(3)").get_attribute("innerHTML")
                        rank = driver.find_element(By.CSS_SELECTOR, f"tbody tr:nth-child({i+1}) td:nth-child(4)").get_attribute("innerHTML")
                        #masterlist.append([get_team(team_name), score, league, a, rank, country])  #a == flight
                        #if a == 3:
                            #print(country)
                        print(get_team(team_name) + ", " + score + ", " + str(league) + ", " + str(a) + ", " + rank + ", " + country)
                        #print(masterlist)
                except:
                    pass
                
                driver.find_element(By.XPATH, "//button[normalize-space()='Clear All']").click()
                #Clear Search

    #print(masterlist)

main()