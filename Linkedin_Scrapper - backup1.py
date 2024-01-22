# Import necessary packages for web scraping and logging
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
import random
import time

# Configure logging settings
logging.basicConfig(filename="scraping.log", level=logging.INFO)


def scrape_linkedin_jobs(job_title: str, location: str, pages: int = None) -> list:
    """
    Scrape job listings from LinkedIn based on job title and location.

    Parameters
    ----------
    job_title : str
        The job title to search for on LinkedIn.
    location : str
        The location to search for jobs in on LinkedIn.
    pages : int, optional
        The number of pages of job listings to scrape. If None, all available pages will be scraped.

    Returns
    -------
    list of dict
        A list of dictionaries, where each dictionary represents a job listing
        with the following keys: 'job_title', 'company_name', 'location', 'posted_date',
        and 'job_description'.
    """

    # Log a message indicating that we're starting a LinkedIn job search
    logging.info(f'Starting LinkedIn job scrape for "{job_title}" in "{location}"...')

    ProgLanguage = ("Python", "Java", "C++", "Scala", "R", "Julia", "Go", "Kotlin", "Bash")
    DataBase = ("SQL", "NoSQL"," MongoDB", "Cassandra", "Neo4j", "HBase", "Elasticsearch")
    DataAnalytics = ("Pandas", "NumPy", "R", "MATLAB")
    BigData = ("Hadoop", "Spark", "Databricks", "Flink", "Apache Airflow")
    MachingLearning = ("Scikit-Learn", "TensorFlow", "Keras", "PyTorch", "XGBoost", "LightGBM", "CatBoost", "Orange")
    DataView = ("Tableau", "Power BI", "PowerBI", "Matplotlib", "Seaborn", "Plotly")
    Statistics = ("Statistiques Descriptives", "Inférentielles", "Bayesian Statistics", "Statistiques Bayésiennes")
    CloudComputing = ("AWS", "Azure", "Google Cloud Platform", "IBM Cloud", "Alibaba Cloud")
    DevTools = ("Git", "Docker", "Jenkins", "Travis CI")
    Os = ("Linux", "Windows", "MacOS")
    SoftDB = ("MySQL", "PostgreSQL", "Oracle", "Microsoft SQL Server", "Snowflake")
    SoftBigDataProcessing = ("Apache Kafka", "Apache Flink", "HBase", "Apache Cassandra")
    Automation = ("Ansible", "Kubernetes", "Puppet", "Chef", "Airflow")
    InfrastructureAsCode = ("Terraform", "CloudFormation")
    NetworkSecurty = ("VPN", "Firewall", "SSL/TLS", "Wireshark")
    Virtualisation = ("VMware", "VirtualBox", "Hyper-V")
    Containers = ("Docker", "Kubernetes", "OpenShift")
    Collaboration = ("JIRA", "Confluence", "Slack", "Microsoft Teams", "Discord")


    
    # Sets the pages to scrape if not provided
    pages = pages or 1

    # Set up ChromeOptions
    options = Options()
    options.add_argument("--start-maximized")

    # Specify the path to your chromedriver executable
    chrome_driver_path = r'C:\\Users\\Default\\Desktop\\chromedriver-win64\\chromedriver.exe'
    service = ChromeService(chrome_driver_path)
    # Set up the Chrome WebDriver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the LinkedIn job search page with the given job title and location
    driver.get(
        f"https://www.linkedin.com/jobs/search/?keywords={job_title}&location={location}"
    )

    # Scroll through the first 50 pages of search results on LinkedIn
    for i in range(pages):

        # Log the current page number
        logging.info(f"Scrolling to bottom of page {i+1}...")

        # Scroll to the bottom of the page using JavaScript
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        try:
            # Wait for the "Show more" button to be present on the page
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/main/section[2]/button")
                )
            )
            # Click on the "Show more" button
            element.click()

        # Handle any exception that may occur when locating or clicking on the button
        except Exception:
            # Log a message indicating that the button was not found and we're retrying
            logging.info("Show more button not found, retrying...")

        # Wait for a random amount of time before scrolling to the next page
        time.sleep(random.choice(list(range(3, 7))))

    # Scrape the job postings
    jobs = []
    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_listings = soup.find_all(
        "div",
        class_="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
    )

    try:
        for job in job_listings:
            # Extract job details

            # job title
            job_title = job.find("h3", class_="base-search-card__title").text.strip()
            # job company
            job_company = job.find(
                "h4", class_="base-search-card__subtitle"
            ).text.strip()
            # job location
            job_location = job.find(
                "span", class_="job-search-card__location"
            ).text.strip()
            # job link
            apply_link = job.find("a", class_="base-card__full-link")["href"]

            # Navigate to the job posting page and scrape the description
            driver.get(apply_link)

            # Sleeping randomly
            time.sleep(random.choice(list(range(5, 11))))

            # Use try-except block to handle exceptions when retrieving job description
            try:
                # Create a BeautifulSoup object from the webpage source
                description_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Find the job description element and extract its text
                job_description = description_soup.find(
                    "div", class_="description__text description__text--rich"
                ).text.strip()

            # Handle the AttributeError exception that may occur if the element is not found
            except AttributeError:
                # Assign None to the job_description variable to indicate that no description was found
                job_description = None

                # Write a warning message to the log file
                logging.warning(
                    "AttributeError occurred while retrieving job description."
                )

            # Add job details to the jobs list
            jobs.append(
                {
                    "title": job_title,
                    "company": job_company,
                    "location": job_location,
                    "link": apply_link,
                    "description": job_description,
                }
            )
            # Logging scrapped job with company and location information
            logging.info(f'Scraped "{job_title}" at {job_company} in {job_location}...')

    # Catching any exception that occurs in the scrapping process
    except Exception as e:
        # Log an error message with the exception details
        logging.error(f"An error occurred while scraping jobs: {str(e)}")

        # Return the jobs list that has been collected so far
        # This ensures that even if the scraping process is interrupted due to an error, we still have some data
        return jobs

    # Close the Selenium web driver
    driver.quit()

    # Return the jobs list
    return jobs


def save_job_data(data: dict) -> None:
    """
    Save job data to a CSV file.

    Args:
        data: A dictionary containing job data.

    Returns:
        None
    """

    # Create a pandas DataFrame from the job data dictionary
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file without including the index column
    df.to_csv("jobs.csv", index=False)

    # Log a message indicating how many jobs were successfully scraped and saved to the CSV file
    logging.info(f"Successfully scraped {len(data)} jobs and saved to jobs.csv")


data = scrape_linkedin_jobs("Data Engineer", "France")
save_job_data(data)
