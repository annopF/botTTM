import book
import time
import configData
import logging
from logging_config import configure_logging
from os import getpid

def startS_Booker(queue, zone, segIdx,segment):
    configure_logging()
    success = False
    json_file_path = "seatConfig.json"
    config = configData.bookingDetail(json_file_path)
    config.initialize()
    config.showConfig()
    #*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*#
    
    def queueAndWaitHandler():
        """ current_time = time.time()
        queueWait = config.queue_time -5 - current_time
        startWait = config.start_time - 10 - current_time """
    
        book.loadAndLogin(config.url)
        print("----------> The program is still running (wait until queue time begin at {}) <----------\n\n".format(config.queueTime))
        config.countdown(config.queue_time)
        
        book.click_btn_red_DIRECT()
        print("----------> queue has been obtained, wait until sales begin at {}".format(config.startTime))
        config.countdown(config.start_time)

        print("----------> YOU ARE IN QUEUE!, wait until your turn")
        logging.info("----------> YOU ARE IN QUEUE!, wait until your turn")
        if book.waitInQueue(json_file_path): #if waitInQueue() returns True, it means the config file has changed, will call config.update() to read the config file again
            config.update()
        print("----------> IT'S YOUR TURN, Booking starts")


        book.acceptTerms()
        book.clickDropdown(config.day)

    def normalBookingHandler():
    
        book.loadAndLogin(config.url) #load URL and login with the given username and password 
        print("----------> The program is still running (wait until target time) <----------\n\n")
        config.countdown(config.start_time)

        if config.oneDay: #if concert has one round, click button directly by calling click_btn_red_DIRECT()
            book.click_btn_red_DIRECT()
        else:
            book.moreDay(config.day) #if concert has multiple rounds, click call moreDay() to handle it properly
        book.acceptTerms() #click accept terms and conditions by calling acceptTerms()

    if config.queue:
        queueAndWaitHandler()
    else:
      

        normalBookingHandler()
        
    fuckedUpSeat = []
    success = False #success flag change to TRUE if the seats are clicked successfully, default=False
    Mstart = time.time()
    book.findZone(zone,config.day)
    while not success: #this while loop keep looping over a zone in case the click fucntion got intercepted by "this seat has been taken" popup
        print("sleeping")
        time.sleep(2)
        seats= book.findAllSeatUnchecked(config.price, fuckedUpSeat)  
        pid = getpid()
        logging.info(f"@process {pid} ----> current zone {zone}, {config.price}")

        if len(seats) < config.limit:
            logging.info(f"@process {pid} NO seat found, KILLING this process immediately")
            book.driver.quit()
            break 
        
        if config.limit == 1 or (config.limit > 1 and config.mode == "any"):
            
            seatStage = book.clickSeat(config.limit, book.segmentSeat(seats,config.limit,zone,segIdx,segment), queue) #CHANGE on Thu 26 OCT
            
            logging.info(f"@process {pid} SEAT stage: {seatStage}")

            if seatStage == True:
                success = True
                logging.info(f"@process {pid} success stage: {success}")
                book.afterBook(config.name_list)
                

                break
            else:
                logging.info(f"@process {pid} problematic seat: {seatStage}")
                fuckedUpSeat.extend(seatStage)
                logging.info(f"@process {pid} fuckedUpSeat: {fuckedUpSeat}")

            
        elif config.limit > 1 and config.mode == "close":
            consecBlock = book.findConsecseats(config.limit, seats) #allocate continuous block of empty seats
            if len(consecBlock) >= config.limit:
                seatStage = book.clickSeat(config.limit, consecBlock, queue)
                print("X ",seatStage)
                logging.info(f"@process {pid} SEAT stage: {seatStage}")
                if seatStage == True: 
                    success = True
                    book.afterBook(config.name_list)

                    break
                else:
                    logging.info(f"@process {pid} problematic seat: {seatStage}")

                    fuckedUpSeat.extend(seatStage)
                    logging.info(f"@process {pid} fuckedUpSeat: {fuckedUpSeat}")
                    print (success)
            else:
                pass
                

    Mend = time.time()

    if success:
        logging.info(f"@process {pid} ------SUCCESS: MAIN LOOP TERMINATED------, TIME TAKEN: {Mend-Mstart}")
        print(f"@process {pid} SUCCESS: BOOKING HAS COMPLETED TIME TAKEN: {Mend-Mstart} ")

    else:
        logging.info(f"@process {pid} ****************** BOOKING WAS UNSUCCESSFUL ******************.")



