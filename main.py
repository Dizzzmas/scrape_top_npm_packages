import csv
from os import abort
from time import sleep
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def setup_chrome_webdriver():
    chrome_options = webdriver.ChromeOptions()

    chrome_options.add_argument("--headless")  # disables the GUI for chromium
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.binary_location = "./bin/headless-chromium"
    return chrome_options


def setup_headless_chrome():
    chrome_options = setup_chrome_webdriver()

    driver = webdriver.Chrome(executable_path="./bin/chromedriver", chrome_options=chrome_options)
    return driver


def main():
    found_github_urls = []  # Store all github urls here to avoid duplicates

    npm_urls_to_process = []

    with open(
            "npm_package_urls.csv", "r", newline=""
    ) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            npm_urls_to_process.append(row.get('npm_url'))

        for index, url in enumerate(npm_urls_to_process):
            response = requests.get(url)
            if not response.ok:
                log.info(f"Failed at index: {index}, url: {url}")
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
        # try:
        #     driver.get(npm_url)  # Go to the npm package page
        # except:
        #     log.info("Failed at ")
        # try:
        #     package_infos = driver.find_elements_by_xpath(
        #         "//div[contains(@class,'dib w-50 bb b--black-10 pr2 w-100')]"
        #     )  # Get the element with infos about the package
        # except Exception as exception:
        #     log.exception(exception)
        #     if len(driver.window_handles) > 1 and driver.window_handles[1] and driver.current_url.startswith(
        #             "https://www.npmjs.org"):
        #         driver.close()
        #     continue
        # gh_repo_data = [
        #     info for info in package_infos if "Repository" in info.text
        # ]  # Get the element with Github repo details
        # if gh_repo_data:
        #     github_url = (
        #         gh_repo_data[0]
        #             .find_element_by_class_name("link")
        #             .get_attribute("href")  # Extract the github url
        #     )
        #     if github_url not in found_github_urls:
        #         found_github_urls.append(github_url)
        #         # Save url to csv
        #         with open(
        #                 "npm_package_urls.csv", "a+", newline=""
        #         ) as csvfile:
        #             fieldnames = ["github_url"]
        #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #             writer.writerow({"github_url": github_url})
        #
        #         log.info(f"Found url: {github_url}")
        # if len(driver.window_handles) > 1 and driver.window_handles[1] and driver.current_url.startswith(
        #         "https://www.npmjs.org"):
        #     driver.close()  # close the tab with the npm package data and repeat the process
    return "All urls scraped successfully"


if __name__ == '__main__':
    main()
