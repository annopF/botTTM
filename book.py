from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.common.exceptions as EX
from  selenium.webdriver.support.wait import WebDriverWait
import time
import numpy as np
import logging
from logging_config import configure_logging
from random import randint
from os import getpid

configure_logging()

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--remote-allow-origins=*")
options.add_argument("--start-maximized")
driver =webdriver.Chrome("chromedriver.exe",options = options)
wait = WebDriverWait(driver, timeout=2, poll_frequency=0.1)
waitQuick = WebDriverWait(driver,timeout = 0.5, poll_frequency=0.1)
processID = getpid()
class Seat:
    def __init__(self, element, zone, seat_number, price):
        self.element = element
        self.zone = zone
        self.seatNo = int(seat_number)
        self.price = price
    def show(self):
        print(self.price, self.seatNo, self.zone)
               

def killYourSelf():
    driver.quit()

def loadAndLogin(URL):
    
    #wait = WebDriverWait(driver, timeout=2, poll_frequency=0.5, ignored_exceptions=[EX.StaleElementReferenceException, EX.ElementNotSelectableException, EX.ElementClickInterceptedException])

    #go to website
    start  = time.time()

    driver.get(URL)
    wait.until(EC.url_matches(URL))
    #login start
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/header/div[1]/div/div[3]/div/button"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[2]/div/div[1]/input"))).send_keys("peeannop28@outlook.com")
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[2]/div/div[2]/div/input"))).send_keys("nop2000thai")
    wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[3]/div/button"))).click()
   
    #login end
    end = time.time()
    logging.info(f"@process {processID}, elapsed time --load+login {end-start}")
    print(f"@process {processID} SUCCESS: --load+login() elapsed time: {end-start}")

#DESC: monitor for file change by comparing hash of files
#ARGS: accept path to file
#RETURN: hash value of file
def monitorConfigChange(path):
    with open(path,"rb") as file:
        content = file.read()
        return(hash(content))

#DESC: wait in queue until URL change to term and condition page
#it also monitor for file change after each wait
#ARGS: path to a file to be monitored
#RETURN: True if file changed, False otherwise
def waitInQueue(path):
    time.sleep(2)
    change = False
    currentHash = monitorConfigChange(path)
    currentURL = driver.current_url
    print("in queue")
    print("curent url = {}".format(currentURL))
    while True:
        newURL = driver.current_url
        print("new url = {}".format(newURL))
        if currentURL != newURL and "verify" in newURL:
            print("queue ended, booking process starts now")
            return(change)
        elif "ขณะนี้ถึงคิวของคุณ" in driver.page_source:
            print("[CRITICAL] waiting... poll rate = 0.5sec")
            time.sleep(0.5)
        else:
            print("[NORMAL] waiting... poll rate = 5sec")

            time.sleep(5)
            newHash = monitorConfigChange(path)
            if currentHash != newHash:
                change = True


#DESC: click รับบัตรคิว OR ซื้อบัตร depending on the concert, but both use the same locator
# it keep trying until successfully clicked
#ARGS: None
#RETURN: None
def click_btn_red_DIRECT():

    start = time.time()
    attrix = "btn-red"

    current_retry = 0
    currentURL = driver.current_url
    increment = 1
    while True:
        try:
            # Find and click on the element
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,attrix)))
            #time.sleep(0.05*increment)
            element.click()
            newURL = driver.current_url
            if newURL != currentURL:
                break
            else:
                print("trying----PLS WAIT", increment)
                increment+=1
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            current_retry += 1
            logging.info(f"@process {processID}, Attempt #{current_retry}: {e}")
    end = time.time()
    logging.info(f"@process {processID}, elapse time --oneDay() {end-start}")
    print(f"@process {processID} SUCCESS: --oneDay() elapsed time: {end-start}")


#DESC: click ซื้อบัตร but when the concert has multiple rounds. This function is used when the concert has no queue
#ARGS: accept path to file
#RETURN: hash value of file
def click_btn_red_INDIRECT():
    print("click btn-red <->")

    start = time.time()
    attrix = "btn-red"

    current_retry = 0
    increment = 1
    while True:
        try:
            # Find and click on the element
            element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,attrix)))
            #time.sleep(0.05*increment)
            element.click()
            increment+=1
            break
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            current_retry += 1
            logging.info(f"@process {processID}, Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --click_btn_red() {end-start}")


