import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys                     #send_key에 필요
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait             #웹드라이버 딜레이
from selenium.webdriver.support import expected_conditions as EC    #예외처리
from selenium.common.exceptions import TimeoutException             

def Shutdown(_time):
    os.system("shutdown -s -t " + str(_time))

def WaitForClass_CanBeClicked(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))

def WaitForClass_Visible(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))
    
def WaitForID_Visible(driver, delaySec, id_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.ID, id_name)))

def WaitForTag_Visible(driver, delaySec, tag_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))


def Login(self, driver, id, password):
    self.signal_AddLogMessage.emit("유세인트에 로그인합니다..")
    # try:
    driver.get('https://saint.ssu.ac.kr/irj/portal')
    WaitForClass_CanBeClicked(driver, 10, "btn_login")
    driver.find_element_by_class_name('btn_login').click()


    WaitForClass_Visible(driver,10,"tit")
    #ID, PW 필드 채우기
    driver.find_element_by_xpath('//*[@id="userid"]').send_keys(id)
    driver.find_element_by_xpath('//*[@id="pwd"]').send_keys(password)

    #로그인 버튼 클릭
    driver.find_element_by_xpath('//*[@id="sLogin"]/div/div[1]/form/div/div[2]/a').click()

    #로그인 실패 시 Alert 예외처리
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present(),
                                    'Timed out waiting for PA creation ' +
                                    'confirmation popup to appear.')
        alert = driver.switch_to.alert
        alert.accept()
        raise ValueError("로그인 ID, PW를 다시 확인해주세요!")
    except TimeoutException:
        return;

def CheckGrade(self, driver):
    # ===메뉴 이동===
    WaitForID_Visible(driver, 10, 's_gnbUL')
    driver.find_element_by_xpath('//*[@id="ddba4fb5fbc996006194d3c0c0aea5c4"]/a').click()
    driver.find_element_by_xpath('//*[@id="8d3da4feb86b681d72f267880ae8cef5"]/a').click()
    
    # ===팝업창 닫기===
    WaitForClass_Visible(driver, 10, 'lsBlockLayer')
    element = driver.find_element_by_class_name('lsBlockLayer')
    driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)
    element = driver.find_element_by_id('URLSPW-0')
    driver.execute_script("var element = arguments[0]; element.parentNode.removeChild(element);", element)

    # ===성적 테이블 텍스트 가져오기===
    iframes = driver.find_elements_by_tag_name('iframe')
    # iframe 내부에 iframe이 있어서, 두 번 프레임을 바꿔줌
    driver.switch_to.default_content()
    driver.switch_to.frame('contentAreaFrame')
    driver.switch_to.frame('isolatedWorkArea')
    # print(driver.page_source)

    WaitForClass_Visible(driver, 10, 'urSTSStd')
    gradeTexts = driver.find_elements_by_class_name('urSTSStd')     # gradeTexts[0]은 석차정보, [1]은 현재학기 성적ㄴ
    print(gradeTexts[1].text)
    gradeText = gradeTexts[1].text
    characters = ["이수학년도", "이수학기", "과목코드", "과목명", "과목학점", "성적", "등급", "교수명", "비고", "상세"]
    for ch in characters:
        gradeText = gradeText.replace(ch, "")
    gradeText = gradeText.replace("\n조회", " ★")
    gradeText = gradeText.replace("  ", "")
    gradeText = gradeText.strip()
    print(gradeText)
    self.signal_AddLogMessage.emit(gradeText)

    count = gradeText.count("★") # 등록된 성적 개수

    # gradeSum = 0
    # gradeSum += gradeText.count("A+") * 4.5
    # gradeSum += gradeText.count("A0") * 4.3
    # gradeSum += gradeText.count("A-") * 4.2
    # gradeSum += gradeText.count("B+") * 4.0
    # gradeSum += gradeText.count("B0") * 3.5
    # gradeSum += gradeText.count("B-") * 3.3
    # gradeSum += gradeText.count("C+") * 3.0
    # gradeSum += gradeText.count("C0") * 2.5
    # gradeSum += gradeText.count("C-") * 2.3
    # gradeSum += gradeText.count("D+") * 2.0
    # gradeSum += gradeText.count("D0") * 1.5
    # gradeSum += gradeText.count("D-") * 1.3
    # gradeSum += gradeText.count("D-") * 1.0

    # if count > 0:
    #     self.signal_AddLogMessage.emit(f"현재 학점 평균은 {gradeSum / count} 입니다.")
    # else:
    #     self.signal_AddLogMessage.emit("현재 등록된 성적이 없습니다.")

def mainFunc(self):
    # =====드라이버 및 옵션 생성=====
    options = webdriver.ChromeOptions()

    # 필요없고 해결방법도 없는 에러로그들 제거 옵션 추가
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #Alert 팝업 없애는 옵션 추가 (로그인 실패 대응)
    options.add_argument("--disable-popup-blocking")

    # # 창 숨기는 옵션 추가
    options.add_argument("headless")

    # 드라이버 로드
    try:
        driver = webdriver.Chrome('.\CoreFiles\chromedriver\chromedriver.exe', options=options)
        driver.set_window_size(1920, 1080)
    except:
        self.signal_AddLogMessage.emit("! 크롬 드라이버 로드 실패. 크롬 버전과 호환되는 크롬드라이버가 설치되어 있는지, chromedriver.exe가 폴더 내에 있는지 확인해주세요.")
        return;

    # =====로그인=====
    try:
        Login(self, driver, self.id, self.pw)
    except:
        self.signal_AddLogMessage.emit("! 로그인에 실패하였습니다")
        driver.quit()
        return

    try:
        CheckGrade(self, driver)
    except Exception as e:
        self.signal_AddLogMessage.emit(f"! 성적 확인 도중 문제가 발생했습니다. {e}")
        driver.quit()
        return
    driver.quit()




# class Temp():
#     def __init__(self):
#         self.isRun = False
#         self.id = ""
#         self.pw = ""

#     def run(self):
#         mainFunc(self)

# tmp = Temp()
# tmp.run()

