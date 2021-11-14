###################################################################
#                  Author:  Ryan Montgomery                       #
#        Use wisely, or you'll go to prison                       #
#                                                                 #
###################################################################

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains as ac
from time import sleep
from sys import argv, exit
import signal, re

class spoofPhone:
    def __init__(self, numm, callnumm, userName, passWord):
        self.phoneNumber = numm
        self.callN = callnumm
        self.uN = userName
        self.pN = passWord
        signal.signal(signal.SIGINT, self.signal_handler)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('media.navigator.permission.disabled', True)
        profile.set_preference('dom.webnotifications.enabled', False)
        self.s = webdriver.Firefox(profile)
        self.s.set_window_position(0,0)
        self.s.set_window_size(800, 800)
        self.login()

    def login(self):
        self.s.get("https://phone.firertc.com")
        usern = self.s.find_element_by_id("user_email")
        passn = self.s.find_element_by_id("user_password")
        subb = self.s.find_element_by_xpath('//input[@value="Sign In"]')
        usern.send_keys(self.uN)
        passn.send_keys(self.pN)
        subb.click()
        self.spoofId()

    def spoofId(self):
        self.s.get("https://phone.firertc.com/settings")
        spoofAdd =  self.s.find_element_by_id("address-ua-config-display-name")
        subb = self.s.find_element_by_xpath('//button[@type="submit"]')
        spoofAdd.send_keys(Keys.CONTROL + 'a')
        spoofAdd.send_keys(Keys.BACKSPACE)
        spoofAdd.send_keys('1'+self.phoneNumber)
        subb.click()
        self.callNumber()

    def callNumber(self):
        self.s.get("https://phone.firertc.com/phone")
        sleep(1)
        phoneInput = self.s.find_element_by_xpath('//input[@class="dialer-input form-control dropdown-toggle"]')
        phoneInput.send_keys(self.callN)
        phoneInput.send_keys(Keys.ENTER)
        sleep(2)
        while True:
            sleep(.5)
            try:
                self.s.find_element_by_xpath('//button[@data-action="cancel"]')
            except:
                try:
                    self.s.find_element_by_xpath('//button[@data-action="hangup"]')
                except:
                    break

        self.die()

    def signal_handler(self, signal, frame):
            self.die()
            exit(0)

    def die(self):
        self.s.close()


def usage():
    print('Usage: phoneSpoofer.py <PhoneToSpoof> <PhoneToCall> <Username for FireRTC> <Password for FireRTC>')
    print('\n')

if __name__ == '__main__':
    temp = len(argv)
    #check phone
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    #check email
    e = re.compile(r'[^@]+@[^@]+\.[^@]+')
    if(temp < 5 or temp > 5 or r.match(argv[1]) == None or r.match(argv[2]) == None or e.match(argv[3]) == None):
        usage()
        exit(0)
    spoofPhone(str(argv[1]), str(argv[2]), str(argv[3]), str(argv[4]))