def moreDay(day):
    print("more day <->")

    start = time.time()

    attrix = f"#section-event-round > div > div.event-detail-item > div.box-event-list > div.body > div:nth-child({day}) > div.col-btn > span"
    click_btn_red_INDIRECT()
    current_retry = 0
    currentURL = driver.current_url
    increment = 1
 
    while True:
        try:
            # Find and click on the element
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,attrix)))
            #time.sleep(0.05*increment)
            element.click()
            newURL = driver.current_url
            if newURL != currentURL:
                break
            else:
                print("trying----PLS WAIT", increment)
                increment+=1
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            current_retry += 1
            logging.info(f"Attemp#{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --moreDay() {end-start}")
    print(f"@process {processID} SUCCESS: --moreDay() elapsed time: {end-start}")


#click accept term and condition
def acceptTerms():
    start = time.time()
    current_retry = 0
    currentURL = driver.current_url
    increment = 2
    if "verify" not in currentURL:
        return()
    while True:

        try:
            # Find and click on the element
            accept = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"label-txt")))
            accept.click()
            driver.find_element(By.ID,"btn_verify").click()            
            #time.sleep(0.05*increment)
            newURL = driver.current_url
            if newURL != currentURL:
                break
            else:
                print("trying----PLS WAIT", increment)
                increment+=1
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            current_retry += 1
            logging.info(f"@process {processID}, Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --acceptTerms() {end-start}")
    print(f"@process {processID} SUCCESS: --acceptTerm() elapsed time: {end-start}")


def clickDropdown(day):
    start = time.time()
    txt = "Sun 02"

    #driver.find_element(By.XPATH,f"//select[@id='rdId']/option[contains(text(), '{txt}')]").click()
    driver.find_element(By.CSS_SELECTOR,f"#rdId > option:nth-child({day})").click()

    end = time.time()
    logging.info(f"@process {processID}, elapse time --clickDropdown() {end-start}")
    print(f"@process {processID} SUCCESS: --clickDropdown() elapsed time: {end-start}")


def findZone(zone):
    start = time.time()

    current_retry = 0
    currentURL = driver.current_url
    increment = 1
 
    while True:
        try:
            # Find and click on the element

            element = wait.until(EC.visibility_of_element_located((By.XPATH,  f"//*[contains(@href, '#fixed.php#{zone}')]")))
            #time.sleep(0.05*increment)
            element.click()
            newURL = driver.current_url
            if newURL != currentURL:
                break
            else:
                print("trying----PLS WAIT", increment)
                increment+=1
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            current_retry += 1
            logging.info(f"@process {processID}, Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --findZone() {end-start}")
    print(f"@process {processID} SUCCESS: --findZone() elapsed time: {end-start}")

def findAllSeatUnchecked(price, notAvailable):
    def remove_elements_method2(A, toRemove):
        fid = []
        #print("toRemove ", toRemove)
        if len(toRemove) == 0:
            return A
        for idx,x in enumerate(A):
            #print("88888----> ", x.get_attribute("data-seat"))
            if x.get_attribute("data-seat") in toRemove:
                fid.append(idx)
            if (len(fid) == len(toRemove)):
                break
        #print(fid)
        return (np.delete(A, fid)).tolist()
    
    start = time.time()
    seats = driver.find_elements(By.CSS_SELECTOR,f'.seatuncheck[data-seat*="{price}"]')
    
    end = time.time()

    logging.info(f"@process {processID}, elapse time --findAllSeatUnchecked() {end-start} len={len(seats)}")
    print(f"@process {processID} SUCCESS: --findAllSeatUnchecked() elapsed time: {end-start}")

    return remove_elements_method2(seats,notAvailable)

def segmentSeat(seatList, segment, lookAt):
    return np.array_split(seatList, segment)[lookAt]

    
