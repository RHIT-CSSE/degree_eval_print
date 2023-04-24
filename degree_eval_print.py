from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import json
import os
import getpass
import base64

FILE_ROOT = os.path.expanduser("~/Downloads")
print("\n\n Degree Evaluation Downloading launched....\n\n")
print("By default, the files will be downloaded into {}".format(FILE_ROOT))
chrome_options = webdriver.ChromeOptions()
# settings = {
#     "recentDestinations": [{
#         "id": "Save as PDF",
#         "origin": "local",
#         "account": "",
#     }],
#     "selectedDestinationId": "Save as PDF",
#     "version": 2,
# }

# prefs = {"printing.print_preview_sticky_settings.appState": json.dumps(settings),
#          "profile.default_content_settings.popups": 0,
#          "download.prompt_for_download": False,
#          "download.directory_upgrade": True,
#          "safebrowsing.enabled": True}


# pass Option to driver
chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--headless')

print("\n\n Starting Chrome now....\n\n")
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# navigate to the borrower website
driver.get("https://bannerweb.rose-hulman.edu/login")

# find and fill in the login form
username_input = driver.find_element("name", "usernameUserInput")
password_input = driver.find_element("name", "password")
print("Type your login credentials below.....")
username = input("Username: ")
username_input.send_keys(username)
password = getpass.getpass()
password_input.send_keys(password)

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

print("Waiting for login.....")
index = 0
while True:
    try:
        wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Faculty & Advisor"))).click()
    except TimeoutException:
        print("Login failed!!!\nCannot find Faculty & Advisor link.")
        break

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Advisor Menu"))).click()

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "ID Selection"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[Value='Submit']"))).click()
    lastname_input = driver.find_element("name", "last_name")
    lastname_input.send_keys("%")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[Value='Submit']"))).click()

    select = Select(driver.find_element("name", 'xyz'))
    if index == len(select.options):
        break

    select.select_by_index(index)
    student_name = select.first_selected_option.text
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[Value='Submit']"))).click()

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Degree Evaluation"))).click()

    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Generate New Evaluation"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[Value='Generate Request']"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[Value='Submit']"))).click()

    # save to PDF

    # driver.execute_script("document.title = \'{}.pdf\'".format(student_name))
    # driver.execute_script("window.print();")

    pdf_data = driver.execute_cdp_cmd(
        "Page.printToPDF", {"path": 'html-page.pdf', "format": 'A4'})
    path = os.path.join(FILE_ROOT, '{}.pdf'.format(student_name))
    with open(path, "wb+") as file:
        file.write(base64.b64decode(pdf_data['data']))

    print("Saving PDF for {}".format(student_name))

    index += 1

driver.quit()
