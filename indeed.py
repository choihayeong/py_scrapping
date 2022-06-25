import requests
from bs4 import BeautifulSoup

LIMIT = 15
URL = "https://kr.indeed.com/jobs?q=python&l=&from=searchOnHP"

def extract_indeed_pages():
  result = requests.get(URL)
  
  soup = BeautifulSoup(result.text, "html.parser")
  
  pagination = soup.find("ul", {"class": "pagination-list"})
  
  links = pagination.find_all("a")
  pages = []
  
  for link in links[:-1]:
    pages.append(int(link.string))
  
  max_page = pages[-1]

  return max_page


def extract_indeed_jobs(last_page):
  jobs = []
  
  #for page in range(last_page):
  result = requests.get(f"{URL}&start={0 * LIMIT}")
  soup = BeautifulSoup(result.text, "html.parser")
  result_list = soup.find("ul", {"class" : "jobsearch-ResultsList"})
  results = result_list.find_all("li")

  for result in results:
    title = result.find("h2", {"class": "jobTitle"})
    company = result.find("span", {"class": "companyName"})
    
    if (title != None):
      title = title.find("a")["aria-label"]
      company_anchor = company.find("a")
      
      print(title)
      
      if (company_anchor != None):
        company = company_anchor.string
      else:
        company = company.string

      company = company.strip()
      print(company)
  
  return jobs