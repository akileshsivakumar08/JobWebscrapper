from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv
from threading import Timer
import pandas as pd
import winsound

dict_term = [
    {
        'company_name': "MAN",
        'weblink': "https://job.man.eu/sap/bc/bsp/sap/zmg_hcmx_ui_ext/desktop.html#/SEARCH/RESULTS",
        'HTML_head_name': "//li[@class='listItem jobListItem']",
        'HTML_jobtitle_name': 'title',
        'CSVname': "Jobs_MAN.csv",
        'new_jobs_flag': "NO"
    },
    {
        'company_name': "Bosch",
        'weblink': "https://www.bosch.de/karriere/jobs/?experienceLevels=f524b939_fe55_407b_a0b0_e8f4eec28997-f3b92bc1_600d_4d33_9115_5aa27785f52b-e4a3c0db_920d_4356_8ce0_c0b44a54e497-8c682ec0_3d28_4e52_b53b_c63d440a32d3&functions=research-science-engineering",
        'HTML_head_name': "//div[@class='M-JobSearchResultsGroup__item']",
        'HTML_jobtitle_name': 'sr-only',
        'CSVname': "Jobs_Bosch.csv",
        'cookie_path': "//button[@class='BoschPrivacySettingsV2__close']",
        'new_jobs_flag': "NO"
    },
    # {
    #     'company_name': "Schäffler",
    #     'weblink': "https://www.schaeffler.de/content.schaeffler.de/de/karriere/stellensuche/jobs/job_overview/index.jsp?filter=location:39%2C53&page=1",
    #     'HTML_head_name': "//li[@class='resultlist-result']",
    #     'HTML_jobtitle_name': "h3",
    #     'CSVname': "Jobs_Schäffler.csv",
    #     # 'cookie_path': "//button[@class='BoschPrivacySettingsV2__close']"
    #     'new_jobs_flag': "NO"
    # },
    # {
    #     'company_name': "Continental",
    #     'weblink': "https://www.continental-jobs.com/index.php?ac=search_result&search_criterion_activity_level%5B%5D=3&search_criterion_activity_level%5B%5D=23&search_criterion_entry_level%5B%5D=6&search_criterion_entry_level%5B%5D=4&search_criterion_entry_level%5B%5D=5&search_criterion_country%5B%5D=17&search_criterion_language%5B%5D=DE&search_criterion_channel%5B%5D=12&language=1",
    #     'HTML_head_name': "//tr",
    #     'HTML_jobtitle_name': "hidden-xs",
    #     'CSVname': "Jobs_Continental.csv",
    #     # 'cookie_path': "//button[@class='BoschPrivacySettingsV2__close']"
    #     'new_jobs_flag': "NO"
    # },
    # {
    #     'company_name': "IAV",
    #     'weblink': "https://www.iav.com/en/apply?fwp_occupational_groups=engineering-sciences&fwp_levels=students",
    #     'HTML_head_name': "//div[@class='iav-search-list-item uk-width-1-1']",
    #     'HTML_jobtitle_name': "iav-search-result-headline",
    #     'CSVname': "Jobs_IAV.csv",
    #     # 'cookie_path': "//button[@class='BoschPrivacySettingsV2__close']"
    #     'new_jobs_flag': "NO"
    # },
    # {
    #     'company_name': "Porsche",
    #     'weblink': "https://jobs.porsche.com/index.php?ac=search_result&search_criterion_keyword%5B%5D=elektrotechnik&search_criterion_country%5B%5D=46",
    #     'HTML_head_name': "//tr",
    #     'HTML_jobtitle_name': "job",
    #     'CSVname': "Jobs_Porsche.csv",
    #     # 'cookie_path': "//button[@class='BoschPrivacySettingsV2__close']"
    #     'new_jobs_flag': "NO"
    # },
]

filedata = []
title_section = []
listToStr = []
# company = 5
new_jobs_flag = []
OP_Count_of_jobs = [0 for x in range(len(dict_term))]


