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
from os import getpid
from fake_useragent import UserAgent
configure_logging()

options = Options()
ua = UserAgent()
user_agent = ua.random
options.add_experimental_option("detach", True)
options.add_argument("--remote-allow-origins=*")
#options.add_argument("--headless=new")
#options.add_argument(f'--user-agent={user_agent}')

#options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--start-maximized")
driver =webdriver.Chrome("chromedriver.exe",options = options)
wait = WebDriverWait(driver, timeout=2, poll_frequency=0.1)
waitQuick = WebDriverWait(driver,timeout = 0.5, poll_frequency=0.1)
waitLong = WebDriverWait(driver,timeout = 5, poll_frequency=0.5)

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
    success = False
    #go to website
    start  = time.time()

    driver.get(URL)
    wait.until(EC.url_matches(URL))
    #login start
    while not success:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.main > header > div.container > div > div.mh-col.col-12.col-xl > div > button"))).click()
        logging.info(f"@process {processID} login has started -xx")

        waitLong.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#frm-signin > div.row-form.box-input > div > div:nth-child(1) > input"))).send_keys("peeannop28@outlook.com")
        waitLong.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#frm-signin > div.row-form.box-input > div > div.box-input-item.box-view-password > div > input"))).send_keys("nop2000thai")
        waitLong.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#frm-signin > div:nth-child(3) > div > button"))).click()
        #login end
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.main > header > div.container > div > div.mh-col.col-12.col-xl > div > div.box-member.box-dropdown.item.d-none.d-lg-inline-block > button")))
        except (EX.TimeoutException):
            success = False
        finally:
            success = True
    print("success state: ", success)
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
                if increment > 9:
                    driver.refresh()

        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            driver.refresh()
            current_retry += 1
            logging.info(f"@process {processID}, click_btn_red_DIRECT(), Attempt #{current_retry}: {e}")
    end = time.time()
    logging.info(f"@process {processID}, elapse time --click_btn_red_DIRECT() aka. oneDay() {end-start}")
    print(f"@process {processID} SUCCESS: --click_btn_red_DIRECT() aka. oneDay() elapsed time: {end-start}")


#DESC: click ซื้อบัตร but when the concert has multiple rounds, after clicked, it page will scroll down to the date selection section. will be called by moreDay()
#ARGS: None
#RETURN: None
def click_btn_red_INDIRECT():
    print("click btn-red <->")

    start = time.time()
    attrix = "btn-red"

    current_retry = 0
    increment = 1
    while True:
        try:
            # Find and click on the element
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,attrix)))
            #time.sleep(0.05*increment)
            element.click()
            increment+=1
            break
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException, EX.ElementNotInteractableException) as e:
            # Handle the ElementClickInterceptedException
            driver.refresh()
            current_retry += 1
            logging.info(f"@process {processID}, click_btn_red_INDIRECT() Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --click_btn_red() {end-start}")

#DESC after scrolled down by calling click_btn_red_INDIRECT(), it click the day according to the input. this func is for multiple days concert
#ARGS day: date you want to book in case of multiple days concert
#RETURN None
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
            logging.info(f"@process {processID}, moreDay() Attemp#{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --moreDay() {end-start}")
    print(f"@process {processID} SUCCESS: --moreDay() elapsed time: {end-start}")


#DESC auto detech whether or not the concert has term and condition, click accept T&C if has one
#ARGS None
#RETURN None
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
            logging.info(f"@process {processID}, acceptTerms() Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --acceptTerms() {end-start}")
    print(f"@process {processID} SUCCESS: --acceptTerm() elapsed time: {end-start}")

#DESC use for concerts with queue because after queue is ended, you will be redirected to the seat map view directly 
#without going through concert main page. So, oneDay() or moreDay() can't handle this anymore
#ARGS day: day you want to book
#RETURN None
def clickDropdown(day):
    start = time.time()
    txt = "Sun 02"

    #driver.find_element(By.XPATH,f"//select[@id='rdId']/option[contains(text(), '{txt}')]").click()
    driver.find_element(By.CSS_SELECTOR,f"#rdId > option:nth-child({day})").click()

    end = time.time()
    logging.info(f"@process {processID}, elapse time --clickDropdown() {end-start}")
    print(f"@process {processID} SUCCESS: --clickDropdown() elapsed time: {end-start}")


