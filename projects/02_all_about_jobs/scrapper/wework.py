import requests
from bs4 import BeautifulSoup

# weworkremotely.com
def extract_job_from_wework(html):
  jobs = []
  jobs_sections = html.find_all("section", {"class" : "jobs"})

  for section in jobs_sections:
    info = section.find("ul").find_all("li", {"class" : "feature"})
    
    for item in info:
      info_box = item.find("div", {"class" : "tooltip"}).find_next_sibling("a")
      info_company = info_box.find_all("span", {"class" : "company"}, limit=1)[0].text
      info_title = info_box.find("span", {"class" : "title"}).text
      info_link = info_box["href"]

      job_item = {
        "company": info_company,
        "title": info_title,
        "link": f"https://weworkremotely.com{info_link}"
      }
      jobs.append(job_item)
  
  return jobs


# extract_jobs
def extract_jobs(site):
  if (site["site"] == "wework"):
    call_url = requests.get(site["url"])
    soup = BeautifulSoup(call_url.text, "html.parser")
    jobs = extract_job_from_wework(soup)

  return jobs

def get_jobs(keyword):
  wework = {
    "site" : "wework",
    "url" : f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
  }
  
  jobs = extract_jobs(wework)

  return jobs

# print(get_jobs("vue"))