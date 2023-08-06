import dataclasses

import selenium.webdriver
import selenium.webdriver.remote.webdriver
import webdriver_manager.chrome


@dataclasses.dataclass(frozen=True)
class ChromeOptions:
    no_sandbox: bool = True
    start_maximized: bool = True


def create_chrome_driver(
    headless: bool = False,
) -> selenium.webdriver.Chrome:
    options = selenium.webdriver.ChromeOptions()
    for opt in [
        "--no-sandbox",
        "--start-maximized",
    ]:
        options.add_argument(opt)
        # all https://peter.sh/experiments/chromium-command-line-switches/
    options.headless = headless
    manager = webdriver_manager.chrome.ChromeDriverManager()
    return selenium.webdriver.Chrome(
        options=options,
        executable_path=manager.install(),
    )


def create_firefox_driver(
    headless: bool = False,
) -> selenium.webdriver.Firefox:
    options = selenium.webdriver.FirefoxOptions()
    options.headless = headless
    return selenium.webdriver.Firefox(options=options)


def create_aws_lambda_chrome_driver() -> selenium.webdriver.Chrome:
    options = selenium.webdriver.ChromeOptions()
    for option in [
        "--no-sandbox",
        "--single-process",
        "--disable-dev-shm-usage",
        "--homedir=/tmp",
    ]:
        options.add_argument(options)
    options.headless = True
    options.binary_location = "/opt/headless-chromium"
    return selenium.webdriver.Chrome("/opt/chromedriver", options=options)


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
