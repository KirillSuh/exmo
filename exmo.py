from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pynput.keyboard import Key, Listener
import datetime
import time
import ast
import sys

homepath = '/home/shinod/'

browser = webdriver.Chrome(homepath+'chromedriver')
browser.get('https://exmo.me/ru/login')

timeout = 10
myhbz = 9959
myhbz_price = 0.0152
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
            with open(homepath+'exmo/result.txt', 'a') as file:
                file.write(
                    'Продано: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price)+ ' Количество ' + str(myhbz) + ' На счету ' + str(myusd) + '\n')
        if key_press.char == 's':
            content = browser.find_element_by_css_selector('#mCSB_6_container .trade_table tbody tr:nth-of-type(2)')
            price_td = content.find_element_by_class_name('tcol_price')
            price = price_td.text
            print(price)
            content.click()
        if key_press.char == 'p':
            auto_broker()


def auto_broker():
        global myhbz, myhbz_price, myusd, can_sell, homepath
        while 0 != 1:
            time.sleep(1)
            if myhbz != 0 and int(can_sell) == 1:
                try:
                    content = browser.find_element_by_css_selector('#mCSB_5_container .trade_table tbody tr:nth-of-type(2)')
                    price_td = content.find_element_by_class_name('tcol_price')
                    count_td = content.find_element_by_class_name('tcol_count')
                    price = price_td.text
                    count = count_td.text
                    print(str(float(price)))
                    if float(price) > float(myhbz_price)*1.01:
                        print(str(float(price)) + ' ' + str(float(myhbz_price)))
                        if float(count) >float(myhbz):
                            myusd = myusd + float(myhbz) * float(price)
                            myhbz = 0
                            with open(homepath + 'exmo/result.txt', 'a') as file:
                                file.write('Продано: ' + datetime.datetime.now().strftime(
                                    "%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(
                                    myhbz) + ' На счету ' + str(myusd) + ' HBZ ' + str(myhbz) + '\n')
                        else:
                            myusd = myusd + float(count) * float(price)
                            myhbz = float(myhbz) - float(count)
                            with open(homepath + 'exmo/result.txt', 'a') as file:
                                file.write('Продано: ' + datetime.datetime.now().strftime(
                                    "%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(
                                    count) + ' На счету ' + str(myusd) + ' HBZ ' + str(myhbz) + '\n')
                        if float(myhbz) == 0:
                            myhbz_price = price
                            can_sell = 0
                except:
                    print("Снова не найден: ", sys.exc_info()[1])
            else:
                try:
                    content = browser.find_element_by_css_selector('#mCSB_4_container .trade_table tbody tr:nth-of-type(2)')
                    price_td = content.find_element_by_class_name('tcol_price')
                    count_td = content.find_element_by_class_name('tcol_count')
                    price = price_td.text
                    count = count_td.text
                    print(price)
                    if float(price) < float(myhbz_price)*0.99:
                        print(str(float(price)) + ' ' + str(float(myhbz_price)))
                        if float(count) * float(price) > float(myusd):
                            count = float(myusd) / float(price)
                            myhbz = float(myhbz) + float(count)
                            myusd = 0
                            with open(homepath+'exmo/result.txt', 'a') as file:
                                file.write('Куплено: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(count) + ' На счету ' + str(myusd) + ' HBZ ' + str(myhbz) + '\n')
                        else:
                            myhbz = float(myhbz) + float(count)
                            myusd = float(myusd) - float(price) * float(count)
                            with open(homepath+'exmo/result.txt', 'a') as file:
                                file.write(
                                    'Куплено: ' + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ' Цена ' + str(price) + ' Количество ' + str(count) + ' На счету ' + str(myusd) + ' HBZ ' + str(myhbz) + '\n')
                        if float(myusd) == 0:
                            can_sell = 1
                except:
                    print("Снова не найден при продаже: ", sys.exc_info()[1])


with Listener(on_press=on_press) as listener:
    listener.join()
