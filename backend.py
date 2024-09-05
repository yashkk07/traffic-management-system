'''
Requirements

'''

from time import sleep
import json
import math
from pro import process
from nightvideo import process_video as pv
from nightvideo import process_frame
import subprocess

min_time = 10
threshold_time = 60

buffer = [0,0,0,0] #clear buffer when i is 0

def floor5(time):
    return ((time-3)//5)*5

def send_data(SigG, SigO,time,signal):
    json_dict = {"green" : SigG, "orange": SigO  ,"time" : time, "signal" : signal}
    json_string = json.dumps(json_dict, separators=(",", ":"))
    with open('C:/Users/sharv/Downloads/jsx/jsx/sih/src/data.json', 'w') as json_file:
        json_file.write(json_string)

def calc(volume):
    print("For volume : ",volume)
    '''calculating the amt of time required for the current signal using some ratio'''
    if (volume <= 25):
        return volume*2+5
    return 65

def occupy_buffy(signal_id,time):
    '''occupies the buffer for signals except self based on the current time given'''
    for i in range(4):
        if i!=signal_id:
            buffer[i] += (60-time)/3 #+=?
        else:
            buffer[i]=0

volume = [10,50,15,3]

def cycle():
    '''main function for each cycle'''
    for signal in range(4):
        #function from cv that gives volume for each image
        volume = process(f"images/{signal+1}.png",f"images/{signal+1}imask.png")
        # test = int(calc(volume[signal])) #for testing purposes
        test = int(calc(volume))
        variable_time = max(10,test)
        if(variable_time>60):
            time = floor5(variable_time+buffer[signal])
        else:
            time = floor5(variable_time)
        sigArrG = [-1] * 4
        sigArrO = [-1]*4
        sigArrG[signal] = 0
        sigArrO[signal] = 1
        send_data(sigArrG,sigArrO,time,signal) #send data to web server
        occupy_buffy(signal,variable_time)
        time = max(10,int(time))
        print(f"Signal: {signal} - Time allocated : {time}")
        sleep(10)

while(True):
    cycle()
pv()
#uwu