def ReadFromCSV(CSV_name_loc):  # dict_term[company][CSVname]
    with open(CSV_name_loc, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        filedata = list(csv_reader)
    for row in range(len(filedata)):
        if len(filedata[row]) > 1:
            filedata[row][:len(filedata[row])] = [
                ''.join(filedata[row][:len(filedata[row])])]

    flat_list = []
    for sublist in filedata:
        for item in sublist:
            flat_list.append(item)
    return flat_list


def ReachWebsite(IP_company):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "excludeSwitches", ['enable-automation'])
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(30)
    driver.get(
        dict_term[IP_company]["weblink"])
    time.sleep(30)

    if IP_company == 1:
        print("cookie")
        driver.find_element_by_xpath(
            dict_term[IP_company]["cookie_path"]).click()
        print("cookie clicked")
        time.sleep(10)

    childSection = driver.find_elements_by_xpath(
        dict_term[IP_company]["HTML_head_name"])
    for i in range(len(childSection)):
        title_section.append(
            childSection[i].find_element_by_class_name(dict_term[IP_company]["HTML_jobtitle_name"]))
    return title_section


def ExtractionAndFilter(IP_JobsList):
    for ele in range(len(IP_JobsList)):
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
    return listToStr


def compare_Web_And_CSV_List(IP_Web_List, IP_CSV_List, IP_company,):
    diff = []
    j = 0
    count = 0
    print("weblist:", IP_Web_List)
    print("CSVlist:", IP_CSV_List)
    for i in range(len(IP_Web_List)):
        if(len(IP_CSV_List) != 0):
            if(IP_Web_List[i] == IP_CSV_List[j]):
                j = j+1
                count = count+1
            else:
                dict_term[IP_company]['new_jobs_flag'] = "YES"
                OP_Count_of_jobs[IP_company] = OP_Count_of_jobs[IP_company]+1
                winsound.PlaySound("pikachu", winsound.SND_FILENAME)
                print("process happening")
                diff.append(IP_Web_List[i])
                continue
            if (((count == len(IP_CSV_List)) or (count == 3)) and (i == j)):
                dict_term[IP_company]['new_jobs_flag'] = "NO"
                break
        else:
            OP_Count_of_jobs[IP_company] = len(IP_Web_List)
            print("bypassing")
    if len(diff) == len(IP_Web_List):
        dict_term[IP_company]['new_jobs_flag'] = "More than one page of jobs"
        print(OP_Count_of_jobs[IP_company])
    return OP_Count_of_jobs[IP_company]


def Write2CSV(IP_Latest_jobs, IP_company):
    with open(dict_term[IP_company]['CSVname'], 'w') as spdsht:
        for i in range(len(IP_Latest_jobs)):
            spdsht.write(IP_Latest_jobs[i] + "\n")


def funcRunner():

    for company in range(len(dict_term)):
        CSV_List = ReadFromCSV(dict_term[company]['CSVname'])
        WebpageJobList = ReachWebsite(company)
        OP_Joblist = ExtractionAndFilter(WebpageJobList)
        compare_Web_And_CSV_List(
            OP_Joblist, CSV_List, company)
        Write2CSV(OP_Joblist, company)
        CSV_List.clear()
        WebpageJobList.clear()
        OP_Joblist.clear()
        # Latest_jobs.clear()
        print(OP_Count_of_jobs)
    for i in range(len(OP_Count_of_jobs)):
        if i == 0:
            print("writing")
            with open('JOB_Info.csv', 'w') as data_spdsht:
                data_spdsht.write(
                    str(OP_Count_of_jobs[i])+',' + (dict_term[company]['company_name'])+'\n')
        else:
            print("appending")
            with open('JOB_Info.csv', 'a') as data_spdsht:
                data_spdsht.write(
                    str(OP_Count_of_jobs[i])+',' + (dict_term[company]['company_name'])+'\n')

    # Timer(200, funcRunner).start()


funcRunner()
