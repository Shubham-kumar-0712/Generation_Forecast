from datetime import date
from selenium import webdriver
import time


def sel(url):
    driver = webdriver.Chrome()  # navigate to the URL you want to save
    driver.get(url)  # get the page source
    page_source = driver.page_source  # save the page source to a file
    with open(r"C:\Users\skliv\PycharmProjects\generation_forecast\HTML_files\forecast.html",
              "w", encoding="utf-8") as f:
        f.write(page_source)  # close the webdriver instance

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
