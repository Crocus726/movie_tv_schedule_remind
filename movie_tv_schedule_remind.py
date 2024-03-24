import requests
#from PIL import Image
from bs4 import BeautifulSoup
import time

movie_title = ["그녀와+그녀의+고양이", "별의+목소리", "구름의+저편,+약속의+장소", "초속+5센티미터", "별을+쫓는+아이", "언어의+정원", "너의+이름은.", "날씨의+아이", "스즈메의+문단속"] # 신카이 마코토 감독의 작품 제목을 배열에 넣음

# movie_title 배열에 있는 요소(영화 제목)들에 대하여 다음을 수행함
for n in range(0, len(movie_title)):
    url = "https://m.search.naver.com/search.naver?sm=mtp_sly.hst&where=m&query="+movie_title[n]+"+편성표" # 네이버 검색 결과 URL에 영화 제목을 삽입하여 url 변수에 저장함
    response = requests.get(url) # url 변수에 저장된 URL로 웹 접속을 시도하고 결과를 response 변수에 저장함
    soup = BeautifulSoup(response.text, "html.parser")
    
    tv_time_list = soup.find_all("div", class_="tvtime_list") # 검색 결과 페이지에서 클래스가 tvtime_list인 div 요소를 모두 찾아 tv_time_list 배열에 저장함
    
    # 검색 결과 페이지에 편성표 메뉴가 존재하면 다음을 수행함
    if tv_time_list:
        timetable = tv_time_list[0]
        info_list = timetable.find_all("div", class_="info_list")
        
        schedule_dates = len(info_list) # 편성된 일수
        schedule_counts = len(timetable.find_all("div", class_="info")) - len(timetable.find_all("span", class_="number", string="2부")) # 편성된 횟수
        print(movie_title[n].replace("+", " ")+"은(는) "+str(schedule_dates)+"일동안 "+str(schedule_counts)+"회 편성되어 있습니다.\n")
        
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
        
    print("\n", end="") # 줄바꿈 출력함
    time.sleep(3) # 다음 검색 전 딜레이 3초
