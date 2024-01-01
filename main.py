import csv

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def main():
    weather_list = []
    start = False

    driver.get('https://yandex.kz/pogoda/month?lat=43.273564&lon=76.914851&via=hnav')
    driver.implicitly_wait(0.5)
    table = driver.find_element(By.CLASS_NAME, 'climate-calendar')
    rows = WebDriverWait(table, 20).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, 'tr'))
    )
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, 'td')
        for cell in cells:
            if 'Усреднённые' in cell.text:
                break
            weather_details = cell.text.split('\n')
            if '1' in weather_details[0]:
                start = True
            if start is False:
                continue
            if len(weather_details) > 2:
                day = weather_details[0] if weather_details[0].isdigit() else weather_details[0].split(' ')[0]
                day_t = weather_details[-2]
                night_t = weather_details[-1]
                weather_list.append([day, day_t, night_t])
                print(f'day: {day}, day_t: {day_t}, night_t: {night_t}')
    driver.quit()

    csv_file_path = 'parsed_weather_data.csv'

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Day', 'Day Temperature', 'Night Temperature'])
        csv_writer.writerows(weather_list)


if __name__ == "__main__":
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    main()