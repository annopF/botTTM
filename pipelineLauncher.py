import book
import time
import datetime

################################ CONFIG DATA HERE ################################

queue = False  #concert has queue before booking
oneDay = True #concert has only one round
day = "1" #day you want to book
zone_list = ["A1","A2","B2"] #zone you want to book
startTime = {"YEAR": 2023, "MONTH": 8, "DAY": 17, "HOUR": 22, "MINUTE":31}
queueTime = {"YEAR": 2023, "MONTH": 6, "DAY": 17, "HOUR": 21, "MINUTE":58}
ticketPrice = 5500 #price you want to book
fee = 20 #ticket fee
limit = 4 #no. of tickets to purchase   
mode =  "any" #required only when limit > 1, close = continuous seats, any = any seats
name_list = ["john1","john2"]

tst = "https://www.thaiticketmajor.com/concert/2023-kim-bum-asia-fan-meeting-in-bangkok.html"
url = tst
################################ CONFIG END HERE ################################
temp = [val for key, val in startTime.items()]
temp.extend([0,0,0,0])
target_time = time.mktime(tuple(temp)) #format: (Year, Month, Day, Hour, Minute)

tempQ = [val for key, val in queueTime.items()]
tempQ.extend([0,0,0,0])
queue_time = time.mktime(tuple(tempQ))
price = str(ticketPrice+fee)
failCounter = 0 #count how many times program encouter "seat already taken popup", --> must refetch seat map again
success = False
#*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*#
def queueAndWaitHandler():
    current_time = time.time()
    queueWait = queue_time -5 - current_time
    startWait = target_time - 10 - current_time
    print("\n\n-------<<< CONFIRM BOOKING DETAIL >>>-------\n\nConcert: {}\nHas Queue: {}\nOnly One Day: {}\nChosen Day: {}\nZone: {}\nBooking Start: {}\nTicket Price: {}\nNo.of Tickets: {}\nMultiple Ticket Mode: {}\n--------------------------------------------"
        .format(url,queue,oneDay,day,zone_list,startTime,ticketPrice,limit,mode))
    
    book.loadAndLogin(url)
    print("----------> The program is still running (wait until target time) <----------\n\n")

    time.sleep(queue_time)
    
    book.click_btn_red_DIRECT()
    print("----------> YOU ARE IN QUEUE!, wait until your turn")
    book.waitInQueue()
    book.acceptTerms()
    book.clickDropdown(day)

if queue:
    queueAndWaitHandler()
else:
    #current_time = time.time()
    #startWait = target_time - 10 - current_time
    print("----------> The program is still running (wait until target time) <----------\n\n")
    book.loadAndLogin(url)
    #time.sleep(startWait)

    if oneDay:
        book.click_btn_red_DIRECT()
    else:
        book.moreDay(day)

    book.acceptTerms()

for zone in zone_list:
    book.findZone(zone)
    seats = book.findAllSeatUnchecked(price)
    print("len seat:--=", len(seats))
    if len(seats) == 0:
        book.noSeatHandler()
        print("NO seat found, moving to next zone")
        break

    else:  
        if limit == 1:
            click = book.clickSeat(limit, seats)
            print(click)
            if click:
                success = True
                break
        elif limit > 1 and mode == "any":
            click = book.clickSeat(limit, seats)
            print(click)
            break
        elif limit > 1 and mode == "close":
            consecBlock = book.findConsecseats(limit,seats)
            if len(consecBlock) >= limit:
                book.clickSeat(limit,consecBlock)
                break

            else:
                book.noSeatHandler()
                print("NO consec block found, moving to next zone")

