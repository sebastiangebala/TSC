import json
from selenium.webdriver.common.by import By
from .functions import initialize_driver, accept_cookies, click_show_all_buttons, extract_page_text, process_text, highlight_input_text, save_screenshot

def scrape_word(word: str):
    driver = initialize_driver()
    url = f"https://translate.google.com/details?sl=en&tl=es&text={word}&op=translate"

    try:
        driver.get(url)
        accept_cookies(driver)
        
        # Save screenshot after accepting cookies
        save_screenshot(driver, 'after_accepting_cookies.png')
        
        click_show_all_buttons(driver)
        
        # Try to extract page text
        page_text = extract_page_text(driver)
        
        # Check if the page_text contains the expected content, otherwise highlight input text
        if "Translation error" in page_text:
            highlight_input_text(driver, word)
            
            # Save screenshot after highlighting input text
            save_screenshot(driver, 'after_highlighting_input_text.png')
            
            page_text = extract_page_text(driver)

        results = process_text(page_text, word)

    except Exception as e:
        print(f"Error scraping word: {e}")
        results = None
    finally:
        driver.quit()

    return results
