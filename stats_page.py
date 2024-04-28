from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from css_selectors import * #has all css selectors for web scraping
from selenium.webdriver.support.wait import WebDriverWait
import asyncio 

options = webdriver.FirefoxOptions()
options.add_argument("--no-sandbox")
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.binary_location = "/snap/bin/geckodriver"

driver = webdriver.Firefox(options)


async def deposit_check(util):
    if util > 65 and util < 70 :
        return "Open"
    else: 
        return "Closed"
            

async def explorer_guru():
    driver.get("https://nolus.explorers.guru/")
    try: 
        element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, inflation_guru))
        )
        await asyncio.sleep(3)
        data = element.text
        if data == "0%": 
            data = "Error"
    except Exception as e: 
        print ("Error with Explorer.guru: ",e)
        data = "Error"
    return data 


async def ping_pub():
    driver.get("https://ping.pub/nolus/")
    try: 
        element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, inflation_ping))
        )
        await asyncio.sleep(3)
        data = element.text
    except Exception as e: 
        print ("Error with Ping.pub: ",e)
        data = "Error"
    return data

async def get_inflation(): 
    try: 
        result = await ping_pub()
    except: 
        result = await explorer_guru()
    return result


async def osmosis(): 
    try:
        data1 = driver.find_element(By.CSS_SELECTOR, osmosis1_).text
        data2 = driver.find_element(By.CSS_SELECTOR, osmosis2_).text
        util = float(driver.find_element(By.CSS_SELECTOR, osmosis_util).text)
        deposit_result = await deposit_check(util)
        apr = data1 + data2 
    except Exception as e: 
        print (e)
        apr = "Error"
        deposit_result = "Error"
    return apr, deposit_result


async def neutron(): 
    try:
        data1 = driver.find_element(By.CSS_SELECTOR, neutron1_).text
        data2 = driver.find_element(By.CSS_SELECTOR, neutron2_).text
        util = float(driver.find_element(By.CSS_SELECTOR, neutron_util).text)
        deposit_result = await deposit_check(util)
        apr = data1 + data2 
    except Exception as e:
        print (e)
        apr = "Error"
        deposit_result = "Error"
    return apr, deposit_result


async def osmo_neutron(): 
    efforts_to_load = 1
    while True:
        driver.get("https://app.nolus.io/stats")
        try:
            WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, osmosis1_))
            )
            break
        except Exception as e: 
            print ("Problem with app.nolus.io ",e)
            efforts_to_load+=1
            if efforts_to_load == 3: 
                return "Error", "Error", "Error", "Error"

    apr_osmo, deposit_check_osmo = await osmosis()
    apr_ntrn, deposit_check_ntrn = await neutron()
    return apr_osmo, deposit_check_osmo, apr_ntrn, deposit_check_ntrn
