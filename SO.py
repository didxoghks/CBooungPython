
import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=blockchain"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class" : "s-pagination"}).find_all("a")

    page = []

    for c in pagination:
        page.append(c.find("span").get_text())

    page = page[:-1]
    last_page = page[-1]
    return int(last_page)


def extract_job(html):
    title = html.find("h2",{"class" : "mb4"}).find("a")["title"]
    company, location  = html.find("h3",{"class":"fs-body1"}).find_all("span",recursive=False)
    #이런걸 unpacking value 라고 합니다.
    company = company.get_text(strip = True)
    location = location.get_text(strip = True)#.strip("\n") 나는 안써줘도 될 듯?
    job_id = html["data-jobid"]
    apply_link = f"https://stackoverflow.com/jobs/{job_id}"

    return {'title' : title,
            'company' : company,
            'location' : location,
            'apply_link' : apply_link}

def extract_jobs(last_page):

    jobs = []
    for page in range(last_page):
        # print(f"Scrapping SO page number {page}")
        result = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        #results = soup.find_all("div", {"class": "grid"}) 이 grid 에는 직업카드가 아닌 광고도 있어서 놉 안됨
        results = soup.find_all("div",{"class" : "-job"})


        for result in results:
            job = extract_job(result)
            jobs.append(job)

    return jobs



def get_jobs():

    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs

last_page = get_last_page()
extract_jobs(last_page)