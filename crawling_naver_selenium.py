from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pyperclip
from bs4 import BeautifulSoup
import openpyxl
from selenium.webdriver.common.by import By

# 네이버 계정 아이디, 비밀번호
id = 'syjung64'
pw = '*****'

# # 완료해도 창 꺼지지 않게
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
# driver = webdriver.Chrome(options=chrome_options)

driver = webdriver.Chrome()
driver.implicitly_wait(3)

# 네이버 로그인 화면
driver.get('https://nid.naver.com/nidlogin.login')

# id 선택 후 붙여넣기 (mac이면 command, windows면 control)
id_input = driver.find_element('id', 'id')
id_input.click()
pyperclip.copy(id)
actions = webdriver.ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
time.sleep(1)

# pw 선택 후 붙여넣기
pw_input = driver.find_element('id', 'pw')
pw_input.click()
pyperclip.copy(pw)
actions = webdriver.ActionChains(driver)
actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).send_keys(Keys.ENTER).perform()
time.sleep(1)

# 로그인 버튼 클릭
#driver.find_element(By.ID, 'log.login').click()
print('title(naver) : ', driver.title)
#print('page(naver) : ', driver.page_source)

#
# 메일함으로 이동
driver.get('https://mail.naver.com/v2/folders/0')
time.sleep(2)  # 페이지 로딩 대기
print('title(mail) : ', driver.title)

# 이동 결과 확인
if "메일" in driver.title or "메일함" in driver.page_source:
    print("메일함 이동 성공")
else:
    print("메일함 이동 실패")

# 검색어 입력 후 검색
#driver.find_element('id', 'search').send_keys('광고')
#driver.find_element('xpath', '//*[@id="search-bar"]/div/button').click()
#time.sleep(1)

# 메일 목록 파싱 (id)
soupForMailList = BeautifulSoup(driver.page_source, 'html.parser')

mailIdList = []
# 검색 결과인 ul로 반복문
mails = soupForMailList.find('ul', {'class': 'mail_list'})

for mail in mails:
    # 제목 추출
    title_tag = mail.find('div', class_='mail_title')
    title = title_tag.get_text(strip=True) if title_tag else '제목 없음'

    # 발신자 추출
    sender_tag = mail.find('div', class_='mail_sender')
    if not sender_tag:
        sender_tag = mail.find('div', class_='mail_send')  # 혹시 다른 class명일 경우
    sender = sender_tag.get_text(strip=True) if sender_tag else '발신자 없음'

    print(f'{sender} / {title}')

time.sleep(3)