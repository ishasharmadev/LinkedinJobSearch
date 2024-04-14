# IMPORT LIBRARIES START ----------------------------------------------------------------------------------------------

import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd

# IMPORT LIBRARIES END ----------------------------------------------------------------------------------------------



# LAUNCH CHROME & VISIT LINKEDIN ------------------------------------------------------------------------------------

# Path for the chrome driver
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")
driver.maximize_window()
time.sleep(2)

# LAUNCH CHROME & VISIT LINKEDIN ENDS ------------------------------------------------------------------------------------



# LOG INTO YOUR ACCOUNT --------------------------------------------------------------------------------------------------

# Login Credentials
# Again use find_element_by_xpath to find email and password
# Reading txt file where we have our user credentials
with open('C:/Users/Isha/Documents/Important Documents/user_credentials.txt', 'r',encoding="utf-8") as file:
    user_credentials = file.readlines()
    user_credentials = [line.rstrip() for line in user_credentials]
username = user_credentials[0]
password = user_credentials[1]

print(username + " "+ password)

try : 
    # Find the element by XPath using By.XPATH
    username_element = driver.find_element(By.XPATH, '//input[@id="username"]')
    password_element = driver.find_element(By.XPATH, '//input[@id="password"]')

    # Perform actions on the element (e.g., input text)
    username_element.send_keys(username)
    password_element.send_keys(password)

except Exception as e : 
    print(e)

time.sleep(1)

# Wait for the login button to be clickable (using WebDriverWait)
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
)

# Click the button
button.click()
driver.implicitly_wait(30)

# LOG INTO YOUR ACCOUNT ENDS ------------------------------------------------------------------------------------------------


# VISIT HOME  & JOB PAGE ------------------------------------------------------------------------------------------------

# Entered home page now 
# Go to jobs button and search results accordingly
# Access to the Jobs button and click it
# Wait for the Jobs icon to be clickable using WebDriverWait
jobs_icon = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'global-nav__primary-link--active'))
)
scroll_script = "window.scrollBy(0, 1000);"
driver.execute_script(scroll_script)
# Click the Jobs icon
jobs_icon.click()
print("Clicked on the LinkedIn Jobs icon!")

# Wait briefly before navigating to search results
time.sleep(3)

# Navigate to the job search results page
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3858690441&geoId=102713980&keywords=data&location=India&origin=JOBS_HOME_LOCATION_HISTORY&refresh=true")
print("Navigated to job search results.")


# VISIT HOME & JOB PAGE ENDS ------------------------------------------------------------------------------------------------

links = set()
global max_page, current_page
max_page = 2
current_page = 1

# NAVIGATE JOB LISTINGS NOW ------------------------------------------------------------------------------------------------
def get_links():
    try :
        # Wait for the job listings container to be visible
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container")))  
        jobs_list = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item") 

        # loop through jobs in job list
        # When scroll happens, we can locate all the classes (else only 7 / 25)
        container_element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results-list")))
        print("FOUND THE PLACE TO SCROLL")
        scroll_script = "arguments[0].scrollBy(0, 500);"

        # Scroll multiple times (adjust the range as needed)
        for i in range(7):  # Example: Scroll 5 times
            # Execute the JavaScript scroll command
            print("SCROLL KIYA RE")
            driver.execute_script(scroll_script, container_element)
            time.sleep(1)

        
        for job in jobs_list : 
            job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            if job_link.startswith("https://www.linkedin.com/jobs/view"):
                links.add(job_link)

        for link in links : 
            print(link)
        print(len(links))
        

    except Exception as e:
        print(f"Error occurred: {e}")

    # Go to the next page
    # Linkedin doesn't have a next button so we identify button type in page numbers
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container")))

    xpath = "//button[@aria-label='Page " + str(current_page) + "']"

    button = WebDriverWait(driver, 1).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    
    button.click()
    print("PAGE NUMBER BUTTON FOUND")
    time.sleep(3)
    
while current_page < max_page:
    current_page = current_page+1
    get_links()
    
    
    
# NAVIGATE JOB LISTINGS ENDS ------------------------------------------------------------------------------------------------



# SCRAPING STARTS ------------------------------------------------------------------------------------------------------- 

# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []


i = 0
j = 1
# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
for i in range(len(links)):
    try:
        driver.get(links[i])
        i=i+1
        time.sleep(2)
        # Click See more.
        driver.find_element(By.CLASS_NAME, "artdeco-card__actions").click()
        print("first find works")
        time.sleep(2)
    except:
        pass


# Locate the fields we need to scrape
# use find_elements_by_class_name() with clas name = p5
contents = driver.find_elements(By.CLASS_NAME, "jobs-search__job-details--wrapper")
print(contents)
for content in contents:
    print(content)
    print("BEFORE TRY BLOCK")
    try:
        print("After TRY BLOCK")
        job_title_element = content.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title")
        job_title_text = job_title_element.text
        job_titles.append(job_title_text)
        print(job_titles)
        company_names.append(content.find_element(By.CSS_SELECTOR, ".job-details-jobs-unified-top-card__primary-description-without-tagline.mb2").text)
        company_locations.append(content.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title").text)
        work_methods.append(content.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title").text)
        post_dates.append(content.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title").text)
        work_times.append(content.find_element(By.CSS_SELECTOR, "h2.t-24.t-bold.job-details-jobs-unified-top-card__job-title").text)
        print('Scraping the Job Offer '+ str(j)+' DONE.')

        j+=1
            
    except:
        pass
    time.sleep(2)


# Take whole text in job description 
# Scraping the job description
    job_description = driver.find_elements(By.CLASS_NAME,'jobs-description__content')
    for description in job_description:
        job_text = description.find_element(By.CLASS_NAME,"jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer '+ str(j))
        time.sleep(2) 



# SCRAPING ENDS ------------------------------------------------------------------------------------------------------------ 




# Store in csv file ---------------------------------------------------------------------------------------------------------

# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
 company_locations,work_methods,
 post_dates,work_times)),
 columns =["job_title", "company_name",
 "company_location","work_method",
 "post_date","work_time"])
# Storing the data to csv file
df.to_csv("job_offers.csv", index=False)
# Output job descriptions to txt file
with open("job_descriptions.txt", "w",encoding="utf-8") as f:
 for line in job_desc:
  f.write(line)
  f.write("\n")


# Store in csv file ENDS ---------------------------------------------------------------------------------------------------------
