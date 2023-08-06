import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import threading

headers = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Mobile Safari/537.36"
}

errors = []
err_msg_network = "Make Sure You Have An Internet Connection."

session = requests.Session()  # create a session

def saveAsForked(name, src, about, tech_stacks, license_, from_, stars):
    forked[name] = {
        "src": src,
        "about": about,
        "tech_stack": tech_stacks,
        "license": license_,
        "from": from_,
        "stars": stars,

    }


def save(name, src, about, tech_stacks, license_, stars, forked_by):
    projectInfo[name] = {
        "src": src,
        "about": about,
        "tech_stack": tech_stacks,
        "license": license_,
        "stars": stars,
        "forked_by": forked_by,

    }


def handle_pagination(username, url):

    try:
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")

        try:
            username = soup.find(
                attrs={"itemprop": "additionalName"}).text.strip()

        except Exception as e:
            errors.append(e)

        for div in soup.findAll("div", id="user-repositories-list"):
            for li in div.select('ul>li'):

                inner_soup = BeautifulSoup(str(li), "lxml")
                tech_stacks = []
                license_ = ""
                name = ""
                about = ""
                from_ = ""
                stars = ""
                forked_by = ""
                src = f"https://github.com/{li.a['href']}"

                # if li.a.text.strip() != username:
                try:
                    name = inner_soup.find(
                        attrs={"itemprop": "name codeRepository"}).text.strip()
                except Exception as e:
                    errors.append(e)
                try:
                    about = inner_soup.find(
                        attrs={"itemprop": "description"}).text.strip()
                except Exception as e:
                    errors.append(e)
                try:
                    tech_stacks.append(inner_soup.find(
                        attrs={"itemprop": "programmingLanguage"}).text.strip())
                except Exception as e:
                    errors.append(e)
                try:
                    stars = inner_soup.find(
                        attrs={"href": f"/{username}/{name}/stargazers"}).text.strip()

                except Exception as e:
                    errors.append(e)
                try:
                    forked_by = inner_soup.find(
                        attrs={"href": f"/{username}/{name}/network/members"}).text.strip()

                except Exception as e:
                    errors.append(e)
                try:
                    if li.select('span')[len(li.select('span')) - 1]['class'][0] == 'mr-3':
                        license_ = li.select('span')[len(
                            li.select('span')) - 1].text.strip()

                    # if "Template" == li.span.text.strip():
                    #     license_ = li.select("span")[5].text.strip()

                except Exception as e:
                    errors.append(e)
                try:

                    if "Forked" in li.div.div.findAll("span")[2].text.strip():
                        from_ = li.div.div.findAll("span")[2].text.strip()

                    # if "Template" == li.span.text.strip():
                    #     from_ = li.select("span")[1].text.strip()

                except Exception as e:
                    errors.append(e)

                try:

                    if "Forked" in li.div.div.findAll("span")[2].text.strip():
                        saveAsForked(name, src, about,
                                     tech_stacks, license_, from_, stars)
                    else:
                        save(name, src, about, tech_stacks,
                             license_, stars, forked_by)

                except Exception as e:
                    errors.append(e)
                    save(name, src, about, tech_stacks,
                         license_, stars, forked_by)

        try:
            if soup.find(attrs={"data-test-selector": "pagination"}):
                div = soup.find(
                    attrs={"data-test-selector": "pagination"}).select("a")

                for a in div:
                    if a.text == "Next":
                        url = a['href']
                errors.clear()
                handle_pagination(username, url)
        except Exception as e:
            errors.append(e)
    except Exception as e:
        errors.append(err_msg_network)
        exit(0)


def loader(url, username):
    try:
        response = session.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "lxml")
        # print(soup)
        total_projects = soup.find(
            "span", class_="Counter").text.strip()
        print(f"Hello {username}\n")

        print(f"{total_projects} repositories found.")
        print(f"NOTE: The private repositories will not be fetched.\n")

        for i in tqdm(range(int(total_projects))):
            time.sleep(0.2)
    except Exception as e:
        print(e)
        errors.append(e)


def scrape(_username):
    global projectInfo
    projectInfo = {}
    global forked
    forked = {}

    fileName = f"{_username}-projects.json"
    first_url = f"https://github.com/{_username}?tab=repositories"

    p1 = threading.Thread(target=handle_pagination,
                          args=[_username, first_url])
    p1.start()

    loader(first_url, _username)

    projectInfo['FORKED'] = forked

    if len(projectInfo) == 1 and len(projectInfo['FORKED']) == 0:
        if err_msg_network in errors:
            print("\n", err_msg_network.upper(), "\n")
            return
        print("Note: Check for the conditions below-\n\n1. Username does not exist.\n2. Username is of an organization.\n\n")
        return

    _json = open(fileName, 'w', encoding="utf-8")
    _json.write(json.dumps(projectInfo))
    _json.close()
    print(
        f"Done! checkout your {_username}-projects.json file at the root of this directory\n")
    return
