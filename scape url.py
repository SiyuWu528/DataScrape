#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium')


# In[2]:


get_ipython().system('pip install webdriver_manager')


# In[3]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load Excel file with pandas
df = pd.read_csv('VerifiedContact List.csv')  # Make sure to replace with your actual file path and name


# In[4]:


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver with WebDriver Manager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://www.linkedin.com')


# In[5]:


# For Email or Phone Number Field
email_field = driver.find_element(By.ID, "session_key")

# For Password Field
password_field = driver.find_element(By.ID, "session_password")


# In[6]:


# Now, use these elements with Selenium
email_field.send_keys('@gmail.com')  # Replace with your LinkedIn email
password_field.send_keys('')        # Replace with your LinkedIn password


# In[7]:


from selenium.webdriver.common.by import By


# In[8]:


# Find the sign-in button using its class name and click it
sign_in_button = driver.find_element(By.CSS_SELECTOR, "button.sign-in-form__submit-btn--full-width")
sign_in_button.click()


# In[11]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# In[12]:


# Define an empty list to hold profile URLs
profile_urls = []

# Wait for the search box to be ready
wait = WebDriverWait(driver, 10)

for index, row in df.iterrows():
    # Navigate to LinkedIn search page
    driver.get('https://www.linkedin.com/search/results/people/')
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@class,"search-global-typeahead__input")]')))
    search_box.clear()

    # Enter the search query for the name and press RETURN
    search_query = f"{row['First Name']} {row['Last Name']}"
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)

    try:
        # Wait for the search results to be present on the page or for the no results message
        WebDriverWait(driver, 10).until(
            lambda driver: driver.find_elements(By.CSS_SELECTOR, 'ul.reusable-search__entity-result-list') or 
                           driver.find_elements(By.CSS_SELECTOR, 'h2.artdeco-empty-state__headline'))
        
        # Check if the 'No results found' element is present
        no_results_elements = driver.find_elements(By.CSS_SELECTOR, 'h2.artdeco-empty-state__headline')
        if no_results_elements and "No results found" in no_results_elements[0].text:
            print(f"No results for {row['First Name']} {row['Last Name']}")
            df.at[index, 'LinkedIn URL'] = "No results"
            continue  # Skip to the next iteration if no results are found

        # Extract the URL of the first search result from the specific title link
        profile_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.entity-result__title-text > a.app-aware-link')))
        profile_url = profile_link.get_attribute('href')
        df.at[index, 'LinkedIn URL'] = profile_url

    except TimeoutException:
        print(f"Timed out waiting for results for {row['First Name']} {row['Last Name']}")
        df.at[index, 'LinkedIn URL'] = "Timed out"
    except Exception as e:
        print(f"Error retrieving profile URL for {row['First Name']} {row['Last Name']}: {e}")
        df.at[index, 'LinkedIn URL'] = "Error"
        
# Optionally close the WebDriver session
driver.quit()

# Save the DataFrame with the URLs to a new CSV file
df.to_csv('linkedin_urls.csv', index=False)


# In[ ]:




