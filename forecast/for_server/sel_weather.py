from datetime import date
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def sel(url):
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    chrome_options.add_argument("user-agent={}".format(user_agent))
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)  # navigate to the URL you want to save
    driver.get(url)  # get the page source
    page_source = driver.page_source  # save the page source to a file

    soup = BeautifulSoup(page_source, 'html.parser')
    print(soup)
    time.sleep(10)
    driver.quit()


if __name__ == '__main__':

    todays_date = date.today()
    number_to_month = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june', 7: 'july', 8: 'august',
                       9: 'september', 10: 'october', 11: 'november', 12: 'december'}

    for k, v in number_to_month.items():
        if k == todays_date.month:
            month_name = v

    url = "https://www.accuweather.com/en/in/gadag-betigeri/2849071/{0}-weather/2849071".format(month_name)

    sel(url)


