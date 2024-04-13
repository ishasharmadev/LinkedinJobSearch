import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


# Path for the chrome driver 
#path = 'C:/Users/Isha/Documents/Machine Learning/Linkedin Job Search/LinkedinJobSearch/chromedriver_win32/chromedriver.exe'
#driver = webdriver.Chrome(path)
driver = webdriver.Chrome()
driver.get("https://www.google.com/")
#driver.quit()


# When launching the browser, make it full screen 
# Maximise window 
driver.maximize_window() 
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)


# Go to linkedin page and login
# Enter the website 
driver.get("https://www.linkedin.com/login")
time.sleep(2)


# Accept the cookies
# Locate the element of Accept button and make program click it
# Use developer tools to insepct the button (Ctrl + Shift + I)
# After spotting the button, we copy the XPath (Copy -> Copy xpath)
# By using find_element_by_xpath() function, we are accessing the button and with the help of click(), we accept the cookies.

#driver.find_element_by_xpath("/html/body/div/main/div[1]/div/section/div/div[2]/button[2]").click()


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


# Repeat same process for Sign in and click it 
# Login in button
# Wait for the button to be clickable (using WebDriverWait)
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'))
)

# Click the button
button.click()
driver.implicitly_wait(30)


# Entered home page now 
# Go to jobs button and search results accordingly
# Access to the Jobs button and click it
# Wait for the Jobs icon to be clickable using WebDriverWait
jobs_icon = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'global-nav__primary-link--active'))
)

# Click the Jobs icon
jobs_icon.click()
print("Clicked on the LinkedIn Jobs icon!")

# Wait briefly before navigating to search results
time.sleep(3)



# Navigate to the job search results page
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3858690441&geoId=102713980&keywords=data&location=India&origin=JOBS_HOME_LOCATION_HISTORY&refresh=true")
print("Navigated to job search results.")

# Wait for the job listings container to be visible

# WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results__list")))


## Works bookamrk--------------------------------------------


try:
    # Wait for the job listings container to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "jobs-search-results__list")))

    # Collect links for job offers
    jobs_list = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item")

    # Use a set to store unique job links
    links = set()
    print("works till line 116")

    # Loop through job listings and extract job links
    for job in jobs_list:
        job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        if job_link.startswith("https://www.linkedin.com/jobs/view"):
            links.add(job_link)

    # Output the collected job links
    print("Collected Job Links:")
    for link in links:
        print(link)

except Exception as e:
    print(f"Error occurred: {e}")


# While collecting the links, we need to scroll down for each job card
# scroll down for each job element

driver.execute_script("arguments[0].scrollIntoView();", job)


# Go to the next page
# Linkedin doesn't have a next button so we identify button type in page numbers
driver.find_element_by_xpath(f"//button[@aria-label='Page {page}']").click()
time.sleep(3)



## --------------------  SCRAPING ------------------------------------- ##

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
        driver.find_element_by_class_name("artdeco-card__actions").click()
        time.sleep(2)
    except:
        pass



# Locate the fields we need to scrape
# use find_elements_by_class_name() with clas name = p5
contents = driver.find_elements_by_class_name('p5')
for content in contents:
    try:
        job_titles.append(content.find_element_by_tag_name("h1").text)
        company_names.append(content.find_element_by_class_name("jobs-unified-top-card__company-name").text)
        company_locations.append(content.find_element_by_class_name("jobs-unified-top-card__bullet").text)
        work_methods.append(content.find_element_by_class_name("jobs-unified-top-card__workplace-type").text)
        post_dates.append(content.find_element_by_class_name("jobs-unified-top-card__posted-date").text)
        work_times.append(content.find_element_by_class_name("jobs-unified-top-card__job-insight").text)
        print(f'Scraping the Job Offer {j} DONE.')
        j+= 1
            
    except:
        pass
    time.sleep(2)


# Take whole text in job description 
# Scraping the job description
    job_description = driver.find_elements_by_class_name('jobs-description__content')
    for description in job_description:
        job_text = description.find_element_by_class_name("jobs-box__html-content").text
        job_desc.append(job_text)
        print(f'Scraping the Job Offer {j}')
        time.sleep(2) 



## ----------------------- SCRAPING ENDS ------------------------------- ##


# Store in csv file 
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


