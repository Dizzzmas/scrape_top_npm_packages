import csv
from os import abort
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
    return chrome_options


def setup_headless_chrome():
    chrome_options = setup_chrome_webdriver()

    driver = webdriver.Chrome(chrome_options=chrome_options
    )
    return driver


def main():
    found_github_urls = []  # Store all github urls here to avoid duplicates
    found_npm_urls = []  # Store all npm urls to avoid duplicates

    # Create a file to store scraped GitHub urls
    with open("github_urls_for_npm_packages.csv", "w", newline="") as csvfile:
        fieldnames = ["github_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    try:
        driver = setup_headless_chrome()
    except Exception as exception:
        log.info("Couldn't setup webdriver")
        log.exception(exception)
        abort()

    driver.get(
        "https://gist.github.com/anvaka/8e8fa57c7ee1350e3491"
    )  # Visit the github gist with top npm repos

    lists = driver.find_elements_by_css_selector(
        "ol[start='0']"
    )  # Lists of npm packages based on category

    for list in lists:
        for npm_link in list.find_elements_by_tag_name("a"):
            driver.switch_to.window(
                driver.window_handles[0] # Switch to the window with github gist
            )
            npm_url = npm_link.get_attribute("href")  # Get url to the npm package page
            if npm_url not in found_npm_urls:
                found_npm_urls.append(npm_url)
            else:
                continue
            driver.execute_script("window.open('');")  # Open a window for the npm page
            driver.switch_to.window(
                driver.window_handles[1]
            )  # Switch to the npm window
            driver.get(npm_url)  # Go to the npm package page

            package_infos = driver.find_elements_by_xpath(
                "//div[contains(@class,'dib w-50 bb b--black-10 pr2 w-100')]"
            )  # Get the element with infos about the package
            gh_repo_data = [
                info for info in package_infos if "Repository" in info.text
            ]  # Get the element with Github repo details
            if gh_repo_data:
                github_url = (
                    gh_repo_data[0]
                    .find_element_by_class_name("link")
                    .get_attribute("href")  # Extract the github url
                )
                if github_url not in found_github_urls:
                    found_github_urls.append(github_url)
                    # Save url to csv
                    with open(
                        "github_urls_for_npm_packages.csv", "a+", newline=""
                    ) as csvfile:
                        fieldnames = ["github_url"]
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow({"github_url": github_url})

                    log.info(f"Found url: {github_url}")

            driver.close()  # close the tab with the npm package data and repeat the process


if __name__ == "__main__":
    main()
