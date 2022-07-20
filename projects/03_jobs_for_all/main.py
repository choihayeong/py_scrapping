import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"


def extract_brand_info(html):
    brand_name = html.find("span", {"class" : "company"}).text
    brand_url = html.find("a")['href']
    
    return {
        "brand": brand_name,
        "site": brand_url
    }

brands_info = []

def extract_brands():
    alba_requests = requests.get(alba_url)
    soup = BeautifulSoup(alba_requests.text, "html.parser")
    brand_list = soup.find("div", {"id" : "MainSuperBrand"})
    brands = brand_list.find_all("li", {"class" : "impact"})

    for brand in brands:
        info = extract_brand_info(brand)
        brands_info.append(info)

    return brands_info


extract_brands()

LIMIT = len(brands_info) # 133

def extract_each_info(html):
    place = html.find("td", {"class" : "local"})
    title = html.find("td", {"class" : "title"})
    data = html.find("td", {"class" : "data"})
    pay = html.find("td", {"class" : "pay"})
    date = html.find("td", {"class" : "regDate"})
    
    if (place != None):
        place = place.text
    if (title != None):
        title = title.find("span", {"class" : "company"}).text
    if(data != None):
        data = data.find("span").text
    if(pay != None):
        pay = pay.text
    if(date != None):
        date = date.text
    
    return {
        "place": place,
        "title": title,
        "time": data,
        "pay": pay,
        "date": date
    }


def extract_each(brand_info):
    each_info = {
        "name": '',
        "jobs": []
    }

    disabled_char = ['?', '/', '%', '*', ':', '|', '"', '>', '<', ".", "\r"]

    each_info["name"] = brand_info["brand"]
    
    for char in disabled_char:
        if (brand_info["brand"].find(char) != -1):
            each_info["name"] = brand_info["brand"].replace(char, " ")

    res = requests.get(brand_info["site"])
    each_soup = BeautifulSoup(res.text, "html.parser")
    job_list = each_soup.find("tbody").find_all("tr", {"class" : ""})

    if job_list != None:
        for job_item in job_list:
            if job_item != None:
                job = extract_each_info(job_item)
        
                each_info["jobs"].append(job)
        
    return each_info


def save_each_file(each_jobs):
    file = open(f"{each_jobs['name']}.csv", mode="w", encoding="utf-8")
    writer = csv.writer(file)

    writer.writerow(["place", "title", "time", "pay", "date"])

    for job in each_jobs["jobs"]:
        writer.writerow(list(job.values()))
    
    return
    
    
def extract_all_brands(brands_info):  
    for brand_info in brands_info:
        each_brand_jobs = extract_each(brand_info)
        save_each_file(each_brand_jobs) # csv
        
extract_all_brands(brands_info)