#DESC
#ARGS
#RETURN
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
            logging.info(f"@process {processID}, findZone() Attempt #{current_retry}: {e}")

    end = time.time()
    logging.info(f"@process {processID}, elapse time --findZone() {end-start}")
    print(f"@process {processID} SUCCESS: --findZone() elapsed time: {end-start}")

#DESC
#ARGS
#RETURN
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

#DESC divide empty seats map into multiple chunks. This only applies to mode="any".
#The intention is to allow multiple processes to work on the same zone, each process will work in its chunk to avoid race condition 
#where more than one process try to book the same seats
#ARGS   seatList: list of available seats
#       segment: number of chunks to split into
#lookAt: a block
#RETURN
def segmentSeat(seatList, limit, zone, lookAt, segment):
    if lookAt is None:
        logging.info(f"@process {processID} Multi-workers will not be used for this zone {zone}")
        print("logging info seat segment1")
        return seatList
    seg = np.array_split(seatList, segment)[lookAt]
    if len(seg) < limit:
        logging.info(f"@process {processID} number of seats in this chunk less than limit")
        print("logging info seat segment2")

        driver.quit()
    return seg

#DESC algorithm for finding continuous block of seats according to the specified number
#ARGS limit: number of seats to book
    #seats: list of available seats
#RETURN a list of consecutive seats
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

#DESC 
#ARGS
#RETURN
def noSeatHandler():
    logging.info(f"@process {processID}, [NO SEAT] No seat or consec seat found, Moving to next zone")
    driver.back()
    driver.refresh()

#DESC click booknow button to proceed to payment page, if success, put signal to message queue to terminate the rest of processes
#ARGS queue: message queue used to communicate with other processes (IPC)
#RETURN return 0: if error or can't reach payment page due alert, 
#       return 1: if successfully put queue and click booknow button
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
#DESC click seat up to specified limit. it handles all interrceptions and alert that might happen during the process.
#If the cilck is intercepted either by alert or popup due to the seats already booked by others, it will keep track of the problematic seats
#and add them to a list of temp[] and tempAll[]. 
#ARGS limit: seat limit
    #seats: list of avaiable seat
    #queue: message queue
#RETURN True: if all seats successfully clicked and payment page is reached
        #tempAll: if javascript is present,
        #temp: if pop up is present
def clickSeat(limit,seats,queue):
    
    temp = [] #use to discard seat in case "seat already taken" pop up is displayed, only this particular seat will be discarded (add to fucked up seat list)
    tempAll = [] #use to batch discard. in case of alert (javascript alert) is present, all clicked seaats will be discarded (add to fucke up seat list)
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
    
#DESC fill name on the ticket, if required only
#ARGS nameList: list of names to fill in
#RETURN None
def fillTicName(nameList):
    for i in range(len(nameList)):
        driver.find_element(By.XPATH,f'//*[@id="txt_firstname_{i}"]').send_keys(nameList[i])
    driver.find_element(By.CSS_SELECTOR,"#btn_regnow").click()


   
#DESC perform payment process including getting OTP. due to user input from terminal is blocked by multiprocessing
#the workaround is to read from .txt file instead. This function will launch a notepad editor, you need to type OTP in.
#ARGS nameList: pass this to fillTicName()
#RETURN True: if successfully completed payment
def afterBook(nameList):
    def getOTP():
        from subprocess import Popen
        file_path = "F:/Work Folder/ticSeleBot/otp.txt"
        with open(file_path, 'w') as file:
                file.write("")
        Popen(["notepad.exe", file_path])
        while True:
            print("waiting for OTP....")
            with open(file_path, 'r') as file:
                content = file.read()
            if content:
                return content.strip()
            else:
                time.sleep(2)

    newURL = driver.current_url      
    
    if "enroll_fixed" in newURL:
        fillTicName(nameList)
        logging.info(f"@process {processID}, fill name completed")
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#checkagree > strong"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#tab-payment > div:nth-child(6) > label > strong"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_pickup"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_mobile"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_truemoney"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#truemoney_contact"))).send_keys("0842564963")
    logging.info(f"@process {processID}, LAST STEP! Wait for OTP")
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_confirm"))).click()
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#otp"))).send_keys(getOTP())
    waitLong.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#payment-process > input"))).click()
    return True
  
    

