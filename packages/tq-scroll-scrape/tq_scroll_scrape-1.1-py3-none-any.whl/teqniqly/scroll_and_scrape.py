"""
Scroll and Scrape module.
"""
import os
import time
from typing import Callable
import errors
from selenium import webdriver


# pylint: disable=too-few-public-methods
class ScrollAndScrape:
    """
    The ScrollAndScrape class manages the scrolling and downloading of pages.
    """

    def __init__(self):
        self._driver_path = os.path.join(os.getcwd(), "chromedriver.exe")

        if not os.path.exists(self._driver_path):
            raise errors.ChromeDriverNotFoundException(self._driver_path)

        self.driver = None

    def download(
            self,
            url: str,
            on_after_download: Callable[[str], None] = None,
            sleep_after_scroll_seconds: int = 2,
            **kwargs,
    ):
        """
        Downloads a page.
        Args:
            url: The page's URL.
            on_after_download: An optional callback to execute after the page downloads.
            sleep_after_scroll_seconds: The time in seconds to sleep after each scroll event.
            **kwargs: Additional keyword arguments to the function.
        """
        if sleep_after_scroll_seconds < 1:
            raise ValueError(
                "sleep_after_scroll_seconds value must be greater than zero."
            )

        scroll_by = None

        if kwargs.get("scroll_by") is not None:
            scroll_by = int(kwargs.get("scroll_by"))

            if scroll_by < 1:
                raise ValueError("scroll_by value must be greater than zero.")

        self.driver = webdriver.Chrome(
            executable_path=os.path.join(os.getcwd(), "chromedriver.exe")
        )

        self.driver.maximize_window()
        self.driver.get(url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        if kwargs.get("scroll_by") is not None:
            last_height = self.driver.execute_script("return window.pageYOffset")

        while True:
            if scroll_by is not None:
                self.driver.execute_script(f"window.scrollBy(0, {scroll_by})")
            else:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )

            time.sleep(sleep_after_scroll_seconds)

            if scroll_by is not None:
                new_height = self.driver.execute_script("return window.pageYOffset")
            else:
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )

            if new_height == last_height:
                break

            last_height = new_height

        if on_after_download is not None:
            on_after_download(self.driver.page_source)
