import requests
#from PIL import Image
from bs4 import BeautifulSoup

url = "https://m.search.naver.com/search.naver?sm=mtp_sly.hst&where=m&query=날씨의+아이+편성표"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

tv_time_list = soup.find_all("div", class_="tvtime_list")

# 검색 결과에 편성표 메뉴가 존재하면
if tv_time_list:
    timetable = tv_time_list[0]
    info_list = timetable.find_all("div", class_="info_list")
    
    schedule_dates = len(info_list) # 편성된 일수
    schedule_counts = len(timetable.find_all("div", class_="info")) - len(timetable.find_all("span", class_="number", string="2부")) # 편성된 횟수
    print(str(schedule_dates)+"일동안 "+str(schedule_counts)+"회 편성되어 있습니다.\n")
    
    for i in range(0, len(info_list)):
        broadcast_date = info_list[i].find("strong", class_="cm_date").get_text()
        print(broadcast_date+" 편성 일정은 다음과 같습니다.")
        
        broadcast_schedule = info_list[i].find_all("div", class_="info")
        for j in range(0, len(broadcast_schedule)):
            print(broadcast_schedule[j].find("span", class_="time").get_text(), end="\t")
            print(broadcast_schedule[j].find("a", class_="channel").get_text(), end="\t")
            if broadcast_schedule[j].find("span", class_="number"):
                print(broadcast_schedule[j].find("span", class_="number").get_text())
        print("\n", end="")
    
else:
    print("현재 TV 편성되어 있지 않은 영화이거나 영화 이름을 잘못 입력하셨습니다.")
