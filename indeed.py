import requests
from bs4 import BeautifulSoup

LIMIT = 15
URL = "https://kr.indeed.com/jobs?q=python&l=&from=searchOnHP"

def get_last_page():
  result = requests.get(URL)
  
  soup = BeautifulSoup(result.text, "html.parser")
  
  pagination = soup.find("ul", {"class": "pagination-list"})
  
  links = pagination.find_all("a")
  pages = []
  
  for link in links[:-1]:
    pages.append(int(link.string))
  
  max_page = pages[-1]

  return max_page

def extract_job(html):
  title = html.find("h2", {"class": "jobTitle"})
  company = html.find("span", {"class": "companyName"})
  location = html.find("div", {"class": "companyLocation"})
  job_id = ""
  
  if (title != None):
    job_id = title.find("a")["data-jk"]
    title = title.find("a")["aria-label"]
    company_anchor = company.find("a")
    
    if (company_anchor != None):
      company = company_anchor.string
    else:
      company = company.string

    company = company.strip()
    location = location.string
    
  return {
    "title": title, 
    "company": company, 
    "location": location, 
    "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
  }

def extract_jobs(last_page):
  jobs = []
  
  for page in range(last_page):
    print(f"Scrapping page {page}")
    
    result = requests.get(f"{URL}&start={page * LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    result_list = soup.find("ul", {"class" : "jobsearch-ResultsList"})
    results = result_list.find_all("li")
  
    for result in results:
      job = extract_job(result)
  
      if (job['title'] != None):
        jobs.append(job)
  
  return jobs

def get_jobs():
  last_page = get_last_page()
  jobs = extract_jobs(last_page)

  return jobs