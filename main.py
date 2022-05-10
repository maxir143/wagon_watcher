import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from gtts import gTTS
from playsound import playsound


def main():
    def login(driver, user, password):
        driver.get('https://tortops.com/')
        print(driver.title)
        time.sleep(3)

        user_input = driver.find_element(by=By.ID, value='mat-input-0')
        pass_input = driver.find_element(by=By.ID, value='mat-input-1')
        submit_button = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-layout/section/app-login/section/mat-card/mat-card-footer/button')

        user_input.send_keys(user)
        pass_input.send_keys(password)
        time.sleep(1)
        submit_button.click()
        time.sleep(5)
        return driver.title

    def get_vehicles_ids(driver):
        driver.get('https://tortops.com/#/vehiclesAdmin')
        time.sleep(3)

        wagon_info_cards = driver.find_elements(by=By.CLASS_NAME, value='vehiclesadmin-vehicle-div')
        time.sleep(1)

        return [card.find_element(by=By.CLASS_NAME, value='vehiclesadmin-id-container').text for card in wagon_info_cards]

    def new_vehicles(old_list, new_list):
        return [wagon_id for wagon_id in new_list if wagon_id not in old_list]

    def scraper_wagon_ids():
        USER = 'maximiliano.valentin@tortoise.dev'
        PASS = 'teleoperador'
        browser = webdriver.Chrome(ChromeDriverManager().install())
        login(browser, USER, PASS)
        request_wagon_id_list = get_vehicles_ids(browser)
        browser.quit()

        return request_wagon_id_list

    new_wagon_list = []
    old_wagon_list = []

    def text_to_speech(message):
        format_text = f'{message}.mp3'
        speech = gTTS(text=message)
        speech.save(format_text)
        time.sleep(1)
        playsound(format_text)
        time.sleep(1)
        os.remove(format_text)

    while True:
        new_wagon_list = scraper_wagon_ids()
        new = new_vehicles(old_wagon_list, new_wagon_list)
        old_wagon_list = new_wagon_list
        for id in new:
            text_to_speech(f'Wagon {id} connected')
        time.sleep(5)


if __name__ == '__main__':
    main()
