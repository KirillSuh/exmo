from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pynput.keyboard import Key, Listener
import pyautogui
import datetime
import ast

browser = webdriver.Chrome('/home/kirill/chromedriver')
browser.get('https://exmo.me/ru/login')

timeout = 10
myhbz = 10000
myhbz_price = 0.0162
can_sell = 1
myusd = 0
try:
    element_present = EC.presence_of_element_located((By.ID, 'reg_form_login'))  # type: object
    WebDriverWait(browser, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")


def on_press(key):
    key_press = key
    print("Pressed", key)
    if key_press == Key.esc:
        return False
    if hasattr(key_press,'char'):
        if key_press.char == 'a':
            emailinput = browser.find_element_by_id('reg_form_login')
            passwordinput = browser.find_element_by_id('reg_form_pass')
            emailinput.send_keys('shinodkir@gmail.com')
            passwordinput.send_keys('')
        if key_press.char == 'b':
            content = browser.find_element_by_css_selector('#mCSB_5_container .trade_table tbody tr:nth-of-type(2)')
            price_td = content.find_element_by_class_name('tcol_price')
            price = price_td.text
            print(price)
            content.click()
            with open('/home/kirill/exmo/result.txt', 'a') as file:
                file.write(
                    'Продано: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price)+ ' Количество ' + str(myhbz) + ' На счету ' + str(myusd))
        if key_press.char == 's':
            content = browser.find_element_by_css_selector('#mCSB_6_container .trade_table tbody tr:nth-of-type(2)')
            price_td = content.find_element_by_class_name('tcol_price')
            price = price_td.text
            print(price)
            content.click()
        if key_press.char == 'p':
            auto_broker()


def auto_broker():
        global myhbz, myhbz_price, myusd, can_sell
        while 0 != 1:
            if myhbz != 0 and int(can_sell) == 1:
                content = browser.find_element_by_css_selector('#mCSB_6_container .trade_table tbody tr:nth-of-type(2)')
                price_td = content.find_element_by_class_name('tcol_price')
                count_td = content.find_element_by_class_name('tcol_count')
                price = price_td.text
                count = count_td.text
                if ast.literal_eval(price) > myhbz_price*1.01:
                    if ast.literal_eval(count) >ast.literal_eval(myhbz):
                        myusd = ast.literal_eval(myhbz) * ast.literal_eval(price)
                        with open('/home/kirill/exmo/result.txt', 'a') as file:
                            file.write('Продано: '+datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(myhbz) + ' На счету ' + str(myusd))
                        myhbz = 0
                    else:
                        myusd = ast.literal_eval(count) * ast.literal_eval(price)
                        with open('/home/kirill/exmo/result.txt', 'a') as file:
                            file.write('Продано: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(count) + ' На счету ' + str(myusd))
                        myhbz = myhbz - ast.literal_eval(count)
                    if myhbz == 0:
                        myhbz_price = price
                        can_sell = 0
            else:
                content = browser.find_element_by_css_selector('#mCSB_5_container .trade_table tbody tr:nth-of-type(2)')
                price_td = content.find_element_by_class_name('tcol_price')
                count_td = content.find_element_by_class_name('tcol_count')
                price = price_td.text
                count = count_td.text
                if ast.literal_eval(price) < myhbz_price*1.01:
                    if ast.literal_eval(count) * ast.literal_eval(price) > myusd:
                        count = ast.literal_eval(myusd) / ast.literal_eval(price)
                        myhbz = myhbz + count
                        myusd = 0
                        with open('/home/kirill/exmo/result.txt', 'a') as file:
                            file.write('Куплено: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(count) + ' На счету ' + str(myusd))
                    else:
                        myhbz = myhbz + count
                        myusd = myusd - ast.literal_eval(price) * ast.literal_eval(count)
                        with open('/home/kirill/exmo/result.txt', 'a') as file:
                            file.write(
                                'Куплено: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(count) + ' На счету ' + str(myusd))
                    if myusd == 0:
                        can_sell = 1


with Listener(on_press=on_press) as listener:
    listener.join()
