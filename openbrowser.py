# Installation commands: pip install selenium, pip install requests

# Gives specific time interval for the code
import time
sec = 2

# Extension for selenium exception
import selenium.common.exceptions as se_exception

from selenium import webdriver
from selenium.webdriver.common.by import By

# This keeps the browser on if the code fails
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

import json

# for JSON Place Holder API
import requests

def OpenBrowser():
    driver.get('https://www.saucedemo.com')
    print("\nOpened Browser")
    time.sleep(sec)

def GetCredentials():
    l = json.load(open('login.json','r'))
    print("\nGot credentials")
    time.sleep(sec)
    return l['username'], l['password']

def login():
    _username, _password = GetCredentials()

    # Fields from the login form
    user_field = driver.find_element(by="id", value="user-name")
    pass_field = driver.find_element(by="id", value="password")
    button = driver.find_element(by="id", value="login-button")

    user_field.send_keys(_username)
    pass_field.send_keys(_password)

    button.click()

    # Check if username or password is incorrect
    try:
        error_check = driver.find_element(by=By.CLASS_NAME, value="error-button")
    except se_exception.NoSuchElementException:
        print("\nLogged in")
        time.sleep(sec)
    else:
        driver.quit()
        assert error_check, "Wrong Username or Password."

def scrapper():
    # Scrapes data and adds it to JSON

    b = driver.find_elements(by=By.CLASS_NAME, value="inventory_item")

    # Checks if any data is scraped from website
    if len(b) >= 1:
        print("\nData scraped successfully")
        time.sleep(sec)

    # Store scraped data in dictionary
    products = {}

    for i in range(len(b)):
        prod = b[i].text.splitlines()
        products[prod[0]] = {"description":prod[1], "price":prod[2]}
    
    # Dump data in json file
    json.dump(products, open('products.json','w'), indent=4)
    print("\nSuccessfully created JSON file")
    time.sleep(sec)

def manipulate(n):
    # Check if file eist and is not empty
    try:
        products = json.load(open('products.json','r'))
    except FileNotFoundError:
        print("\nNo file found.")
    except json.decoder.JSONDecodeError:
        print("\nEmpty JSON file.")
    else:
        # Changes the price in the specified element.
        # n value chooses the positin of key
        k = list(products.keys())
    
        print("\nKey according to position "+str(n)+":", k[n-1])
        print("Price:", products[k[n-1]]["price"])

        products[k[n-1]]["price"] = "$100"
        json.dump(products, open('products.json','w'), indent=4)

        print("Price after modification:", json.load(open('products.json','r'))[k[n-1]]["price"])


def call_api():
    # returns content from API to JSON
    url = 'https://jsonplaceholder.typicode.com/posts'
    print("\nCalled JSON Placeholder API")
    time.sleep(sec)
    return requests.get(url).json()

def Main():
    print("1. Website Scripting and JSON Storage\n2. JSON Manipulation\n3. JSON Placeholder API call\n4. Exit")
    while True:
        a = input("\n1/2/3/4 (exit): ")

        match a:
            case '1':
                # Checks Internet connection
                # If there, proceed with other operation
                try:
                    global driver
                    driver = webdriver.Chrome(options=chrome_options)
                    OpenBrowser()
                except se_exception.WebDriverException:
                    print("\nCheck your internet connection and try again.")
                    driver.quit()
                else:
                    login()
                    scrapper()
                    driver.quit()
            case '2':
                manipulate(3)
            case '3':
                # Checks internet connection
                # If there, get a title from JSON api and store it in new JSON file
                try:
                    extract = call_api()[0]['title']
                except requests.exceptions.ConnectionError: 
                    print("\nCheck your internet connection and try again.")
                else:
                    Dict = {"Title": extract}
                    json.dump(Dict, open('api_call.json','w'), indent=4)
                    print("\nCreated new JSON file.")
            case '4':
                break
            case default:
                print("Wrong input. Try again!")


Main()