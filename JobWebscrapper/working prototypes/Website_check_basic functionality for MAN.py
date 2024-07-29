from selenium import webdriver
import time
import csv
import re
# details_list[1]=['MAN',"https://job.man.eu/sap/bc/bsp/sap/zmg_hcmx_ui_ext/desktop.html#/SEARCH/RESULTS"]
filedata = []
title_section = []
listToStr = []
with open('Jobs.csv', 'r') as csv_file:
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


driver = webdriver.Chrome()
time.sleep(30)
driver.get(
    "https://job.man.eu/sap/bc/bsp/sap/zmg_hcmx_ui_ext/desktop.html#/SEARCH/RESULTS")
time.sleep(30)
childSection = driver.find_elements_by_xpath(
    "//li[@class='listItem jobListItem']")
print(len(childSection))
for i in range(len(childSection)):
    title_section.append(childSection[i].find_element_by_class_name("title"))
numItems = len(title_section)
print(numItems)
for ele in range(numItems):
    if title_section[ele].text.count(',') == 0:
        # print(len(listToStr))
        listToStr.append(title_section[ele].text)
    if title_section[ele].text.count(',') > 0:
        print("comma exists..\n")
        extract = list(title_section[ele].text)
        print("trying to fix it...\n")
        for occ in range(len(extract)):
            if extract[occ] == ',':
                extract[occ] = ''
        print("should be fixed by now...\n")
        listToStr.append(''.join(map(str, extract)))
        print(type(listToStr))
        print(type(title_section[ele].text))

for loop in range(len(listToStr)):
    print(listToStr[loop])

print("\n the latest job must be:")

li_dif = [j for j in listToStr if j not in flat_list]
print(li_dif)

# with open('Jobs.csv', 'w') as spdsht:
#     for i in range(numItems):
#         spdsht.write(title_section[i].text + "\n")
