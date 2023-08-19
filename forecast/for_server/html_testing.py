from bs4 import BeautifulSoup


def forecast(file_name):
    files = open(file_name, "r")

    # Reading the file and storing in a variable
    contents = files.read()

    soup = BeautifulSoup(contents, 'html.parser')

    a = soup.findAll('div', class_="date")
    b = soup.findAll('div', class_="high")
    c = soup.findAll('div', class_="low")
    d = soup.findAll('div', class_="map-dropdown-toggle")

    print(soup)
    print(a)


if __name__ == '__main__':
    forecast_table = forecast(r'C:/Users/skliv/PycharmProjects/generation_forecast/HTML_files/forecast.html')
