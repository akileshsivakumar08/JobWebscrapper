from selenium import webdriver
import time
import csv
import re

dict_term = [
    {
        'company_name': "MAN",
        'weblink': "https://job.man.eu/sap/bc/bsp/sap/zmg_hcmx_ui_ext/desktop.html#/SEARCH/RESULTS",
        'HTML_head_name': "//li[@class='listItem jobListItem']",
        'HTML_jobtitle_name': "title",
        'CSVname': "Jobs_MAN.csv"
    },
    {
        'company_name': "MAN",
        'weblink': "https://job.man.eu/sap/bc/bsp/sap/zmg_hcmx_ui_ext/desktop.html#/SEARCH/RESULTS",
        'HTML_head_name': "//li[@class='listItem jobListItem']",
        'HTML_jobtitle_name': "title",
        'CSVname': "Jobs_MAN.csv"
    }
]

filedata = []
title_section = []
listToStr = []
company = 1


def ReadFromCSV(CSV_name_loc):  # dict_term[company][CSVname]
    with open(CSV_name_loc, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        filedata = list(csv_reader)
    print(filedata[6][0])
    print(type(filedata[6]))
    for row in range(len(filedata)):
        if len(filedata[row]) > 1:
            filedata[row][:len(filedata[row])] = [
                ''.join(filedata[row][:len(filedata[row])])]
        print(filedata[row])

    flat_list = []
    for sublist in filedata:
        for item in sublist:
            flat_list.append(item)
    print(flat_list)
    return flat_list


def ReachWebsite():
    driver = webdriver.Chrome()
    time.sleep(30)
    driver.get(
        dict_term[company]["weblink"])
    time.sleep(30)
    childSection = driver.find_elements_by_xpath(
        dict_term[company]["HTML_head_name"])
    print(len(childSection))
    for i in range(len(childSection)):
        title_section.append(
            childSection[i].find_element_by_class_name(dict_term[company]["HTML_jobtitle_name"]))
    return title_section


def ExtractionAndFilter(IP_JobsList):
    numItems = len(IP_JobsList)
    print(numItems)
    for ele in range(numItems):
        if IP_JobsList[ele].text.count(',') == 0:
            listToStr.append(IP_JobsList[ele].text)
        if IP_JobsList[ele].text.count(',') > 0:
            print("comma exists..\n")
            extract = list(IP_JobsList[ele].text)
            print("trying to fix it...\n")
            for occ in range(len(extract)):
                if extract[occ] == ',':
                    extract[occ] = ''
            print("should be fixed by now...\n")
            listToStr.append(''.join(map(str, extract)))
            print(type(listToStr))
            print(type(IP_JobsList[ele].text))
    for loop in range(len(listToStr)):
        print(listToStr[loop])
    return listToStr


def compare_Web_And_CSV_List(IP_Web_List, IP_CSV_List):

    li_dif = [j for j in IP_Web_List if j not in IP_CSV_List]
    if not li_dif:
        li_dif = IP_CSV_List
    return li_dif


def Write2CSV(IP_Latest_jobs):
    with open(dict_term[company]['CSVname'], 'w') as spdsht:
        for i in range(len(IP_Latest_jobs)):
            spdsht.write(IP_Latest_jobs[i] + "\n")
    spdsht.close()


CSV_List = ReadFromCSV(dict_term[company]['CSVname'])
WebpageJobList = ReachWebsite()
OP_Joblist = ExtractionAndFilter(WebpageJobList)
Latest_jobs = compare_Web_And_CSV_List(OP_Joblist, CSV_List)
Write2CSV(Latest_jobs)
