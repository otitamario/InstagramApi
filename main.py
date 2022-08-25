from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
from bs4 import BeautifulSoup
from flask import Flask, jsonify,request

# Simple usage with built-in WebDrivers:
options = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
options.add_argument("--disable-gpu")
options.headless = True
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(executable_path="C:\\chromedriver.exe", options=options)
    
app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'name': 'jose',
                    'email': 'jose@dasilva.com'})



@app.route('/api/artist',methods=['GET'])
def artist():
    global driver
    try:
        args = request.args
        artist_id = args.get('id')
        URL_BASE='https://instagram.com/'+str(artist_id)+'/?__a=1'
        try:
            driver.get(URL_BASE)
        except:
            result = {'-1'}
            return result, 201
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        item = soup.find('pre')
        data=json.dumps(item.contents)
        print(data)
        
        return data['graphql']['user']
    except:
        result = {'-1'}
        return result, 201
    finally:
        driver.quit()
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
