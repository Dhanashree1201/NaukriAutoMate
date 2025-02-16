import time
import re
import os
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from google import genai
from dotenv import load_dotenv
from gemini_api import bard_flash_response
from helper import extract_text_from_pdf

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("GOOGLE_API_KEY")


# Configuration for the WebDriver and paths
driver_path = "./geckodriver.exe"
binary = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
profile_path = "C:\\Users\\User\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\gf13svj6.default-release"
maxcount = 50
threshold = 35
isEnd = False

skills = ['html', 'css', 'javascript', 'typescript',
          'react.js', 'node.js', 'react-native', 'mongodb', 'express']
location = 'pune'
experience = 10
job_age = 7

# Helper functions


def generate_url(skills, location, experience, job_age):
    base_url = "https://www.naukri.com/"

    # Format skills as a hyphenated string (replace '.' with 'dot' and join skills)
    skills_formatted = '-'.join([skill.replace('.', '-dot-')
                                for skill in skills])

    # Create query parameters
    query_params = {
        'experience': experience,  # Years of experience
        'jobAge': job_age         # Job age in days
    }

    # Encode the query parameters
    query_string = urllib.parse.urlencode(
        query_params, quote_via=urllib.parse.quote)

    # Combine the base URL with the formatted skills and query parameters
    full_url = f"{base_url}{skills_formatted}-jobs-in-{location}?{query_string}"

    return full_url


def setup_driver():
    service = Service(driver_path)
    options = Options()
    options.binary_location = binary
    profile = FirefoxProfile(profile_path)
    options.profile = profile
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def extract_keywords(text):
    return set(re.findall(r'\w+', text.lower()))


def get_match_score(job_description, resume):
    prompt = f"Calculate the match score between the following Job Description and Resume. Keep this aspects as main skills & experience. Return only the match score as a number between 0 and 100. DONT ADD ANYTHING EXTRA, GIVE 0 ON JAVA, PYTHON, DOT NET ROLES\n\nJob Description: {job_description}\nResume: {resume}"
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt)
    return response.text


def apply_for_job(driver, job_url, resume_text, threshold):
    driver.execute_script("window.open(arguments[0], '_blank');", job_url)
    time.sleep(3)

    original_window = driver.current_window_handle
    job_windows = driver.window_handles
    new_window = [
        window for window in job_windows if window != original_window][0]
    driver.switch_to.window(new_window)

    try:
        company_site_buttons = driver.find_elements(
            By.ID, "company-site-button")
        walk_in = driver.find_elements(By.ID, "walkin-button")
        jd_container_elements = driver.find_elements(
            By.CLASS_NAME, "jdContainer")
        already_applied = driver.find_elements(By.ID, "already-applied")

        if company_site_buttons or jd_container_elements or walk_in or already_applied:
            # Skip job if already applied
            return False

        # Extract job description and calculate match score
        job_description = driver.find_element(
            By.XPATH, "//*[contains(@class, 'styles_JDC__match-score')]").text
        job_keywords = extract_keywords(job_description)
        match_score = int(get_match_score(job_keywords, resume_text))
        print(match_score)
        if match_score < threshold:
            print(f"Skipping job due to low match score ({match_score}%)")
            return False

        # Apply for job
        driver.find_element(By.ID, "apply-button").click()

        time.sleep(5)

        chatBot = driver.find_elements(
            By.CLASS_NAME, "chatbot_DrawerContentWrapper")
        print(chatBot)
        # Check if a chatbot or question popup exists
        if chatBot:
            print("Chatbot detected, handling questions...")
            handle_questions(driver)

            # After handling questions, check if application was successful
            if WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]"))):
                print("Successfully applied after handling questions.")
                return True
            else:
                print("Failed to apply after handling questions.")
                return False

        # Wait for success message if no chatbot present
        if WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'apply-message') and contains(text(), 'successfully applied')]"))):
            print("Successfully applied.")
            return True

    except Exception as e:
        print(f"Error applying for job: {e}")
        return False
    finally:
        driver.close()
        driver.switch_to.window(original_window)


def handle_questions(driver):
    while True:
        try:
            question = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "(//li[contains(@class, 'botItem')])[last()]//span"))
            ).text

            print(f"Question: {question}")

            if "Thank you for your responses." in question:
                break

            # Handle various input types
            input_elements = driver.find_elements(
                By.XPATH, "//*[contains(@id, 'userInput')]")
            radio_buttons = driver.find_elements(
                By.XPATH, "//*[contains(@class, 'ssrc__radio-btn-container')]")
            chip_elements = driver.find_elements(
                By.XPATH, "//*[contains(@class, 'chipItem')]")

            if chip_elements:
                print("IN CHIP")
                chip_elements[0].click()
            elif radio_buttons:
                print("IN RADIO")
                options = [f"{index}. {btn.find_element(By.CSS_SELECTOR, 'label').text}" for index, btn in enumerate(
                    radio_buttons, start=1)]
                selected_option = int(bard_flash_response(
                    f"{question}\n" + "\n".join(options)))
                inputEle = radio_buttons[selected_option -
                                         1].find_element(By.CSS_SELECTOR, 'label')
                time.sleep(5)
                print(inputEle.is_displayed())
                if inputEle.is_displayed():
                    inputEle.click()
                print(inputEle.is_displayed())
            elif input_elements:
                print("IN INPUT")
                for text_input in input_elements:
                    text_input.send_keys(bard_flash_response(question))

            WebDriverWait(driver, 3).until(EC.element_to_be_clickable(
                (By.XPATH, "//*[contains(@class, 'sendMsg')]"))).click()
            time.sleep(3)
        except Exception as e:
            print(f"Error during question handling: {e}")
            break


def navigate_pages(driver):
    try:
        # Find the 'Next' button
        next_page_button = driver.find_elements(
            By.XPATH, "//a[contains(@class, 'styles_btn-secondary')]")

        # Check if the 'Next' button is disabled (if it is, we're on the last page)
        if 'disabled' in next_page_button[1].get_attribute('class'):
            print("No more pages to go to.")
            isEnd = True

        # If the 'Next' button is enabled, click it to go to the next page
        next_page_button[1].click()
        # Adjust the sleep time based on your needs to ensure the page loads
        time.sleep(3)

    except Exception as e:
        print(f"Error navigating pages: {e}")
        isEnd = True


def main(resume_text):
    driver = setup_driver()
    driver.get(generate_url(skills, location, experience, job_age))
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class='title ']")))

    applied = 0
    while applied < maxcount and not isEnd:
        job_elements = driver.find_elements(By.XPATH, "//a[@class='title ']")
        for job_element in job_elements:
            job_url = job_element.get_attribute("href")
            if apply_for_job(driver, job_url, resume_text, threshold):
                applied += 1
            time.sleep(3)
        navigate_pages(driver)

    driver.quit()


if __name__ == "__main__":
    resume_text = extract_text_from_pdf()
    main(resume_text)
