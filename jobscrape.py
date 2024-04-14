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
global max_page, current_page, job_titles, company_names, company_locations, work_methods, post_dates, work_times, job_desc, applicants
max_page = 30
current_page = 1


# Create empty lists to store information
job_titles = []
company_names = []
company_locations = []
work_methods = []
post_dates = []
work_times = [] 
job_desc = []
applicants = []

# NAVIGATE JOB LISTINGS NOW ------------------------------------------------------------------------------------------------
def get_links():
    try :
        # Wait for the job listings container to be visible
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "scaffold-layout__list-container")))  
        jobs_list = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results__list-item") 
        print(jobs_list)
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
        print("STOPPED SCROLLING BITCH")
        
        for job in jobs_list :
            print("ENTERING LINKING LOOP")
            job_link = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            print(job_link)
            if job_link.startswith("https://www.linkedin.com/jobs/view"):
                links.add(job_link)
                print("LINK ADDED")

        for link in links :
            print("PRINTING LINKS")
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
   
							  
								 
			   
	
	
	
# NAVIGATE JOB LISTINGS ENDS ------------------------------------------------------------------------------------------------



while current_page < max_page:
    current_page = current_page+1
    get_links()
			   
				  
					  
				 
			   
				
			 

# SCRAPING STARTS ------------------------------------------------------------------------------------------------------- 

	 
j = 1

# Visit each link one by one to scrape the information
print('Visiting the links and collecting information just started.')
print(len(links))


# INSERT LOOP HERE


for link in links:
    print("PRINTING THE LINK TO GO TO ", )
    try:
        print("PRINTING THE LINK TO GO TO ", link)
        driver.get(link)
        time.sleep(2)
        # Click See more.

        print("Click see more")
        xpath = "//button[@aria-label='Click to see more description']"

        button = WebDriverWait(driver, 1).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
    
        button.click()
        print("see more clicked")
        time.sleep(2)


        # Locate the fields we need to scrape
        # use find_elements_by_class_name() with clas name = p5
        contents = driver.find_elements(By.CLASS_NAME, "p5")


        #-------FOR LOOP HERE ------------------
        for content in contents:
            print(content)
            print("BEFORE TRY BLOCK")
            try:
                print("After TRY BLOCK")
                # Find the parent div element
                parent_div = driver.find_element(By.CLASS_NAME, "job-details-jobs-unified-top-card__primary-description-without-tagline.mb2")

                # Extract text content from the parent div
                parent_div_text = parent_div.text

                # Split the text content by "·" character and take the second part as location
                div_text_parts = parent_div_text.split("·")
                if len(div_text_parts) > 1:
                    company_loc = div_text_parts[1].strip()
                else:
                    company_loc = ""
                company_locations.append(company_loc)
                print("Location:", company_locations)

                # Extract mode of posting from the span with class name "tvm__text"
                postings = parent_div.find_element(By.CLASS_NAME, "tvm__text").text
                post_dates.append(postings)
                
                # Extract posting date from the last span
                applications = parent_div.find_elements(By.TAG_NAME, "span")[-1].text
                applicants.append(applications)
                
                # Output the extracted information

                print("Location:", company_locations)
                print("Posted when:", post_dates)
                print("Applicants:", applicants)

                # Find all parent span elements with the class name "ui-label--accent-3"
                parent_spans = driver.find_elements(By.CSS_SELECTOR, "span.ui-label.ui-label--accent-3.text-body-small")

                # Initialize lists to store the extracted data

                # Loop through each parent span
                for parent_span in parent_spans:
                    # Find the first span element inside the parent span
                    child_span = parent_span.find_element(By.TAG_NAME, "span")
                    
                    # Extract the text content from the child span
                    span_text = child_span.text.strip()
                    
                    # Append the extracted text to the respective list based on the index of the parent span
                    if parent_span == parent_spans[0]:
                        work_methods.append(span_text)
                    else:
                        work_times.append(span_text)

                # Output the extracted data
                print("work_methods:", work_methods)
                print("work_times", work_times)

                
                job_title_element = content.find_element(By.CSS_SELECTOR, "h1.t-24.t-bold.job-details-jobs-unified-top-card__job-title")
                job_title_text = job_title_element.text
                job_titles.append(job_title_text)
                                
                                                                                                                                                            
                                                                                                                                                
                                                                                                                                            
                                                                                                                                            
                                                                                                                                            
                                                                

                # Extract company name from the first <a> tag
                company_name = parent_div.find_element(By.TAG_NAME, "a").text
                company_names.append(company_name)
                print("Company Name:", company_names)
                
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


        #-------FOR LOOP ENDS HERE ------------------


    except:
        pass



# SCRAPING ENDS ------------------------------------------------------------------------------------------------------------ 




# Store in csv file ---------------------------------------------------------------------------------------------------------

# Creating the dataframe 
df = pd.DataFrame(list(zip(job_titles,company_names,
 company_locations,work_methods,
 post_dates,work_times, applicants, job_desc)),
 columns =["job_title", "company_name",
 "company_location","work_method",
 "post_date","work_time", "applicants","job_desc"])
# Storing the data to csv file

df.to_csv("job_offers.csv", index=False)

'''
# Output job descriptions to txt file
with open("job_descriptions.txt", "w",encoding="utf-8") as f:
 for line in job_desc:
  f.write(line)
  f.write("\n")
'''


# Store in csv file ENDS ---------------------------------------------------------------------------------------------------------
