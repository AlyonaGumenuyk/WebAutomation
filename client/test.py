from selenium import webdriver

from client.my_driver import MyDriver

#my_driver = webdriver.Firefox(executable_path='drivers/firefoxdriver/geckodriver.exe', service_log_path='logs/geckodriver.log')

my_driver = MyDriver(executable_path='drivers/firefoxdriver/geckodriver.exe',
                     service_log_path='logs/geckodriver_service.log',
                     log_path='logs/geckodriver.log')

my_driver.get('https://stackoverflow.com/')
logo = my_driver.find_element_by_css_selector('[class="-img _glyph"]')
print(logo.text)
