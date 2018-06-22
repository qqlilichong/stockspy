
import time
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument(r'headless')
browser = webdriver.Chrome(chrome_options=options)

try:
	browser.get(r'https://www.jisilu.cn/data/lof/')
	time.sleep(5)
	tbody = browser.find_element_by_tag_name('tbody')
	for tr in tbody.find_elements_by_tag_name('tr'):
		td = tr.find_element_by_css_selector(r'[data-name=fund_nm_color]')
		if td:
			print(td.text)

finally:
	browser.close()
	browser.quit()
	exit(0)
