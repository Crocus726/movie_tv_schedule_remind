import requests
from bs4 import BeautifulSoup
import time

# 안내 문구 출력
print("검색할 영화 제목을 입력해주세요")
print("예시: 언어의 정원, 날씨의 아이 (여러 개일 경우 쉼표로 구분)")

user_input = input("영화 제목 입력: ") # 사용자로부터 영화 제목 입력 받음

# 입력받은 영화 제목 파싱 (쉼표로 구분, 공백 제거)
movie_title = [title.strip() for title in user_input.split(',')]
print("-" * 50)

# 크롤링 차단 방지를 위한 유저 에이전트 헤더 추가
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# movie_title 배열에 있는 요소(영화 제목)들에 대하여 다음을 수행함
for n in range(0, len(movie_title)):
    search_keyword = movie_title[n].replace(" ", "+") # 영화 제목의 공백을 '+'로 대체하여 serch_keyword 변수에 저장
    url = "https://m.search.naver.com/search.naver?sm=mtp_sly.hst&where=m&query=" + search_keyword + "+편성표" # 네이버 검색 결과 URL에 영화 제목을 삽입하여 url 변수에 저장함
    
    response = requests.get(url, headers=headers) # url 변수에 저장된 URL로 웹 접속을 시도하고 결과를 response 변수에 저장함
    soup = BeautifulSoup(response.text, "html.parser")
    
    tv_time_list = soup.find_all("div", class_="tvtime_list") # 검색 결과 페이지에서 클래스가 tvtime_list인 div 요소를 모두 찾아 tv_time_list 배열에 저장함
    
    # 검색 결과 페이지에 편성표 메뉴가 존재하면 다음을 수행함
    if tv_time_list:
        timetable = tv_time_list[0]
        info_list = timetable.find_all("div", class_="info_list")
        
        schedule_dates = len(info_list) # 편성된 일수
        schedule_counts = len(timetable.find_all("div", class_="info")) - len(timetable.find_all("span", class_="number", string="2부")) # 편성된 횟수
        print(movie_title[n].replace("+", " ")+"은(는) "+str(schedule_dates)+"일동안 "+str(schedule_counts)+"회 편성되어 있습니다.")
        
        for i in range(0, len(info_list)):
            broadcast_date = info_list[i].find("strong", class_="cm_date").get_text()
            print(broadcast_date+" 편성 일정은 다음과 같습니다.")
            
            broadcast_schedule = info_list[i].find_all("div", class_="info")
            for j in range(0, len(broadcast_schedule)):
                print(broadcast_schedule[j].find("span", class_="time").get_text(), end="\t")
                print(broadcast_schedule[j].find("a", class_="channel").get_text(), end="\t")
                if broadcast_schedule[j].find("span", class_="number"):
                    print(broadcast_schedule[j].find("span", class_="number").get_text(), end="")
                print("\n", end="")
        
    # 검색 결과 페이지에 편성표 메뉴가 존재하지 않으면 다음을 수행함
    else:
        print(movie_title[n].replace("+", " ")+"은(는) 현재 TV 편성되어 있지 않습니다.")
        
    #print("\n", end="") # 줄바꿈 출력함
    time.sleep(3) # 다음 검색 전 딜레이 3초
