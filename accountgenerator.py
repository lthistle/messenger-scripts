from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random, string, time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

def delay(): time.sleep(random.random()/2)
def slowtype(message, element):
    for character in message:
        element.send_keys(character)
        delay()

#generate fake details
driver.get("https://www.fakenamegenerator.com/advanced.php?t=country&n%5B%5D=us&c%5B%5D=us&gen=100&age-min=19&age-max=85")
first_name, _, last_name = driver.find_element_by_tag_name('h3').text.split(' ')
email = first_name + last_name + ''.join([str(random.randint(0,9)) for x in range(5)]) + "@myoverlandtandberg.com"
alphabet = string.hexdigits + "!@#$%^&*()"
password = ''.join([alphabet[random.randint(0, len(alphabet) - 1)] for x in range(15)])

#facebook account creation
driver.get("https://www.facebook.com/")
delay()
slowtype(first_name, driver.find_element_by_xpath("//*[@id='u_0_e']"))
slowtype(last_name, driver.find_element_by_xpath("//*[@id='u_0_g']"))
slowtype(email, driver.find_element_by_xpath("//*[@id='u_0_j']"))
slowtype(email, driver.find_element_by_xpath("//*[@id='u_0_m']"))
slowtype(password, driver.find_element_by_xpath("//*[@id='u_0_q']"))
month, day, year = random.randint(2, 13), random.randint(2, 32), random.randint(31, 41)
driver.find_element_by_xpath("//*[@id='month']/option[" + str(month) + "]").click()
delay()
driver.find_element_by_xpath("//*[@id='day']/option[" + str(day) + "]").click()
delay()
driver.find_element_by_xpath("//*[@id='year']/option[" + str(year) + "]").click()
delay()
driver.find_element_by_xpath("//*[@id='u_0_9']").click()
delay()
driver.find_element_by_xpath("//*[@id='u_0_y']").click()

#go to sketchy email website to verify (they seem to snoop all links received, so there's no need to actually do anything)
time.sleep(10)
driver.get("https://generator.email/" + email)
time.sleep(5)
driver.quit()

print("Generated new Facebook account")
print("Email: " + email)
print("Password: " + password)
