# python 3.5

from twilio.rest import Client


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import os
import threading
import time as TIME

# These varibles will be used for Texting services
TIMEOUT = 10
account_sid  = None
auth_token = None
twilio_number = None
to_number = None


# a dictionary to convert numeric date into phonetic form
date_day = {"01": "January", "02": "February", "03": "March", "04": "April", "05": "May",
            "06": "June", "07": "July", "08": "August", "09": "September", "10": "October",
            "11": "November", "12": "December"}


class Alert:
    """An Object Representation of a Text Alert
    
    This class is used to store the information that will be texted to the user. An Alert represents available 
    reservations for a restaurant. 
    
    Attributes:
        restaurant_name (str): Name of the restaurant the user is looking to make a reservation at
        date (str): A string of when the reservation is available. 
        times (:obj: `list`): List of available times that were found via webscraping. Default value is an empty list
    
    """
    def __init__(self, restaurant_name, date, times = []):
        self.restaurant_name = restaurant_name
        self.times = times
        self.date = date


class Reservation:
    """An object representation of all the information needed to search for a reservation in disney's website
    
    A reservation at disney requires a time, a party size and a date. The website returns possible reservation for a 
    specific date and time range if a reservation of the time the user chooses isn't currently available.
     
     Attributes:
         time (str): The time a user wants to eat in the specific format : HH:MM pm/am. Capitalization matters.
         date (date): The date a user wants to make a reservation for. format: DD:MM:YY
         party (str): The amount of people who will be eating at for the reservation
    
    
    """
    def __init__(self, time, date, party):
        self.time = time
        self.party = party
        self.date = date


class Restaurant:
    """Information and details about the Restaurant a user wants to make a reservation at
     
     A Restaurant at disney as a distinct website that we can use to search for reservations. This object will have a 
     list of possible reservations a user would like to make for one specific restaurant.
     
     Attributes:
         name (str): The Name of the restaurant
         reservations (:obj: `list` of :obj: `Reservation`): A list of reservation that the user is looking for
         link (str): link to the websites specific website
    
    
    """
    def __init__(self, name, link,  reservations = []):
        self.name = name
        self.reservations = reservations
        self.link = link



def get_settings():
    """Sets up the variables that Twilio Api needs to send a text message
    """

    # check for the account.json file if not found we cannot continue the program
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
        # if there is any missind data we need to throw an exception and end the program
        Exception("Missing Arguments in 'account.json,' please include account_sid, auth_token, and twilio_number")



