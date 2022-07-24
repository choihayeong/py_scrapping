import requests
from bs4 import BeautifulSoup

# extract_jobs
def extract_jobs(keyword):
  jobs = []
  
  call_url = f"https://remoteok.com/remote-{keyword}-jobs"
  headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"}

  call_url = requests.get(call_url, headers=headers)
  soup = BeautifulSoup(call_url.text, "html.parser")
  jobs_list = soup.find("table", {"id" : "jobsboard"}).find_all("tr", {"class" : "job"})

  for item in jobs_list:
    info_box = item.find("td", {"class" : "company"})
    company = info_box.find("h3").text.strip()
    title = info_box.find("h2").text.strip()
    link = info_box.find("a", {"class" : "preventLink"})["href"]

    job_item = {
      "company": company,
      "title": title,
      "link": f"https://remoteok.com{link}"
    }
    jobs.append(job_item)

  return jobs

def get_jobs(keyword):  
  jobs = extract_jobs(keyword)

  return jobs

# print(get_jobs("vue"))