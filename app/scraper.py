from .functions import (initialize_driver, 
                        accept_cookies, 
                        click_show_all_buttons, 
                        extract_page_text, 
                        extract_html_text, 
                        process_text, 
                        highlight_input_text)

def scrape_word(word: str):
    driver = initialize_driver()
    url = f"https://translate.google.com/details?sl=en&tl=es&text={word}&op=translate"

    try:
        driver.get(url)
        accept_cookies(driver)
        
        click_show_all_buttons(driver)
        
        # Try to extract page text
        page_text = extract_page_text(driver)
        html_text = extract_html_text(driver)
        
        # Check if the page_text contains the expected content, otherwise highlight input text
        if "Translation error" in page_text:
            highlight_input_text(driver, word)
            
            page_text = extract_page_text(driver)

        results = process_text(page_text, html_text, word)

    except Exception as e:
        print(f"Error scraping word: {e}")
        results = None
    finally:
        driver.quit()

    return results
