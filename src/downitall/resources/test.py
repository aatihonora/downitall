import time

from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver  # <<< This replaces normal selenium.webdriver

# Setup Chrome with headless mode (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Remove this if you want to see the browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Create the Selenium Wire driver
driver = webdriver.Chrome(options=chrome_options)

# Target video page URL (replace this with your actual target)
driver.get("https://vidjoy.pro/embed/movie/27205")

# Wait for traffic to load
time.sleep(10)  # Increase if needed for slower pages

# Filter and print .m3u8 URLs
print("\nFound Streaming Links:")
with open("found_streams.txt", "a") as out_file:
    for request in driver.requests:
        if request.response:
            url = request.url
            if ".m3u8" in url or ".mp4" in url or ".ts" in url:
                print(url)
                out_file.write(url + "\n")

# Clean up
driver.quit()
