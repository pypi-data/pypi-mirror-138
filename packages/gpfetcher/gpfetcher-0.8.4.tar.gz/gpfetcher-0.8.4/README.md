# Github Projects Fetcher (gp-fetcher)

- This a tool to fetch your github project details so that your time for writing an API is saved.
- Simple to use tool made in Python with bs4(Beautiful Soup)

### Supports Apple Silicon Macs

#### Install the latest version to get full support

## Link to the package: [pypi.org/project/gpfetcher](https://pypi.org/project/gpfetcher/)

# Only if you want to skip the documentation then checkout this video [here](https://www.youtube.com/watch?v=xC6f_aGi8m0)

## Documentation

_Assuming python and pip installed on your system_

- _Checkout resources to install [python](https://www.python.org/downloads/) and [pip](https://packaging.python.org/tutorials/installing-packages/) if not installed_

---

#### Installing the package gpfetcher

For linux and mac

```bash

pip3 install gpfetcher
```

For windows

```bash
pip install gpfetcher
```

- Then use the package in your python file as shown below

## Usage

```python
from gpfetcher import scraper

if __name__ == "__main__":
    username = "< github username here >"
    scraper.scrape(username)
```

- After you get the message below, check your root where your .py file is , a json file is generated that can be used in your projects

```bash
  Done! checkout your {github-username-here}-projects.json file at the root of this project directory
```

##### You are done!

_go ahead and use this json to parse in your project_

## Sample Output

```json
{
    "gp-fetcher": {
        "src": "https://github.com//DevGautam2000/gp-fetcher",
        "about": "You don't want to spend a lot of time just writing a block of code for fetching your projects from github.
        So, go ahead and use this python package to make your life easier",
        "tech_stack": [
            "Python"
        ],
        "license": "MIT License",
        "stars": "",
        "forked_by": ""
    },
    "infoScraper": {
        "src": "https://github.com//DevGautam2000/infoScraper",
        "about": "Scraper written in Python using bs4 to scrape results from SMIT results",
        "tech_stack": [
            "Python"
        ],
        "license": "MIT License",
        "stars": "",
        "forked_by": ""
    },
    "results-web": {
        "src": "https://github.com//DevGautam2000/results-web",
        "about": "The web app for Results",
        "tech_stack": [
            "JavaScript"
        ],
        "license": "",
        "stars": "",
        "forked_by": ""
    },
    "results.github.io": {
        "src": "https://github.com//DevGautam2000/results.github.io",
        "about": "",
        "tech_stack": [
            "Python"
        ],
        "license": "",
        "stars": "",
        "forked_by": ""
    },
    "resume": {
        "src": "https://github.com//DevGautam2000/resume",
        "about": "",
        "tech_stack": [
            "JavaScript"
        ],
        "license": "",
        "stars": "",
        "forked_by": ""
    },
    "DevGautam2000": {
        "src": "https://github.com//DevGautam2000/DevGautam2000",
        "about": "Config files for my GitHub profile.",
        "tech_stack": [],
        "license": "",
        "stars": "",
        "forked_by": ""
    },
```

- Also fetches the forked repos separately

```json

       "forked_by": ""
    },
    "FORKED": {
        "Making-Musical-Apps": {
            "src": "https://github.com//DevGautam2000/Making-Musical-Apps",
            "about": "Resources for the O'Reilly book \"Making Musical Apps\"",
            "tech_stack": [
                "Pure Data"
            ],
            "license": "",
            "from": "Forked from nettoyeurny/Making-Musical-Apps",
            "stars": ""
        },
        "Simple-Guitar-Tuner": {
            "src": "https://github.com//DevGautam2000/Simple-Guitar-Tuner",
            "about": "Android app",
            "tech_stack": [
                "Java"
            ],
            "license": "",
            "from": "Forked from siemanko/Simple-Guitar-Tuner",
            "stars": ""
        }
    }
}

```

---

# Author

## Gautam Chandra Saha

2021 &copy; Gautam Chandra Saha

## License

[MIT](https://choosealicense.com/licenses/mit/)
