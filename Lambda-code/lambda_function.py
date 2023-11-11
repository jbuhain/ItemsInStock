from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = '/opt/headless-chromium/headless-chromium'
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--single-process')
options.add_argument('--disable-dev-shm-usage')
custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
options.add_argument(f"--user-agent={custom_user_agent}")
    

def lambda_handler(event, context):
    
    try:
    
        driver = webdriver.Chrome('/opt/chromedriver/chromedriver',chrome_options=options)
        driver.get("https://www.uniqlo.com/us/en/products/E459574-000/00?colorDisplayCode=95&sizeDisplayCode=027")
        # returns dynamically rendered HTML
        current_html = driver.page_source
        title = driver.title
        
        driver.quit();
        
        if "add to cart" in current_html.lower():
            result = "The product is in stock."
        else:
            result = "The product is not in stock."
    
        response = {
            "statusCode": 200,
            "body": title + " : " + result
        }

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        response = {
            'statusCode': 500,
            'body': error_message
        }   

        
    return response