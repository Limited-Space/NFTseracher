from calendar import month
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
from webdriver_manager.chrome import ChromeDriverManager
#Installs or initiates automaticall chromium
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options= chrome_options)

def fetch_data():
    #Sorted List
    sorted_information = []

    #Goes to link
    driver.get("https://rarity.tools/upcoming/")
    #Checks the availability of the tables
    try:
        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[5]')))
    except:
        print('First month missing!')
        driver.quit()

    #Gives data to BeautifulSoup
    parsed_page = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    #Extracts tables
    nuxt_div = parsed_page.div
    layout_div = nuxt_div.find(attrs={'id': '__layout'})
    main_page = layout_div.div
    lower_half = main_page.find(attrs={'class': "w-full p-4 pb-20 overflow-auto infoPage"})
    for month_div in lower_half.find_all(attrs={'class': None}):
        if month_div.find('table', attrs={'class': 'relative m-auto dataTable upcoming'}) != None:
            table = month_div.find('table', attrs={'class': 'relative m-auto dataTable upcoming'})
            nft_components = table.find_all(attrs={'class': 'text-left text-gray-800'})
            for nft_component in nft_components:
                #Format results
                name = nft_component.find(attrs={'class': 'text-lg font-bold text-pink-700 dark:text-gray-300', 'style': 'max-width: 600px;'})
                theme = nft_component.find(attrs={'class': None, 'style': 'max-width: 600px;'})
                links = nft_component.find_all('a', attrs={'class': 'text-pink-600 hover:underline', 'target': '_blank'})
                price = nft_component.find(attrs={'class': 'font-bold text-green-500'})
                size = price.find_next_sibling('div')
                times_included = nft_component.find('td', attrs={'class': 'block clear-both mb-4 lg:mb-0 lg:table-cell lg:align-center'})
                printed_name = name.text.replace('\n', '')
                printed_theme = theme.text.replace('\n', '')
                printed_price = price.text.replace('\n', '')
                printed_size = size.text.replace('\n', '')
                printed_time = "Not Disclosed"
                printed_date = "Not Disclosed"
                discord_link = "Not Disclosed"
                twitter_link = "Not Disclosed"
                website_link = "Not Disclosed"
                if times_included.find('div', attrs={'class': 'flex flex-row lg:flex-col'}) != None:
                        printed_date = times_included.find('div', attrs={'class': 'flex flex-row lg:flex-col'}).text
                for link in links:
                    if link.text is not None:
                        if 'discord' in link['href']:
                            discord_link = 'Discord link: ' + link['href']
                        elif 'twitter' in link['href']:
                            twitter_link = 'Twitter link: ' + link['href']
                        elif link['href'] == 'https://TBA':
                            website_link = 'Website link is not out yet...'
                        else:
                            website_link = 'Website link: ' + link['href']
                for time in times_included.find_all('div'):
                    if ':' in time.text.replace('\n', ''):
                        printed_time = re.sub(' +', ' ', time.text.replace('\n', '').strip())
                sorted_information.append({'name': printed_name.strip(), 'theme': printed_theme.strip(), 'price': printed_price.strip(), 'quantity': printed_size.strip(), 'time': printed_time, 'date': printed_date.strip(), "discord": discord_link, "twitter": twitter_link, "website": website_link})
    today_posts = []
    for post in sorted_information:
        if post['date'] == 'Today':
            today_posts.append(post)
    #Outputs results in a json format, which can be outputted to any text/json file
    result = json.dumps(today_posts, indent=2)
    print(result)
    print("\n------------------END------------------")

fetch_data()