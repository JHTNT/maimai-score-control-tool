import csv
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

thread_local = threading.local()
drivers = []
all_sheet_data = []

options = Options()
# hide browser window
options.add_argument("--headless")
# only show fatal message in console
# INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3
options.add_argument("--log-level=3")
# disable images and css to speed up
options.set_preference("permissions.default.stylesheet", 2)
options.set_preference("permissions.default.image", 2)


def get_driver():
    """
    Get the driver of current thread, if not exist then create a new one.
    """
    if not hasattr(thread_local, "driver"):
        thread_local.driver = webdriver.Firefox(options=options)
        drivers.append(thread_local.driver)
    return thread_local.driver


def get_sheet_info(link: tuple[int, str]):
    driver = get_driver()
    url = link[1]
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))

    # get song info
    title = driver.find_element(By.TAG_NAME, "h1").text
    category = driver.find_element(
        By.XPATH, "//th/span[text()='Category']/../following-sibling::td/span"
    ).text
    version = driver.find_element(
        By.XPATH, "//th/span[text()='Version']/../following-sibling::td/span"
    ).text

    # get sheet data
    sheet_data = []
    sheets = driver.find_elements(
        By.XPATH, "//h2/following-sibling::div/div/div/div/table/tbody/tr"
    )
    for sheet in sheets:
        if sheet.find_element(By.XPATH, "./td[5]").text == "":
            continue

        sheet_type = sheet.find_element(By.XPATH, "./td[1]").text
        difficulty = sheet.find_element(By.XPATH, "./td[2]").text
        level = sheet.find_element(By.XPATH, "./td[3]").text
        tap = int(sheet.find_element(By.XPATH, "./td[6]").text)
        hold = int(sheet.find_element(By.XPATH, "./td[7]").text)
        slide = int(sheet.find_element(By.XPATH, "./td[8]").text)
        touch = sheet.find_element(By.XPATH, "./td[9]").text
        touch = 0 if touch == "" else int(touch)
        bk = int(sheet.find_element(By.XPATH, "./td[10]").text)
        magnitude = tap + hold * 2 + slide * 3 + touch + bk * 5
        sheet_data.append(
            {
                "ID": link[0],
                "Title": title,
                "Category": category,
                "Version": version,
                "Type": sheet_type,
                "Difficulty": difficulty,
                "Level": level,
                "TAP": tap,
                "HOLD": hold,
                "SLIDE": slide,
                "TOUCH": touch,
                "BREAK": bk,
                "Magnitude": magnitude,
            }
        )
    return sheet_data


def main():
    # start timing
    start_time = time.time()
    driver = webdriver.Firefox(options=options)
    driver.get("https://arcade-songs.zetaraku.dev/maimai/songs/")

    # show all songs
    print("正在獲取歌曲列表...")
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "v-select__slot")))
    btn = driver.find_element(By.CLASS_NAME, "v-select__slot")
    driver.execute_script("arguments[0].click();", btn)
    WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'v-list-item__title') and text()='All']")
        )
    )
    driver.find_element(
        By.XPATH, "//div[contains(@class, 'v-list-item__title') and text()='All']"
    ).click()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//tr/td[text()='1']"))
    )

    # get song links
    song_links = []
    links = driver.find_elements(By.CSS_SELECTOR, "tr td a[href^='/maimai/song/?id=']")
    for link in links:
        id = int(link.find_element(By.XPATH, "./../../td[1]").text)
        song_links.append((id, link.get_attribute("href")))
    driver.quit()

    # get sheet info
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_sheet_info, link) for link in song_links]
        for future in tqdm(as_completed(futures), total=len(song_links)):
            all_sheet_data.extend(future.result())

    # close all drivers
    for driver in drivers:
        try:
            driver.quit()
        except:
            pass

    # write to csv
    all_sheet_data.sort(key=lambda x: x["ID"])
    with open("sheet_data.csv", "w", encoding="utf-8", newline="") as f:
        fields = [
            "ID",
            "Title",
            "Category",
            "Version",
            "Type",
            "Difficulty",
            "Level",
            "TAP",
            "HOLD",
            "SLIDE",
            "TOUCH",
            "BREAK",
            "Magnitude",  # 物量當量
        ]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for sheet in all_sheet_data:
            writer.writerow(sheet)
        f.close()

    # end timing
    end_time = time.time()
    print(f"總耗時：{end_time - start_time:.2f}s")


if __name__ == "__main__":
    main()
