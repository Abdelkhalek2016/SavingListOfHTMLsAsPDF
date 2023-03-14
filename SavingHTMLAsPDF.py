from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import io
from time import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os

with open("links.txt", "r",encoding="utf-8") as f:
    # read the links from the text file
    links = f.readlines()

# set up the chrome options to run in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# create a new Chrome web driver instance
driver = webdriver.Chrome(options=chrome_options)


with open("SavedLinks.txt", "a+",encoding="utf-8") as f:
    counter=1
        # navigate to the webpage you want to screenshot
    for link in links:
        try:
            driver.get(link.strip())

            # wait for the cookies message to be visible and click the "Accept" button
            if counter==1:
                try:
                    cookies_accept_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div[2]/ul/li/a"))
                    )
                    cookies_accept_button.click()
                    
                except:
                    print("Cookies message not found or could not be dismissed.")

            # get the full height of the page
            scroll_height = driver.execute_script("return document.body.scrollHeight")

            # set the window size to the full height of the page
            driver.set_window_size(1920, scroll_height)

            # take a screenshot of the entire page
            screenshot = driver.find_element("tag name","body").screenshot_as_png

            # convert the screenshot to an RGB image
            image = Image.open(io.BytesIO(screenshot)).convert("RGB")

            # save the image as a PDF file
            timesavingfile=round(time())
            filename=link.split("=")[1].split("&")[0] +"_"+str(timesavingfile) +".pdf"
            image.save("SavedHTML\\"+filename, "PDF", resolution=100.0)
            print(link.strip() + "\t" + filename)
            f.write(link.strip() + "\t" + filename + "\n")
            print(f"html number {counter} Saved")
            f.flush()
            counter+=1
        except Exception as e:
            print("Type of exception is ",type(e))
            print(e)
            print(f"this html number {counter} not saved correctly")
            counter+=1
            continue
# close the web driver instance
driver.quit()
