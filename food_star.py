import json
import time
from time import sleep
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def search_food(key):
    
    food_list = []
    
    url = 'https://map.naver.com/v5/search'
    driver = webdriver.Chrome()  # 드라이버
    driver.get(url)
    key_word = key + ' 맛집'  # 검색어

    # css 찾을때 까지 10초대기
    def time_wait(num, code):
        try:
            wait = WebDriverWait(driver, num).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, code)))
        except:
            print(code, '태그를 찾지 못하였습니다.')
            driver.quit()
        return wait

    # frame 변경 메소드
    def switch_frame(frame):
        driver.switch_to.default_content()  # frame 초기화
        driver.switch_to.frame(frame)  # frame 변경

    # 페이지 다운
    def page_down(num):
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.click()
        for i in range(num):
            body.send_keys(Keys.PAGE_DOWN)

    # css를 찾을때 까지 10초 대기
    time_wait(10, 'div.input_box > input.input_search')

    # (1) 검색창 찾기
    search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
    search.send_keys(key_word)  # 검색어 입력
    search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

    sleep(1)

    # (2) frame 변경
    switch_frame('searchIframe')
    page_down(40)
    sleep(3)

    # 가게 리스트
    shop_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
    # 페이지 리스트
    next_btn = driver.find_elements(By.CSS_SELECTOR, '.zRM9F> a')

    # dictionary 생성
    shop_dict = {'가게정보': []}
    # 시작시간
    start = time.time()
    print('[크롤링 시작...]')

    # 크롤링 (페이지 리스트 만큼)
    for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
        parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.UEzoS')
        names = driver.find_elements(By.CSS_SELECTOR, '.TYaxT')  # (3) 장소명
        types = driver.find_elements(By.CSS_SELECTOR, '.KCMnt')  # (4) 장소 유형
        star = driver.find_elements(By.CSS_SELECTOR, '.h69bs.orXYY') #별점 박스
        #real_star = driver.find_elements(By.XPATH, 'h69bs')
        #star = driver.find_element(By.CSS_SELECTOR, "_pcmap_list_scroll_container > ul > li:nth-child(2) > div.CHC5F > div > div > span.h69bs.orXYY")
        #/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/div[1]/div/div
        #print(driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[3]/div[1]/div[2]/div/span[2]/text()'))
        #_pcmap_list_scroll_container > ul > li:nth-child(2) > div.CHC5F > div > div > span.h69bs.orXYY

        for data in range(len(shop_list)):  # 가게 리스트 만큼
            print(data)
            

            sleep(1)
            try:

                # (3) 가게명 가져오기
                shop_name = str(names[data].text)
                print(shop_name)

                # (4) 유형
                shop_type = str(types[data].text)
                print(shop_type)
                
                #(5) 별점
                real_star = star[data].text
                real_star = str(real_star).split("\n")[1]
                print(real_star)
                
                tmp = [shop_name, real_star]
                food_list.append(tmp)
                
                print(f'{shop_name} ...완료')

                sleep(1)

            except Exception as e:
                print(e)
                print('ERROR!' * 3)

                sleep(1)

        # 다음 페이지 버튼 누를 수 없으면 종료
        if not next_btn[-1].is_enabled():
            break

        if names[-1]:  # 마지막이면 다음버튼 클릭
            next_btn[-1].click()

            sleep(2)

        else:
            print('페이지 인식 못함')
            break

    print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
    driver.quit()  # 작업이 끝나면 창을 닫는다.

    index_final = len(food_list) // 2
    food_list = food_list[0:index_final]
    
    return food_list

##############################################################################

regions = ["종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구", "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구", "양천구", 
           "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구", "서초구", "강남구", "송파구", "강동구", "서구", "동구", "영도구", "부산진구", "동래구", 
           "남구", "북구", "해운대구", "사하구", "금정구", "연제구", "수영구", "사상구", "기장군", "수성구", "달서구", "달성군", "군위군", "연수구", "남동구", 
           "부평구", "계양구", "미추홀구", "강화군", "옹진군", "광산구", "유성구", "대덕구", "울주군", "세종시", "수원시 장안구", "수원시 권선구", "수원시 팔달구", 
           "수원시 영통구", "성남시 수정구", "성남시 중원구", "성남시 분당구", "의정부시", "안양시 만안구", "안양시 동안구", "부천시", "광명시", "평택시", "동두천시", 
           "안산시 상록구", "안산시 단원구", "고양시 덕양구", "고양시 일산동구", "고양시 일산서구", "과천시", "구리시", "남양주시", "오산시", "시흥시", "군포시", "의왕시", 
           "하남시", "용인시 처인구", "용인시 기흥구", "용인시 수지구", "파주시", "이천시", "안성시", "김포시", "화성시", "광주시", "양주시", "포천시", "여주시", "연천군", 
           "가평군", "양평군", "춘천시", "원주시", "강릉시", "동해시", "태백시", "속초시", "삼척시", "홍천군", "횡성군", "영월군", "평창군", "정선군", "철원군", "화천군", 
           "양구군", "인제군", "고성군", "양양군", "충주시", "제천시", "청주시 상당구", "청주시 서원구", "청주시 흥덕구", "청주시 청원구", "보은군", "옥천군", "영동군", "진천군", 
           "괴산군", "음성군", "단양군", "증평군", "천안시 동남구", "천안시 서북구", "공주시", "보령시", "아산시", "서산시", "논산시", "계룡시", "당진시", "금산군", "부여군", "서천군", 
           "청양군", "홍성군", "예산군", "태안군", "전주시 완산구", "전주시 덕진구", "군산시", "익산시", "정읍시", "남원시", "김제시", "완주군", "진안군", "무주군", "장수군", "임실군", 
           "순창군", "고창군", "부안군", "목포시", "여수시", "순천시", "나주시", "광양시", "담양군", "곡성군", "구례군", "고흥군", "보성군", "화순군", "장흥군", "강진군", "해남군", "영암군", 
           "무안군", "함평군", "영광군", "장성군", "완도군", "진도군", "신안군", "포항시 남구", "포항시 북구", "경주시", "김천시", "안동시", "구미시", "영주시", "영천시", "상주시", "문경시", 
           "경산시", "의성군", "청송군", "영양군", "영덕군", "청도군", "고령군", "성주군", "칠곡군", "예천군", "봉화군", "울진군", "울릉군", "진주시", "통영시", "사천시", "김해시", "밀양시", 
           "거제시", "양산시", "창원시 의창구", "창원시 성산구", "창원시 마산합포구", "창원시 마산회원구", "창원시 진해구", "의령군", "함안군", "창녕군", "남해군", "하동군", "산청군", "함양군", 
           "거창군", "합천군", "제주시", "서귀포시"]


for i in range(116, len(regions)):
    filename = "./out_food/out_" + str(i) + "_food.csv"
    f = open(filename, 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerows(search_food(regions[i]))
    f.close()
