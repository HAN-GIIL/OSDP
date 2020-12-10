import matplotlib
import requests
import re
import datetime
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import matplotlib.font_manager as fm


plt.rcParams["figure.figsize"] = (14,4)
# 보고자 하는 공기업의 공고리스트 페이지 링크주소 배열
CompanyList = ['http://www.alio.go.kr/popSusi.do?apbaId=C0124&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0305&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0005&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0220&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0082&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0105&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C1024&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0247&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0268&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0259&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0066&reportFormRootNo=B1020',
               'http://www.alio.go.kr/popSusi.do?apbaId=C0394&reportFormRootNo=B1020']

global listCount
global companyNameForShow

company = []
notice = []
recruitment_period = []
link_url = []
recruitment_amount = []
# (함수) 상세정보 링크 구하기
def linkToDetails():
    for href in soupForDetailLink.find_all(id=re.compile('^goSusiView')):
        wordCnt = 0
        wordStId = [] # 각 가변부위의 시작점 인덱스가 들어가게 될 배열 [0]: 가변 부위 1 [1] : 가변 부위 4 [2] : 가변 부위 2,3 [3] : 가변 부위 5
        url_1 = "http://www.alio.go.kr/popSusiViewB1020.do?disclosure_no="
        for i in range(len(href["onclick"])):
            if href["onclick"][i] == "'":
                wordCnt += 1
                if wordCnt == 3:
                    wordStId.append(i+1)
                if wordCnt == 5:
                    wordStId.append(i+1)
                if wordCnt == 7:
                    wordStId.append(i+1)
                if wordCnt == 13:
                    wordStId.append(i+1)
        # for i in range(len(wordStId)):
        #     print(wordStId[i])
        # url_1 += 가변부위1
        for i in range(wordStId[0], wordStId[0]+16):
            url_1 += href["onclick"][i]
        url_2 = "&report_form_no="
        # url_1 += url_2 + 가변부위2
        url_1 += url_2
        for i in range(wordStId[2], wordStId[2]+5):
            url_1 += href["onclick"][i]
        url_3 = "&nowcode="
        url_1 += url_3
        # url_1 += url_3 + 가변부위3
        for i in range(wordStId[2], wordStId[2]+5):
            url_1 += href["onclick"][i]
        url_4 = "&apbaid="
        url_1 += url_4
        # url_1 += url_4 + 가변부위4
        for i in range(wordStId[1], wordStId[1]+5):
            url_1 += href["onclick"][i]
        url_5 = "&table_name=TTB_RECRUIT&idx_name=IDX&idx="
        url_1 += url_5
        # url_1 += url_5 + 가변부위5
        for i in range(wordStId[3], wordStId[3]+6):
            url_1 += href["onclick"][i]
        url_6 = "&report_gbn=N&bid_type="
        url_1 += url_6
        # 링크 완성했으니 여기서 타고 들어가서 모집여부 판단
        resForDetail = requests.get(url_1) # 상세정보 페이지 res
        soupForDetailPage = BeautifulSoup(resForDetail.content, 'html.parser') # html 태그 정보 떠옴
        # 채용기간 가져오기 (문자열)
        recruitPeriod = soupForDetailPage.find_all('td', class_='c_blue f_center')[9].get_text()
        recruitAmount = soupForDetailPage.find_all('td', class_='c_blue f_center')[7].get_text()
        recruitAmountForShow = ""
        for j in range(len(recruitAmount)):
            if recruitAmount[j] == "명":
                recruitAmountForShow = int(recruitAmount[j-1])


        recruitPeriodStart_Year = recruitPeriod[0] + recruitPeriod[1] + recruitPeriod[2] + recruitPeriod[3]
        recruitPeriodStart_Month = recruitPeriod[5] + recruitPeriod[6]
        recruitPeriodStart_Day = recruitPeriod[8] + recruitPeriod[9]

        recruitPeriodStart = int(recruitPeriodStart_Year)*365 + int(recruitPeriodStart_Month)*31 + int(recruitPeriodStart_Day)

        recruitPeriodEnd_Year = recruitPeriod[13] + recruitPeriod[14] + recruitPeriod[15] + recruitPeriod[16]
        recruitPeriodEnd_Month = recruitPeriod[18] + recruitPeriod[19]
        recruitPeriodEnd_Day = recruitPeriod[21] + recruitPeriod[22]

        recruitPeriodEnd = int(recruitPeriodEnd_Year)*365 + int(recruitPeriodEnd_Month)*31 + int(recruitPeriodEnd_Day)


        # 현재 날짜 가져오기 (문자열)
        now = datetime.datetime.now()
        nowDate = int(now.strftime('%Y'))*365+int(now.strftime('%m'))*31+int(now.strftime('%d'))


        if nowDate <= recruitPeriodEnd and nowDate >= recruitPeriodStart:
            # 현재 모집중이면
            print()
            print(href.get_text()) # 공고 제목
            print("접수 기간 : ", end="")
            print(recruitPeriod) # 모집 기간
            print(url_1) # 상세 정보 링크
            global listCount
            listCount+=1
            # company.append(companyNameForShow)
            # notice.append(href.get_text())
            # recruitment_amount.append(recruitAmountForShow)
            # recruitment_period.append(recruitPeriod)
            # link_url.append(url_1)
        # else:
        #    print(href.get_text()) # 공고 제목
        #    print("모집 기간 : ", end = "")
        #    print(recruitPeriod)
        #    print("모집 기간이 지난 공고입니다.")
        company.append(companyNameForShow)
        notice.append(href.get_text())
        recruitment_amount.append(recruitAmountForShow)
        recruitment_period.append(recruitPeriod)
        link_url.append(url_1)


noticeNo = 1

# 각 공기업 하나씩 보면서 모집 중인 공고 정보 출력해주기
for i in range(len(CompanyList)):
    listCount = 0
    # 공기업 리스트 페이지 링크 주소 변수 resForListPage
    resForListPage = requests.get(CompanyList[i])

    soupForDetailLink = BeautifulSoup(resForListPage.content, 'html.parser')

    companyName = soupForDetailLink.find('title').get_text()
    global companyNameForShow
    companyNameForShow = ""
    for j in range(11, len(companyName)):
        if companyName[j] == " ":
            break;
        companyNameForShow += companyName[j]


    print(noticeNo, end="")
    print(". ", end="")
    print(companyNameForShow, end="")
    print()
    linkToDetails()  # 상세 정보 페이지 링크 구하기
    if listCount == 0:
        print()
        print("   [현재 진행중인 공고가 없습니다.]")
    print()
    noticeNo += 1
#
# print(company)
# print(notice)
# print(recruitment_period)
# print(link_url)

company_card = pd.DataFrame({'Company':company,
                             'Notice':notice,
                             'Recruitment amount': recruitment_amount,
                             'Recruitment period':recruitment_period,
                             'link url':link_url
                             })

print(company_card.groupby('Company').mean())
print(company_card)

x_values = company
y_values = recruitment_amount

plt.plot(x_values, y_values)
plt.show()
#
# student_card = pd.DataFrame({'ID':[20190103, 20190222, 20190531],
#                              'name':['Kim', 'Lee', 'Jeong'],
#                              'class':['H', 'W', 'S']})
# print(student_card)
