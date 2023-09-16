from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.common.exceptions as EX
from  selenium.webdriver.support.wait import WebDriverWait
import time



options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--remote-allow-origins=*")
options.add_argument("--start-maximized")
driver =webdriver.Edge("chromedriver.exe",options = options)
wait = WebDriverWait(driver, timeout=5, poll_frequency=0.5)
waitQueue = WebDriverWait(driver,timeout = 10, poll_frequency=1)

class Seat:
    def __init__(self, element, zone, seat_number, price):
        self.element = element
        self.zone = zone
        self.seatNo = int(seat_number)
        self.price = price
    def show(self):
        print(self.price, self.seatNo, self.zone)
        


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
    print("---->> <<----elapsed time --load+login ", end - start)

def waitInQueue():
    time.sleep(2)
    currentURL = driver.current_url
    print("in queue")
    print("curent url = {}".format(currentURL))
    while True:
        newURL = driver.current_url
        print("new url = {}".format(newURL))
        if currentURL != newURL and "verify" in newURL:
            print("queue ended, booking process starts now")
            return()
        else:
            print("waiting... poll rate = 5sec")

            time.sleep(5)

    
def click_btn_red_DIRECT():
    print("one day <->")

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
            print(f"Attempt #{current_retry} - {e}") 
    end = time.time()
    print("---->> <<----elapsed time --oneDay ", end-start, current_retry)
    
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
            print(f"Attempt #{current_retry} - {e}") 
    end = time.time()
    print("---->> <<----elapsed time --click btn red ", end-start, current_retry)

def moreDay(day):
    print("more day <->")

    start = time.time()

    attrix = f"#section-event-round > div > div.event-detail-item > div.box-event-list > div.body > div:nth-child({day}) > div.col-btn > span"
    click_btn_red_INDIRECT()
    max_retries = 3
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
            print(f"Attempt #{current_retry} - {e}") 
    end = time.time()
    print("---->> <<----elapsed time --moreDay ", end - start, current_retry)


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
            print(f"Attempt #{current_retry} - {e}")
    
    end = time.time()
    print("---->> <<----elapsed time --accept terms ", end - start)


def clickDropdown(day):
    start = time.time()
    txt = "Sun 02"

    #driver.find_element(By.XPATH,f"//select[@id='rdId']/option[contains(text(), '{txt}')]").click()
    driver.find_element(By.CSS_SELECTOR,f"#rdId > option:nth-child({day+1})").click()

    end = time.time()
    print("---->> <<----elapsed time --click dropdown ", end - start)

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
            print(f"Attempt #{current_retry} - {e}") 
    end = time.time()
    print("---->> <<----elapsed time --find zone ", end - start)

def findAllSeatUnchecked(price):
    start = time.time()
    seats = driver.find_elements(By.CSS_SELECTOR,f'.seatuncheck[data-seat*="{price}"]')
    end = time.time()
    
    print("---->> <<----elapsed time --find all .seatuncheck", end - start)
    return seats


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
    print("---->> <<----elapsed time --find consecutive seats", end - start)
    print("_------- OUT")
    print(temp)

    return temp

def noSeatHandler():
    driver.back()
    driver.refresh()

def clickSeat(limit,seats):
    print("--len seat",len(seats))
    
    print("start clickSeat")
    start = time.time()
    for i in range(limit):
        time.sleep(0.2)
        try:
            seats[i].click()

            print("-->",seats[i].get_attribute("data-seat"))
        except EX.ElementClickInterceptedException:
            driver.find_element(By.CSS_SELECTOR,"body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > a").click()
            driver.refresh()
            print("one or more seats unavailable, calling noSeatHandler()")

            return(False)
    end = time.time()
    print("---->> <<----elapsed time --click seat", end - start)
    return(True)

def fillTicName(nameList):
    for i in range(len(nameList)):
        driver.find_element(By.XPATH,f'//*[@id="txt_firstname_{i}"]').send_keys(nameList[i])
    driver.find_element(By.CSS_SELECTOR,"#btn_regnow").click()


def completeBooking(confirm, nameList):
    try:
        driver.find_element(By.CSS_SELECTOR,"#booknow").click()
    except EX.UnexpectedAlertPresentException:

        driver.switch_to().alert().accept()
        driver.refresh()
        return False
    except EX.ElementClickInterceptedException:
        driver.find_element(By.CSS_SELECTOR,"body > div.fancybox-overlay.fancybox-overlay-fixed > div > div > a").click()
        driver.refresh()
        return False

    if confirm:
        fillTicName(nameList)
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_pickup"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_mobile"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_truemoney"))).click()
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#truemoney_contact"))).send_keys("0842564963")
    time.sleep(0.5)

    

def tst():
    driver.find_element(By.CSS_SELECTOR,"#booknow").click()





