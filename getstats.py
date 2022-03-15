from selenium import webdriver
from selenium.webdriver.firefox.options import Options 
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import sqlite3

def save_data(youtube,twitter,instagram):

  record = {
    'date': datetime.now().strftime('%-d %b %Y'),
    'youtube': youtube,
    'twitter': twitter,
    'instagram': instagram
  }

  con = sqlite3.connect('followers.db')
  cur = con.cursor()

  cur.execute('''
     CREATE TABLE IF NOT EXISTS monthly_stats(
       date TEXT, youtube INTEGER, twitter INTEGER, instagram INTEGER
     )
  ''')

  insert = cur.execute(
    'INSERT INTO monthly_stats VALUES ("%s", %s, %s, %s)' % (record['date'], record['youtube'], record['twitter'], record['instagram'])
  )

  con.commit()
  con.close()



# Set up webdriver
options = Options()
options.add_argument('--headless')
s=Service('./geckodriver')
driver = webdriver.Firefox(service=s, options=options)
driver.implicitly_wait(10)

# Youtube
driver.get('https://www.youtube.com/c/Datacamp')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
cookies = driver.find_element(By.XPATH, '//span[text()="I agree"]')
ActionChains(driver).move_to_element(cookies).click().perform()

youtube_count = int(driver.find_element(By.ID,'subscriber-count').text.split(' ')[0][0:3])

# Twitter
driver.get('https://twitter.com/DataCamp?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor')
twitter_count =  int(driver.find_element(By.XPATH, '//span[text()="64.5K"]').text[0:2])

# Instagram
driver.get('https://www.picuki.com/profile/datacamp')
instagram_count = int(driver.find_element(By.XPATH, '//span[text()="140,366"]').text[0:3])


# Close the driver
driver.close()

# Save the data
save_data(youtube_count,twitter_count,instagram_count)








