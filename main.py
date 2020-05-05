import csv
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def main():
    found_github_urls = []  # Store all github urls here to avoid duplicates

    npm_urls_to_process = []

    with open(
            "npm_package_urls.csv", "r", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            npm_urls_to_process.append(row.get('npm_url'))

    # Start actual scraping of GitHub urls
    for index, url in enumerate(npm_urls_to_process):
        response = requests.get(url)
        if not response.ok:
            log.info(f"Failed at index: {index}, url: {url}. Will sleep for 5 mins")
            sleep(300)

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        package_infos = soup.find_all("div", {
            "class": ["dib", "w-50", "bb", "b--black-10", "pr2", "w-100"]})  # The repository section

        gh_repo_data = [
            info for info in package_infos if
            "RepositoryGitgithub.com" in info.text and "Installnpm" not in info.text
        ]

        if gh_repo_data:
            github_url = (
                gh_repo_data[0].find_all("a", href=True)[0]["href"]
            )

            log.info(f"Found GitHub url: {github_url}, {index} of {len(npm_urls_to_process)}")

            with open(
                    "npm_package_urls.csv", "a+", newline=""
            ) as csvfile:
                fieldnames = ["github_url"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({"github_url": github_url})

    return "All urls scraped successfully"


if __name__ == '__main__':
    main()
