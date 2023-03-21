from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException    
import re
import pandas as pd
import time
import datetime
import sqlite3



options = webdriver.ChromeOptions()
#options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("--start-maximized")
PATH = r"C:\Users\grego\Dev\Data and IR\Abstimmungsverhalten_v2\chromedriver_win32.exe"

# Getting link list (we maybe could write this a as a function elsewhere and just call it here)

# Set up the webdriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Navigate to the relevant page
driver.get("https://www.bundestag.de/abgeordnete/biografien")

# Expand the page to show all MPs
button = driver.find_element(By.CSS_SELECTOR, '.bt-link-list[href="javascript:void(0);"]')
button.click()
time.sleep(5)

# Get the links of all MPs
try:
    links = [i.get_attribute('href') for i in driver.find_elements(By.CSS_SELECTOR, 'a[href^="/abgeordnete"]')]
    print('Success!!!')
    print(f'Found {len(links)} links.')
except Exception as e:
    print('Error:', e)

# Quit the webdriver
driver.quit()


# working with the links liste generated above. we need to filter out the wrong links first before iterating over it and fetching the relevant information

regex = 'biografien\/[a-zA-Z]\/'

falsche_links = []
richtige_links = []

for lnk in links:
    if bool(re.search(regex, lnk)):
        richtige_links.append(lnk)
    else:
        falsche_links.append(lnk)

print(len(falsche_links))
print(len(richtige_links))


# thinking how to include vote retrieval

def retrieve_votes(lnk):
    df_abstimmungen_selenium = pd.DataFrame()
    
    def check_abstimmungen_exists():
        try:
            driver.find_element(By.LINK_TEXT, 'Abstimmungen')
        except NoSuchElementException:
            return False
        return True
    
    driver.get(lnk)
    if check_abstimmungen_exists() == True:
        try:
            link = driver.find_element(By.LINK_TEXT, 'Abstimmungen')
            link.click()

            link = driver.find_element(By.CSS_SELECTOR, 'button.bt-button.bt-button--icon-right.bt-button--show-more.loadMore[type="submit"]')
            link.click()

            page_source = driver.page_source
            table = pd.read_html(page_source)

            df = table[0]
            id_stripped = re.findall("\d+", str(lnk))
            df['bundestags_id'] = id_stripped[0]
            data = df.iloc[:-1 , :]

            df_abstimmungen_selenium = df_abstimmungen_selenium.append(data,ignore_index=True)

        except Exception as e:
                #driver.quit()
                print('duh!!!!!')
                print('Error:', e)

    else:
        data = ['Keine Abstimmungen']
        df_abstimmungen_selenium = df_abstimmungen_selenium.append(data,ignore_index=True)

    return df_abstimmungen_selenium




#creating the lists that eventually will form the dataframe

bundestags_id = []
wahlkreis = []
nachnamen = []
vornamen = []
facebook_links = []
instagram_links = []
twitter_links = []
website_links = []

df_politiker_selenium = pd.DataFrame()
df_abstimmungen_selenium = pd.DataFrame()



start_time = time.time()


#iterating over all  pages and getting the relevant information into df
driver = webdriver.Chrome(PATH)

# to verify the existence of elements

def check_link_exists(link_text):
    try:
        driver.find_element(By.CSS_SELECTOR, f'.bt-link-extern[title^="{link_text}"]')
    except NoSuchElementException:
        return False
    return True

def check_abstimmungen_exists():
    try:
        driver.find_element(By.LINK_TEXT, 'Abstimmungen')
    except NoSuchElementException:
        return False
    return True



#for test
i = 0




