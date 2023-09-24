from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.common.exceptions as EX
from  selenium.webdriver.support.wait import WebDriverWait
import time
import json
import datetime
import numpy as np
""" options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--remote-allow-origins=*")
options.add_argument("--start-maximized")
driver =webdriver.Edge("chromedriver.exe",options = options)


driver.get("https://www.w3schools.com/js/tryit.asp?filename=tryjs_alert")
time.sleep(2)
driver.refresh()
time.sleep(3)
driver.find_element(By.CSS_SELECTOR,"body > button").click() """



def remove_elements_method1(A, toRemove):
    start_time = time.time()
    result = [x for x in A if x not in toRemove]
    end_time = time.time()
    return result, end_time - start_time

def remove_elements_method2(A, toRemove):
    start_time = time.time()
    result = []
    fid = []
    for idx,x in enumerate(A):
        if x in toRemove:
          fid.append(idx)
        if len(fid) == len(toRemove):
          break
    end_time = time.time()
    
    return (np.delete(A, toRemove)).tolist(), end_time - start_time

A = [x for x in range(100000000)]
toRemove = [1, 4, 5]

result_method1, time_method1 = remove_elements_method1(A, toRemove)
result_method2, time_method2 = remove_elements_method2(A, toRemove)

#print("Method 1 Result:", result_method1)
print("Method 1 Time Taken:", time_method1)

#print("Method 2 Result:", result_method2)
print("Method 2 Time Taken:", time_method2)