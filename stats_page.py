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

driver_guru = webdriver.Firefox(options)
driver_guru.get("https://nolus.explorers.guru/")

driver_ping = webdriver.Firefox(options)
driver_ping.get("https://ping.pub/nolus/")

driver_osmo = webdriver.Firefox(options)
driver_osmo.get("https://app.nolus.io/stats")

driver_neutron = webdriver.Firefox(options)
driver_neutron.get("https://app.nolus.io/stats")

async def deposit_check(util):
    if util > 65 and util < 70 :
        return "Open"
    else: 
        return "Closed"
            

async def explorer_guru():
    driver_guru.refresh()

    try: 
        element = WebDriverWait(driver_guru, 20).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, inflation_guru))
        )
        await asyncio.sleep(3)
        data = element.text
    except Exception as e: 
        print ("Error with Explorer.guru: ",e)
        data = "Error"
    return data 


async def ping_pub():
    driver_ping.refresh()
    try: 
        element = WebDriverWait(driver_ping, 20).until(
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
        result = await explorer_guru()
        if result == "0%" or result == "Error":
            raise Exception
    except: 
        result = await ping_pub()
    return result


async def osmosis(): 
    driver_osmo.refresh()

    WebDriverWait(driver_osmo, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, osmosis1_))
    )
    try:
        data1 = driver_osmo.find_element(By.CSS_SELECTOR, osmosis1_).text
        data2 = driver_osmo.find_element(By.CSS_SELECTOR, osmosis2_).text
        util = float(driver_osmo.find_element(By.CSS_SELECTOR, osmosis_util).text)
        deposit_result = await deposit_check(util)
        apr = data1 + data2 
    except Exception as e: 
        print (e)
        apr = "Error"
        deposit_result = "Error"
    return apr, deposit_result


async def neutron(): 
    driver_neutron.refresh()
    WebDriverWait(driver_neutron, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, osmosis1_))
    )
    try:
        data1 = driver_neutron.find_element(By.CSS_SELECTOR, neutron1_).text
        data2 = driver_neutron.find_element(By.CSS_SELECTOR, neutron2_).text
        util = float(driver_neutron.find_element(By.CSS_SELECTOR, neutron_util).text)
        deposit_result = await deposit_check(util)
        apr = data1 + data2 
    except Exception as e:
        print (e)
        apr = "Error"
        deposit_result = "Error"
    return apr, deposit_result


async def osmo_neutron(): 
    apr_osmo, deposit_check_osmo = await osmosis()
    apr_ntrn, deposit_check_ntrn = await neutron()
    return apr_osmo, deposit_check_osmo, apr_ntrn, deposit_check_ntrn