for lnk in richtige_links:
    driver.get(lnk)
    
    webpage_exists = check_link_exists("Homepage")
    facebook_exists = check_link_exists("Facebook")
    twitter_exists = check_link_exists("Twitter")
    instagram_exists = check_link_exists("Instagram")
    wahlkreis_exists = check_link_exists("Wahlkreis")

    try:
        #bundestags_id
        id_stripped = re.findall("\d+", lnk)
        bundestags_id.append(id_stripped[0])
        
        # names --- !!!! derzeit sind es nicht immer die korrekten namen. besser sie aus dem namenselement statt dem titel zu ziehen
        # NOCH UNKLAR: Welcher Name soll gewählt werden... in welchem Format. Hier scheinen Abweichungen auf der Website, bei manchen wird z.b. (Heilbronn) mitübergeben.
        get_title = driver.title
        nachnamen.append(re.findall("\w+", get_title)[-1])
        vornamen.append(re.findall("\w+", get_title)[-2])

        # wahlkreis
        if wahlkreis_exists == True:
            search = driver.find_element(By.CSS_SELECTOR, '.bt-link-intern[title^="Wahlkreis"]').get_attribute('innerHTML')
            wahlkreis.append(search)
        else: #gibt mir das Bundesland
            search = driver.find_element(By.CSS_SELECTOR, '.bt-standard-content.col-sm-6.col-xs-12').get_attribute('innerHTML')
            land = re.findall('\>(.*)\<', search)
            wahlkreis.append('Landesliste:' + str(land))

        # links
        if webpage_exists == True:
            element = driver.find_element(By.CSS_SELECTOR, '.bt-link-extern[title^="Homepage"]')
            website_links.append(element.get_attribute('href'))
        else:
            website_links.append('keine auf Bundestagsseite')

        if facebook_exists == True:
            element = driver.find_element(By.CSS_SELECTOR, '.bt-link-extern[title^="Facebook"]')
            facebook_links.append(element.get_attribute('href'))
        else:
            facebook_links.append('keine auf Bundestagsseite')

        if twitter_exists == True:
            element = driver.find_element(By.CSS_SELECTOR, '.bt-link-extern[title^="Twitter"]')
            twitter_links.append(element.get_attribute('href'))
        else:
            twitter_links.append('keine auf Bundestagsseite')
            
        if instagram_exists == True:
            element = driver.find_element(By.CSS_SELECTOR, '.bt-link-extern[title^="Instagram"]')
            instagram_links.append(element.get_attribute('href'))
        else:
            instagram_links.append('keine auf Bundestagsseite')
       

    except Exception as e:
        #driver.quit()
        print('duh!!!!!')
        print('Error:', e)
    
    if check_abstimmungen_exists() == True:
        try:
            link = driver.find_element(By.LINK_TEXT, 'Abstimmungen')
            link.click()

            link = driver.find_element(By.CSS_SELECTOR, 'button.bt-button.bt-button--icon-right.bt-button--show-more.loadMore[type="submit"]')
            link.click()

            page_source = driver.page_source
            table = pd.read_html(page_source)

            df = table[0]
            id_stripped = re.findall("\d+", str(lnk))
            df['bundestags_id'] = id_stripped[0]
            data = df.iloc[:-1 , :]

            df_abstimmungen_selenium = df_abstimmungen_selenium.append(data,ignore_index=True)

        except Exception as e:
                #driver.quit()
                print('duh!!!!!')
                print('Error:', e)

    else:
        data = ['Keine Abstimmungen']
        df_abstimmungen_selenium = df_abstimmungen_selenium.append(data,ignore_index=True)
    
     # to test this loop with 5 iterations
    #i = i + 1
    #if i == 2:
        #break



df_politiker_selenium['bundestags_id'] = bundestags_id
df_politiker_selenium['vorname'] = vornamen
df_politiker_selenium['nachname'] = nachnamen
df_politiker_selenium['wahlkreis'] = wahlkreis
df_politiker_selenium['facebook_links'] = facebook_links
df_politiker_selenium['twitter_links'] = twitter_links
df_politiker_selenium['website_links'] = website_links
df_politiker_selenium['instagram_links'] = instagram_links

end_time = time.time()
total_time = end_time - start_time

print("Time taken: ", total_time, "seconds")



timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# save the dataframe to a CSV file with the timestamp in the filename
filename1 = f'df_politiker_selenium_{timestamp}.csv'
filename2 = f'df_abstimmungen_selenium_{timestamp}.csv'
df_politiker_selenium.to_csv(filename1, index=False)
df_abstimmungen_selenium.to_csv(filename2, index=False)


# adding the dataframes to the App's database for further use (ideally we'd clean it before)
conn = sqlite3.connect('database.db')
df_politiker_selenium.to_sql('df_politiker_selenium', conn, if_exists='replace', index=False)
df_abstimmungen_selenium.to_sql('df_abstimmungen_selenium', conn, if_exists='replace', index=False)
