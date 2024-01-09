# Import Packages
from selenium import webdriver
import time
import pandas as pd
import os

# Import additional packages
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Specify the path to the chromedriver executable
chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'

# Create a Chrome Service instance
chrome_service = Service(chrome_driver_path)

# Create a Chrome WebDriver instance using the service
driver = webdriver.Chrome(service=chrome_service)

# Rest of your code
driver.implicitly_wait(10)
url1 = 'https://www.linkedin.com/jobs/search/?currentJobId=3776009950&geoId=105015875&keywords=data%20engineer&location=France&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
driver.get(url1)

# Find number of job listings using a more generic approach
job_count_element = driver.find_element(By.CLASS_NAME, 'results-context-header__job-count')
y = job_count_element.text if job_count_element else 'Not Found'

print(type(y))

# Try to convert to numeric, and handle errors
try:
    n = pd.to_numeric(y, errors='coerce')
    print(n)
except ValueError:
    print("Unable to convert to numeric.")