def get_availability(r_list, driver):
    """A function for returning a list of Alerts of Restaurants availability

    get_availability searches the pages of websites's using Disney's own search feature
    and returns a list of Alert's that will be sent back to the user via Text Messaging.

    Args:
        r_list (list): A list of Restaurant Params
        driver (webdriver): A Selenium Webdriver Instance
    Returns:
        list: A list of Alert objects, if there are failures or no possible reservations this will return an empty list

    """
    results = []
    # get restaurant
    for restaurant in r_list:
        # get reservation
        for reservation in restaurant.reservations:

            driver.get(restaurant.link)
            # get day and date as numbers
            arr = reservation.date.split('/')
            # turn numeric date to text
            month = date_day[arr[0]]
            day = arr[1]

            # problems consistently loading, sleeping to let the page load
            TIME.sleep(1) # full sleep because the python program is going faster than the website can handle
            try:
                element = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(
                    (By.XPATH,'//*[@id="diningAvailabilityForm-searchDateid-base"]/div/button')))
            except:
                print("couldn't load page")
                continue


            # open the calender
            elm = driver.find_element(By.XPATH, '//*[@id="diningAvailabilityForm-searchDateid-base"]/div/button')
            elm.click()
            # get the month at the top of the calender
            elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')
            # until we have the correct month we click the next month
            counter = 0
            while(elm.text.lower() != month.lower()):

                # reservations can't be made more than 6 months in advanced
                # the program is getting stuck and sometimes missing the proper month
                if counter > 6:
                    break
                try:
                    elm = WebDriverWait(driver, TIMEOUT).until(
                        EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-datepicker-div"]/div/a[2]')))
                except TimeoutException:
                    print("Couldn't click next on calender")
                    continue
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/a[2]')
                elm.click()
                elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/div/div/span[1]')
                counter += 1

            # if we have searched too far there is an error and we exit.
            if counter > 6:
                break
            # after we find the month we need to find the proper date
            # elements = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody')
            # find the element of the specific date
            TIME.sleep(1) # full sleep because the python program is going faster than the website can handle
            elm = driver.find_element(By.XPATH, '//*[@id="ui-datepicker-div"]/table/tbody/tr//a[text()=' +day +']'  )
            # click the element
            elm.click()
            # click the dropdown list:
            elm = driver.find_element(By.XPATH, '//*[@id="searchTime-wrapper"]/div[1]')
            elm.click()
            # multiple ways to find the time in the DOM, the format for time has to be 'x:xx pm'/'x:xx am'

            try:
                TIME.sleep(1)
                elm = WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located((By.XPATH, '//*[@data-display="' +reservation.time+'"]')))
                elm.click()
            except TimeoutException:
                print("Can't find reservation time")
            # click on dropdown for party size
            elm = driver.find_element(By.XPATH, '//*[@id="partySize-wrapper"]/div[1]')
            elm.click()
            # find element for party and click
            try:
                TIME.sleep(1) # full sleep because the python program is going faster than the website can handle
                elm = WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable((By.XPATH, '//*[@data-value="'+reservation.party+'" and @role="option"]')))
                elm.click()
            except TimeoutException:
                print("can't select party size")

            # click submit and search
            elm = driver.find_element(By.XPATH, '//*[@id="dineAvailSearchButton"]')
            elm.click()

            try:
                # search by class name
                driver.implicitly_wait(2)# needed to call sleep here, some issues on windows version on chrome
                elm = WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, 'availableTime')))
                elm = driver.find_elements(By.CLASS_NAME, 'availableTime')

                times = []
                for e in elm:
                    times.append(e.text)

                alert = Alert(restaurant.name, reservation.date, times)
                results.append(alert)
            except TimeoutException:
                print("waiting too long for element/no reservation")

    return results

def send_text(body, number):
    """A wrapper function to send texts to one user
    
    send_text sends a message to a single user
    Args:
        body (str): The message to send
        number (str): Phone number to send to
    Returns:
        None
        
    """
    client = Client(account_sid, auth_token)
    message = client.api.account.messages.create(to=number,
                                                 from_=twilio_number,
                                                 body=body)

def send_alerts(alert_list):
    """A function for sending text alerts of Restaurants availability

    send_alert sends a text message via the information given in the account.json file.

    Args:
        alert_list (list): A list of Alerts to send out
        driver (webdriver): A Selenium Webdriver Instance
    Returns:
        None

    """

    # no alerts to be sent
    if alert_list is []:
        return

    header="\nThere is a reservation open for:\n"

    for alert in alert_list:
        body = ""
        body += header
        body += alert.restaurant_name +" \n"
        body += "at: "

        for time in alert.times:
            body += " " + time
        body += "\n on Date:"
        body += alert.date
        send_text(body, to_number)



def main():
    # threading to make sure the fuction is running every 5 minutes
    threading.Timer(60.0 * 5, main).start()
    restaurant_list = []

    # get restaurants
    # process in file
    infile = open("places.json", "r")

    data = json.load(infile)

    # parse data and convert to objects
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

    # close file
    infile.close()

    driver = webdriver.Chrome()

    try:
        alerts = get_availability(restaurant_list, driver)
        send_alerts(alerts)
    finally:
        driver.close() # close the window


if __name__ == "__main__":
    get_settings()  # set global variables for texting service
    main()




