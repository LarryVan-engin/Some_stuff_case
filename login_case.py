import paramiko
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC

#Skip bypass web
def open_url(url):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximize")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url) 
    return driver

def click_login(driver, xpath, timeout=10):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()
        print(f"Click button: {xpath}")
    except Exception as e:
        print(f"Cannot find click button: {xpath}")

def auto_fill(driver, xpath, text, timeout=10):
    try:
        field = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        field.clear()
        field.send_keys(text)
        print(f"Auto fill username")

    except Exception as e:
        print("Cannot fill username/password!")

#Import JSON file
#file_path = 'D:\VSCode\login_session.json'
def load_json(file_path):
    with open(file_path, "r", encoding= "utf-8") as file:
        return json.load(file)

#Main
url = "https://lms.hcmut.edu.vn/login/index.php"
driver = open_url(url)

data = load_json("login_session.json")
data_key = "test"

username = data[data_key]["username"]
password = data[data_key]["password"]

# using Xpath sequentially
click_login(driver, '/html/body/div[2]/div[4]/div/div/section/div/div/div/div/div[3]/a')
auto_fill(driver, '/html/body/div/div/div[2]/div[1]/form/div[1]/input', username)
auto_fill(driver, '/html/body/div/div/div[2]/div[1]/form/div[2]/input', password)
click_login(driver, '/html/body/div/div/div[2]/div[1]/form/div[4]/input[4]')

time.sleep(3)

#Wait until user press Enter
try:
    while True:
        user_input = input("Press Enter to close your browser...")
        if user_input== "":
            break
        time.sleep(0.1)
finally:
    driver.quit()
