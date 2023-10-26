from multiprocessing import Queue, Process
from pipelineLauncher import startS_Booker
import configData
import json
import time

json_path = "F:/Work Folder/ticSeleBot/seatConfig.json"
with open(json_path, "r") as file:
    data = json.load(file)

zone_list = data["zone_list"]

          
if __name__ == "__main__":
    sig_queue = Queue()

    
    for idx,zone in enumerate(zone_list):
        Process(target=startS_Booker, args=(sig_queue,zone,idx,)).start()

    