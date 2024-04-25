from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fill_google_form(form_link, num_responses, option_choices):
    # Initialize the Microsoft Edge WebDriver
    driver = webdriver.Edge()  # Ensure the Edge WebDriver is correctly set up in your PATH

    driver.get(form_link)
    time.sleep(2)  # Adding a delay to ensure the form is fully loaded

    # Allow multiple submissions
    for _ in range(num_responses):
        # Wait until questions are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[role="listitem"]'))
        )

        # Retrieve all question containers
        questions = driver.find_elements(By.CSS_SELECTOR, 'div[role="listitem"]')

        # Iterate over each question and select the appropriate option
        for index, question in enumerate(questions):
            if index < len(option_choices):
                option_to_select = option_choices[index]  # Get option for the current question
                try:
                    # Attempt to click on the specific option within this question
                    radio_button = question.find_element(By.XPATH, f'.//div[@aria-label="{option_to_select}"]')
                    radio_button.click()
                except Exception as e:
                    print(f"Error finding or clicking the radio button for question {index+1}: {e}")
            else:
                print(f"No option choice provided for question {index + 1}, skipping...")

        # Submit the form
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
            )
            submit_button.click()

            # Wait for the confirmation message after submission
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Your response has been recorded')]"))
            )
            print(f"Form submitted successfully for response {_ + 1}.")

            # Return to the form page for the next response, if there are more to do
            if _ < num_responses - 1:
                driver.get(form_link)
                time.sleep(2)  # Pause briefly before next fill
        except Exception as e:
            print(f"Error submitting the form: {e}")
            break

    # Close the browser window after filling the form
    driver.quit()

# Example usage
form_link = "https://docs.google.com/forms/d/e/1FAIpQLSerW5jkoWxMcsaBLxeUVqCJLxbdHOm4tYqDBDyJw1KYg3BAGA/viewform"
num_responses = 5  # Number of times to fill and submit the form
option_choices = ['yes', '2', 'no', 'Once in two months', '7', '1', 'More than 7', 'Hardly', 'None', '3', 'No']  # Options for each question
fill_google_form(form_link, num_responses, option_choices)
