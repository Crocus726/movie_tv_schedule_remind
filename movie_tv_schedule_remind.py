import requests
#from PIL import Image
from bs4 import BeautifulSoup
import time

movie_title = ["그녀와+그녀의+고양이", "별의+목소리", "구름의+저편,+약속의+장소", "초속+5센티미터", "별을+쫓는+아이", "언어의+정원", "너의+이름은.", "날씨의+아이", "스즈메의+문단속"]

for n in range(0, len(movie_title)):
    url = "https://m.search.naver.com/search.naver?sm=mtp_sly.hst&where=m&query="+movie_title[n]+"+편성표"
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    tv_time_list = soup.find_all("div", class_="tvtime_list")
    
    # 검색 결과에 편성표 메뉴가 존재하면
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
        
    else:
        print(movie_title[n].replace("+", " ")+"은(는) 현재 TV 편성되어 있지 않습니다.")
        
    print("\n", end="")
    time.sleep(3)
