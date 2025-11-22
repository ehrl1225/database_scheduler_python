from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import  FirefoxBinary
import time

# 폐기
# 크롬 드라이버는 죽었고 파이어폭스로도 수원대 포털을 뚫지 못함

binary = FirefoxBinary()
driver = webdriver.Firefox(firefox_binary=binary)
driver.get("https://www.naver.com/")
time.sleep(3)
print(driver.page_source)
#driver.find_element(By.NAME, "userId").send_keys(ID)
#driver.find_element(By.NAME, "pwd").send_keys(PW)
#driver.find_element(By.CLASS_NAME, "mainbtn_login").click()
