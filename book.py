from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.common.exceptions as EX
from  selenium.webdriver.support.wait import WebDriverWait
import time
import itertools 
from scrapy.http import HtmlResponse

############## DATA HERE ###############################################
onlyOne = False
zone = "G" 
count = 0
limit = 4
fee = 20
basePrice = 3900
price = str(basePrice+fee)
mode =  "close"
date = "วันเสาร์ที่ 1 กรกฎาคม 2566 18:00"
day = "2"
########################################################################

options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--remote-allow-origins=*")
options.add_argument("--start-maximized")

class Seat:
    def __init__(self, element, zone, seat_number, price):
        self.element = element
        self.zone = zone
        self.seatNo = int(seat_number)
        self.price = price
    def show(self):
        print(self.price, self.seatNo, self.zone)
        
pitsa = "https://www.thaiticketmajor.com/performance/pitsawat-the-musical.html"
wooz = "https://www.thaiticketmajor.com/concert/2023-woodz-world-tour-oo-li-in-bangkok.html"
ft = "https://www.thaiticketmajor.com/concert/2023-ft-island-re-ftisland-in-bangkok.html"


masterStart = time.time()
driver =webdriver.Edge("chromedriver.exe",options = options)
#wait = WebDriverWait(driver, 10)
wait = WebDriverWait(driver, timeout=3, poll_frequency=0.5, ignored_exceptions=[EX.StaleElementReferenceException, EX.ElementNotSelectableException, EX.ElementClickInterceptedException])

#go to website
driver.get(wooz)
time.sleep(0.2)

#login start
driver.find_element(By.XPATH,"/html/body/div[1]/header/div[1]/div/div[3]/div/button").click()
time.sleep(0.2)
driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[2]/div/div[1]/input").send_keys("xperiaz5xl@gmail.com")
driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[2]/div/div[2]/div/input").send_keys("12345620000")
driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div/div/div/div/div/form[1]/div[3]/div/button").click()
#login end



   
def oneDay():
   
    attrix = "btn-red"

    max_retries = 3
    current_retry = 0
    success = False
    start = time.time()
    while current_retry < max_retries and not success:
        try:
            # Find and click on the element
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,attrix)))
            element.click()
            success = True
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException, EX.TimeoutException) as e:
            # Handle the ElementClickInterceptedException
            time.sleep(0.1)
            current_retry += 1
            print(f"Attempt #{current_retry} - {e}")
    end = time.time()
    print("elapse try", end-start, success, current_retry)
    
def moreDay():
    attrix = f"#section-event-round > div > div.event-detail-item > div.box-event-list > div.body > div:nth-child({day}) > div.col-btn > span"
    print("more day -------------------------- <")
    oneDay()
    max_retries = 3
    current_retry = 0
    currentURL = driver.current_url
    increment = 2
 
    while True:
        try:
            # Find and click on the element
            element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,attrix)))
            time.sleep(0.05*increment)
            element.click()
            newURL = driver.current_url
            if newURL != currentURL:
                break
            else:
                print("trying----PLS WAIT", increment)
                increment+=1
        except (EX.StaleElementReferenceException, EX.ElementClickInterceptedException):
            # Handle the ElementClickInterceptedException
            current_retry += 1
            print(f"Attempt #{current_retry} - Element click intercepted. Retrying...") 
#loop through events dates



if onlyOne:
    oneDay()
else:
    moreDay()

#click accept term and condition
accept = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"label-txt")))
accept.click()
driver.find_element(By.ID,"btn_verify").click()

txt = "Sun 02"
driver.find_element(By.XPATH,f"//select[@id='rdId']/option[contains(text(), '{txt}')]").click()
print("OK LA")


driver.find_element(By.XPATH,  f"//*[contains(@href, '#fixed.php#{zone}')]").click()

start = time.time()

seats = driver.find_elements(By.CSS_SELECTOR,f'.seatuncheck[data-seat*="{price}"]')
end = time.time()

print("elapsed time", end - start)
emptySeats = {}

#section-event-round > div > div.event-detail-item > div.box-event-list > div.body > div:nth-child(1)
start = time.time()

for seat in seats:

    seat_value = seat.get_attribute("data-seat").replace("P*","").split("-")
    #emptySeats.append(Seat(seat, seat_value[0], seat_value[1], seat_value[2]))
    if seat_value[0] not in emptySeats:
        emptySeats[seat_value[0]] = []

    emptySeats[seat_value[0]] += [Seat(seat, seat_value[0], seat_value[1], seat_value[2])]

    
    #emptySeats.append(Seat(seat,seat_value[0],seat_value[1],seat_value[2]))
end = time.time()
print("elapsed time --- l ", end - start)


def detectSeq(l, target):
    out = []
    temp = []

    for i in range(1,len(l)):
      if abs(l[i].seatNo - l[i-1].seatNo) == 1:
        temp.append(l[i-1])
      else:
        temp.append(l[i-1])
        if len(temp)>=target:
          out.append(temp)
        temp = []
    return out

def any():
    global count
    print("start any")

    for i in emptySeats:
        i.element.click()
        count +=1
        if count == limit:
            break

def close():
    global count
    f = None
    print("start close")
    start = time.time()
    for key, val in emptySeats.items():
        a = detectSeq(val,limit)
        if len(a) != 0:
            f = a[0]
            print(key,[x.seatNo for x in a[0]])
            
            break
    for i in range(limit):
        f[i].element.click()
        
    end = time.time()
    print("elapsed close", end - start)
    

match mode:
    case "any":
        any()
    case "close":
        close()

masterEnd = time.time()
print("elapse entire run", masterEnd - masterStart)
driver.find_element(By.CSS_SELECTOR,"#booknow").click()

wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_pickup"))).click()
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_mobile"))).click()
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#btn_truemoney"))).click()
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"#truemoney_contact"))).send_keys("0842564963")
