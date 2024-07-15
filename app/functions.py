import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

def initialize_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920x1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def accept_cookies(driver):
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        buttons = driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if 'accept' in button.text.lower() or 'zgadzam się' in button.text.lower():
                button.click()
                print("Accepted cookies.")
                break
        else:
            print("Accept all button not found.")
    except Exception as e:
        print(f"Error clicking Accept all button: {e}")

def click_show_all_buttons(driver):
    try:
        show_all_buttons = driver.find_elements(By.XPATH, "//span[contains(text(), 'Show all')]")
        for button in show_all_buttons:
            driver.execute_script("arguments[0].click();", button)
            print(f"Clicked button: {button.text}")
    except Exception as e:
        print(f"Error clicking 'Show all' buttons: {e}")

def extract_page_text(driver):
    page_text = driver.find_element(By.TAG_NAME, "body").text
    return page_text

def highlight_input_text(driver, word):
    try:
        input_element = driver.find_element(By.XPATH, "//input[@aria-label='Source text']")
        input_element.clear()
        input_element.send_keys(word)
        action = ActionChains(driver)
        action.move_to_element(input_element).click_and_hold().move_by_offset(10, 0).release().perform()
        print("Highlighted input text to see details.")
    except Exception as e:
        print(f"Error highlighting input text: {e}")

def save_screenshot(driver, filename):
    try:
        driver.save_screenshot(filename)
        print(f"Screenshot saved as {filename}")
    except Exception as e:
        print(f"Error saving screenshot: {e}")

def process_text(page_text, word):
    translations = []
    definitions = []
    synonyms = []
    examples = []

    # Extract translation section
    try:
        translation_section = page_text.split("Translation results")[1].split("Send feedback")[0].strip()
        if "More translations" in translation_section:
            pattern = r"(\w+)\n(Verb|Noun|Adjective)"
            matches = re.findall(pattern, translation_section)
            translations.extend([match[0] for match in matches])
            translation_section = translation_section.split("More translations")[0].strip()
        if "feminine" not in translation_section:
            translation_section = translation_section.split("See dictionary")[0].strip()
        translations.extend([line.strip() for line in translation_section.split("\n") if line.strip() and not line.startswith(("Noun", "Translation"))])
    except IndexError:
        print("Error processing translation section")
    
    # Extract definitions section
    try:
        definitions_section = page_text.split(f"Definitions of {word}")[1].split(f"Examples of {word}")[0].strip()
        if "Show all" in definitions_section:
            definitions_section = definitions_section.split("Show all")[0].strip()
        lines = definitions_section.split("\n")[1:]
        skip_next = False

        for line in lines:
            if skip_next:
                parts = line.strip().split()
                i = 0
                while i < len(parts):
                    if i < len(parts) - 1 and parts[i + 1] in ["with", "against", "of"]:
                        synonyms.append(f"{parts[i]} {parts[i + 1]}")
                        i += 2
                    else:
                        synonyms.append(parts[i])
                        i += 1
                skip_next = False
                continue

            if "Synonyms" in line:
                skip_next = True
                continue

            if line.strip() and line.endswith('.') and not line[0].isdigit() and line.strip() not in ["INFORMAL", "Verb", "NAUTICAL", "Abbreviation", "MEDICINE", "Fewer definitions"]:
                definitions.append(line.strip())
    except IndexError:
        print("Error processing definitions section")
    
    # Extract examples section
    try:
        examples_section = page_text.split(f"Examples of {word}")[1].split(f"Translations of {word}")[0].strip()
        examples.extend([line.strip() for line in examples_section.split("\n") if word in line])
    except IndexError:
        print("Error processing examples section")

    results = {
        "word": word,
        "translations": list(dict.fromkeys(translations)),
        "definitions": definitions,
        "synonyms": list(dict.fromkeys(synonyms)),
        "examples": examples
    }
    return results
