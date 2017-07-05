# python 3.5

from twilio.rest import TwilioRestClient
from twilio.rest.resources import Connection
from twilio.rest.resources.connection import PROXY_TYPE_SOCKS4
from twilio.rest.resources.connection import PROXY_TYPE_HTTP


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os
import time as Ti


TIMEOUT = 5
account_sid  = None
auth_token = None
twilio_number = None
to_number = None


date_day = {"01":"January", "02":"February", "03":"March", "04":"April", "05":"May",
            "06":"June", "07":"July", "08":"August", "09":"September", "10":"October",
            "11": "November", "12":"December"}

class Alert:
    def __init__(self, restaurant_name, date, times = []):
        self.restaurant_name = restaurant_name
        self.times = []
        self.date = date





class Reservation:
    def __init__(self, time, date, party):
        self.time = time
        self.party = party
        self.date = date



class Restaurant:
    def __init__(self, name, link,  reservations = []):
        self.name = name
        self.reservations = reservations
        self.link = link



def get_settings():

    if os.path.isfile("account.json"):
        json_data = open("account.json").read()
        data = json.loads(json_data)
    else:
        Exception("No 'account.json' file found")


    if data["to_phone_number"]:
        global to_number
        to_number = data["to_phone_number"]

    if data['account_sid'] and data['auth_token'] and data['twilio_number']:
        global account_sid
        global auth_token
        global twilio_number
        account_sid = data['account_sid']
        auth_token = data['auth_token']
        twilio_number = data['twilio_number']
    else:
        Exception("Missing Arguments in 'account.json,' please include account_sid, auth_token, and twilio_number")



def get_availibility(r_list, driver):
    # get restraunt
    for x in r_list:
        # get reservation
        for y in x.reservations:

            driver.get(x.link)

            # get day and date as numbers
            arr = y.date.split('/')
            # turn numeric date to text
            month = date_day[arr[0]]
            day = arr[1]
            # open the calender
            elm = driver.find_element(By.XPATH, '//*[@id="diningAvailabilityForm-searchDateid-base"]/div/button')
            elm.click()
            # get the month at the top of the calender
            elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')
            # until we have the correct month we click the next month
            while(elm.text.lower() != month.lower()):
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/a[2]')
                elm.click()
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')
            # after we find the month we need to find the proper date
            # elements = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody')
            # find the element of the specific date
            elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr//a[text()=' +day +']'  )
            # click the element
            elm.click()
            # click the dropdown list:
            elm = driver.find_element(By.XPATH, '//*[@id="searchTime-wrapper"]/div[1]')
            elm.click()
            # multiple ways to find the time in the DOM, the format for time has to be 'x:xx pm'/'x:xx am'
            elm = driver.find_element(By.XPATH, '//*[@data-display="' +y.time+'"]')
            elm.click()
            # click on dropdown for party size
            elm = driver.find_element(By.XPATH, '//*[@id="partySize-wrapper"]/div[1]')
            elm.click()
            # find element for party and click
            elm = driver.find_element(By.XPATH, '//*[@data-value="'+y.party+'" and @role="option"]')
            elm.click()

            # click submit and search
            elm = driver.find_element(By.XPATH, '//*[@id="dineAvailSearchButton"]')
            elm.click()

            try:
                # search by class name
                elm = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'availableTime')))
                elm = driver.find_elements(By.CLASS_NAME, 'availableTime')
                for e in elm:
                    print(e.text) # works
            except TimeoutException:
                print("waiting too long for element/no reservation")







if __name__ == "__main__":
    # stores list of restaurants
    restaurant_list = []

    # get restaurants
    # process in file
    infile = open("places.json", "r")

    data = json.load(infile)

    #parse data and convert to objects
    for x in data["places"]:
        name = x["name"]
        link = x["link"]
        # stores temp list of reservations
        reservation_list = []

        for y in x["reservations"]:
            time = y["time"]
            date = y["date"]
            party= y["party"]

            res = Reservation(time, date, party)

            reservation_list.append(res)

        restaurant_list.append(Restaurant(name, link, reservation_list ))

    #close file
    infile.close()

    #print(data)

    driver = webdriver.Chrome()

    get_availibility(restaurant_list, driver)



