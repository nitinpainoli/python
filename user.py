from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


import sys, time

def vpnSeleniumWorkflow(VPN_URL, VPN_ADMIN_USERNAME, VPN_ADMIN_PASSWORD, VPN_NEW_USER):
    try:
        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument('--start-maximised')
        options.add_argument('--disable-gpu')
        options.add_argument('ignore-certificate-errors')
        driver = webdriver.Chrome(options=options)

        # options = webdriver.FirefoxOptions()
        # driver = webdriver.Firefox(options=options)

        print('Logging in...')
        driver.get(f"{VPN_URL}/login")

        username = driver.find_element(By.ID, "username")
        username.send_keys(VPN_ADMIN_USERNAME)
        password = driver.find_element(By.ID, "password")
        password.send_keys(VPN_ADMIN_PASSWORD)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pritunl")))
        signin_button = driver.find_element(By.ID, "submit")
        signin_button.click()
        setup_later_button = driver.find_element(By.CLASS_NAME, "header-button.orgs-add-user.btn.btn-primary")
        setup_later_button.click()

        print('Creating user...')
        time.sleep(5)
        driver.get(f"{VPN_URL}/#/users")
        time.sleep(5)
        add_user_button = driver.find_element(By.CLASS_NAME, "header-button.orgs-add-user.btn.btn-primary")
        add_user_button.click()
        time.sleep(2)
        org_count = len(driver.find_elements(By.CLASS_NAME, "org-title.no-select"))
        text_box = driver.find_elements(By.CLASS_NAME, "form-control")
        text_box[org_count].send_keys(VPN_NEW_USER)
        add_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary.ok")
        add_button.click()
        print('Getting link...')
        time.sleep(2)
        text_box[0].send_keys(VPN_NEW_USER)
        time.sleep(2)
        get_link_button = driver.find_elements(By.CLASS_NAME, "get-key-link.glyphicon.glyphicon-link.no-select")
        get_link_button[0].click()
        text_box_div = driver.find_element(By.CLASS_NAME, "otp-link.form-group")
        text_box = text_box_div.find_element(By.CLASS_NAME, 'form-control')
        time.sleep(2)
        return text_box.get_property('value')
    except Exception as e:
        driver.save_screenshot("debug.png")
        print(e)
        sys.exit(1)
    finally:
        driver.close()



vpnSeleniumWorkflow("https://3.227.230.19", "pritunl", "l41Oezpgctdq", "testiinn")