def findConsecseats(limit,seats):
    start = time.time()
    ##working for real tested 
    temp = []
    for i in range(len(seats)):
        curr = seats[i].get_attribute("data-seat").replace("P*","").split("-")
        prev = seats[i-1].get_attribute("data-seat").replace("P*","").split("-")
        if len(temp) == 0 or abs(int(curr[1]) - int(prev[1])) == 1 and curr[0] == prev[0]:
            temp.append(seats[i])

            if len(temp) >= limit:
                break
        else:
            temp = [seats[i]]



    end = time.time()
    logging.info(f"elapse time --findConsecseats() {end-start}, @process {processID}")
    print(f"@process {processID} SUCCESS: --findConsecseats() elapsed time: {end-start}")

    return temp

def noSeatHandler():
    logging.info(f"@process {processID}, [NO SEAT] No seat or consec seat found, Moving to next zone")
    driver.back()
    driver.refresh()

def complete(queue):
        currentURL = driver.current_url
            
        driver.find_element(By.CSS_SELECTOR,"#booknow").click()
        try:
            newURL = driver.current_url

            if newURL == currentURL:
                print("nefw driver equal")
                driver.refresh()
                print("click book now intercepted by alert v")
                return(0)
        except EX.UnexpectedAlertPresentException:
            logging.info(f"@process {processID}, click book now intercepted by alert")
            print(f"@process {processID} FAIL: RECOVERING...")

            return(0)
        if "enroll_fixed" or "payment" in newURL:
            if queue.empty():
                queue.put("fuck yeah!")
                logging.info(f"@process {processID}, This process is the Winner")
                print(f"@process {processID} SUCCESS: This process is the winner")

                
            else:
                logging.info(f"@process {processID}, Killing this process immediately...")
                print(f"@process {processID} TERMINATED NOW")

                driver.quit()
                exit(0)
        return(1)

def clickSeat(limit,seats,queue):
    
    temp = []
    tempAll = []
    start = time.time()
    p = None
    for i in range(limit):
        try:
            seats[i].click()
            p = seats[i].get_attribute("data-seat")
            tempAll.append(p)
            logging.info(f"@process {processID}, -->{p}")
            time.sleep(0.05)
            if i+1 == len(seats):
                try:
                    waitQuick.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > a"))).click()
                    logging.info(f"@process {processID}, !! last seat already taken {p}")
                    print(f"@process {processID} FAIL: RECOVERING...")

                    temp.append(p)
                except (EX.NoSuchElementException, EX.TimeoutException):
                    pass
        except (EX.ElementClickInterceptedException, EX.UnexpectedAlertPresentException):
            waitQuick.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > a"))).click()
            logging.info(f"@process {processID}, !! seat already taken {p}")
            print(f"@process {processID} FAIL: RECOVERING...")


            temp.append(p)
            print("appendeed ", temp)

    if len(temp) != 0:
        logging.info(f"@process {processID}, [CLICK FAILED] encountered seat already taken popup {temp} ")
        print(f"@process {processID} FAIL: RECOVERING...")

        driver.refresh()
        return(temp)
    if complete(queue):
        end = time.time()  
        logging.info(f"@process {processID}, elapsed time --clickSeat() {end-start} ")
        print(f"@process {processID} SUCCESS: --clickSeat() {end-start}")

        return(True)
    logging.info(f"@process {processID}, [CLICK FAILED] ALERT is present {tempAll} ")
    print(f"@process {processID} FAIL: RECOVERING...")

    return(tempAll)
    #logging.info(f"elapse time --clickSeat() {end-start}, len seat={len(seats)}")
    

def fillTicName(nameList):
    for i in range(len(nameList)):
        driver.find_element(By.XPATH,f'//*[@id="txt_firstname_{i}"]').send_keys(nameList[i])
    driver.find_element(By.CSS_SELECTOR,"#btn_regnow").click()


   

def afterBook(nameList):
    newURL = driver.current_url      
    
    if "enroll_fixed" in newURL:
        fillTicName(nameList)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_pickup"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_mobile"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_truemoney"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#truemoney_contact"))).send_keys("0842564963")
    time.sleep(0.5)
    logging.info(f"@process {processID}, fill name completed")
    return True
  
    

