# Этот код автоматизирует процесс извлечения информации о рецептах с сайта `eda.ru` 
# с помощью Selenium и записывает эту информацию в файл CSV.

# 1. Импортированные модули: 
# - selenium: библиотека для автоматизации управления браузером; 
# - webdriver, By, Options: классы, необходимые для выполнения веб-драйвера Chrome; 
# - WebDriverWait, EC: классы для ожидания элементов на странице; 
# - time: модуль для организации временных задержек; 
# - csv: модуль для работы с CSV-файлами.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv


# Устанавливаем заголовок User-Agent  
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"  
options = Options()  
options.add_argument(f'{user_agent}')  
options.add_argument('--ignore-certificate-errors-spki-list')

# options.add_argument("--headless")  
  
driver = webdriver.Chrome(options=options)  
try:  
    # Заходим на веб-сайт и ждем пока загрузится содержимое  
    driver.get('https://eda.ru')  
    wait = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'body')))  
  
    # Переходим к разделу рецептов  
    recipes = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/header/div/div/div[1]/ul/li[2]/a')  
    recipes.click()  
    size_length = driver.execute_script("return document.documentElement.scrollHeight")  
    print(size_length)  
  
    # Прокручиваем страницу пока не достигнем конца  
    while True:  
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")  
        time.sleep(7)  
        size_new = driver.execute_script("return document.documentElement.scrollHeight")  
        if size_new == size_length:  
            break  
        size_length = size_new  
        print(size_new)  
    print(size_new)  
  
    # Находим элементы с названиями рецептов, ингредиентами и временем приготовления  
    recipe_name = driver.find_elements(By.XPATH, '//*[@id="__next"]//*[contains(@class,"emotion-m0u77r")]/div/div[2]/div[3]/a/span[@class="emotion-1bs2jj2"]')  
    ingredients = driver.find_elements(By.XPATH, '//*[@id="__next"]//*[contains(@class,"emotion-d6nx0p")]')  
    cooking_time = driver.find_elements(By.XPATH, '//*[@id="__next"]//*[contains(@class,"emotion-14gsni6")]')  
  
    # Создаем заголовок таблицы и записываем данные в CSV-файл  
    top_line  = ['number', 'recipe_name', 'ingredients', 'cooking_time']  
    with open('recipes.csv', 'w', encoding='UTF-8', newline='') as f:  
        csv_write = csv.writer(f, dialect='excel', delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)  
        csv_write.writerow(top_line)  
        for i, element in enumerate(zip(recipe_name, ingredients, cooking_time)):  
            line = [i, element[0].text, element[1].text, element[2].text]  
            csv_write.writerow(line)  
            # print(line)  
except Exception as er:  
    print(f'Ошибка {er}')  
finally:  
    driver.quit()