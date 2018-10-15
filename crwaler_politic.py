from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import mysql.connector
from time import sleep

try:
    cnx = mysql.connector.connect(user='root', password='wireless', host='127.0.0.1', database='hanaduri', charset='utf8mb4', use_unicode=True)
    cursor = cnx.cursor()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
try:    
    driver = webdriver.Chrome('/home/trading/Downloads/chromedriver')

    #Link delete
    prev_addr = ""
    next_addr = ""

    #page loop
    for i in range(85, 0, -1):
        end_page_num = i
        full_addr = prev_addr + str(end_page_num) + next_addr
        print(full_addr)

        while True:
            try:
                driver.get(full_addr)
                ct_list1 = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".petition_list > li:nth-child(1) > div:nth-child(1) > div:nth-child(3) > a:nth-child(1)")))
                break
            except:
                sleep(5)
        ct_list1 = driver.find_element_by_class_name('ct_list1')
        bl_body = ct_list1.find_element_by_class_name('bl_body')
        petition_list = bl_body.find_element_by_class_name('petition_list')
        lis = petition_list.find_elements_by_tag_name('li')

        page_handle = driver.current_window_handle
        for li in lis:
            no = li.find_element_by_class_name('bl_no').get_attribute('innerHTML')
            no = int(no[no.rfind('>')+1:])

            category = li.find_element_by_css_selector('div > .bl_category').get_attribute('innerHTML')
            category = category[category.rfind('>')+1:]

            query = "SELECT * FROM president WHERE no=%s and category=%s"
            cursor.execute(query, (no, category))
            cursor.fetchall()
            if cursor.rowcount > 0:
                print(no, ' pass')
                continue
            
            li.find_element_by_tag_name('a').send_keys(Keys.CONTROL + Keys.RETURN)
            driver.implicitly_wait(2)
            driver.switch_to_window(driver.window_handles[1])
            driver.implicitly_wait(2)

            while True:
                try:
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "petitionsView_title")))
                    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, "View_write")))
                    break
                except:
                    sleep(3)
            
            title = driver.find_element_by_class_name('petitionsView_title').get_attribute('innerHTML')
            body = driver.find_element_by_class_name('View_write').get_attribute('innerHTML')

            print('title : ', title)
            print('category : ', category)

            add_writing = "INSERT INTO president VALUES (%s, %s, %s, %s)"
            data = (no, category, title, body)
            cursor.execute(add_writing, data)
            cnx.commit()

            sleep(6)
            driver.close()
            driver.switch_to_window(page_handle)

finally:
    driver.close()
    cnx.close()
