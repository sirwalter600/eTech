import os
from ftplib import FTP
import mysql.connector
import serial, time
import datetime
import csv
import board
import busio
import subprocess
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import requests
from config import *

######################################################################


i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan0 = AnalogIn(ads, ADS.P0)
chan1 = AnalogIn(ads, ADS.P1)
chan2 = AnalogIn(ads, ADS.P2)
chan3 = AnalogIn(ads, ADS.P3)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
led_pin1 = 17 # blue
led_pin2 = 18 # green
led_pin3 = 27 # red
GPIO.setup(led_pin1, GPIO.OUT)
GPIO.setup(led_pin2, GPIO.OUT)
GPIO.setup(led_pin3, GPIO.OUT)
led_pwm1 = GPIO.PWM(led_pin1, 100)
led_pwm2 = GPIO.PWM(led_pin2, 100)
led_pwm3 = GPIO.PWM(led_pin3, 100)

########################################################################

Plant_ID = Device_ID
port1 = '/dev/rfcomm0'
port2 = '/dev/ttyUSB2'
port3 = '/dev/ttyUSB1'
port4 = '/dev/ttyACM0' #Navilock
GPS_device = "NA"


#########################################################################

SampFreq = 9 # sample frequency (seconds)

#########################################################################

os.system("sudo sh /home/pi/HDS/HDS_startup.sh") # BT and 3G setup

#########################################################################

if mode =='paver':
	# 3 white flashes
	led_pwm1.start(70)
	led_pwm2.start(70)
	led_pwm3.start(70)
	time.sleep(0.1)
	led_pwm1.start(0)
	led_pwm2.start(0)
	led_pwm3.start(0)
	time.sleep(0.2)
	led_pwm1.start(70)
	led_pwm2.start(70)
	led_pwm3.start(70)
	time.sleep(0.1)
	led_pwm1.start(0)
	led_pwm2.start(0)
	led_pwm3.start(0)
	time.sleep(0.2)
	led_pwm1.start(70)
	led_pwm2.start(70)
	led_pwm3.start(70)
	time.sleep(0.1)
	led_pwm1.start(0)
	led_pwm2.start(0)
	led_pwm3.start(0)

##########################################################################

path = "/home/pi/HDS/log/"
for file in os.listdir(path):
        fullpath   = os.path.join(path,file)    # turns 'file1.txt' into '/path/to/file1.txt'
        timestamp  = os.stat(fullpath).st_ctime # get timestamp of file
        createtime = datetime.datetime.fromtimestamp(timestamp)
        now        = datetime.datetime.now()
        delta      = now - createtime
        #print(delta)
        if delta.days > 30:

                os.remove(fullpath)
                print("deleted old file")

                
######################################################################

def internet_test():
        try:
                address = "8.8.8.8"
                res = subprocess.call(["ping", "-c", "3", address])
                #print(res)
                if res == 0:
                        print("Internet ping ok")
                elif res == 2:
                        print("Internet no response")
                        # 4 red flashes
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        
                        closePPPD()
                        time.sleep(1)
                        openPPPD()
                else:
                        print("Internet ping failed")
                        # 4 red flashes
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        
                        closePPPD()
                        time.sleep(1)
                        openPPPD()

        except Exception:
                print("No Internet")
                
######################################################################

def activateGPS():
        GPSser2=serial.Serial(port2, 115200, timeout=1, rtscts=True, dsrdtr=True)
        GPSser2.write("AT+QGPS=1\r".encode())
        GPSser2.write('AT+QGPSCFG="gpsnmeatype",1\r'.encode())
        GPSser2.close()

                
#########################################################################


                
#########################################################################

# Start PPPD
def openPPPD():
        subprocess.call("sudo pon fona", shell=True)
        time.sleep(3)


# Stop PPPD
def closePPPD():
        subprocess.call("sudo poff fona", shell=True)
        time.sleep(1)


######################################################################### 

LatDec = ""
LonDec = ""
Height = ""
PDOP = ""

while 1:
               
        loopNum = 1
        GPS_device = "NA"
        activateGPS()
        try:

                #time.sleep(5)
                try:
                        mydb = mysql.connector.connect(
                        host="79.170.44.107",
                        user="cl25-ecube",
                        passwd="4fs/RD6Ky",
                        database="cl25-ecube"
                        )
                except Exception:
                        print("Cannot connect to MySQL DB")
                        
                mycursor = mydb.cursor()
                mycursor.execute("SELECT ID FROM system_data order by ID Desc limit 1")
                myresult = mycursor.fetchone()
                ID = myresult[0]
                #ID = str(ID)
                print("SQL ID = ", ID)
        except Exception:
                print("cannot get mySQL ID")
                ID = 0

        
        #w_lat = "51.900"
        #w_lon = "-1.911"
        w_lat = LatDec
        w_lon = LonDec
        if (w_lat != ""):
                coords = w_lat + "," + w_lon
                params = {
                  'access_key': 'f977d507524422fd7dc9f0cf7a094280',
                  'query': coords
                }

                api_result = requests.get('https://api.weatherstack.com/current', params)
                api_response = api_result.json()

                temperature = api_response['current']['temperature']
                wind_speed = api_response['current']['wind_speed']
                precip = api_response['current']['precip']
        else:
                temperature = ""
                wind_speed = ""
                precip = ""

        print('temp: ', temperature)
        print('wind: ', wind_speed)
        print('rain: ' ,precip)

###########################################################################################
        
        while loopNum <= 12:

                time.sleep(SampFreq)
                ID += 1
		
                ts = time.time()
                st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                dst = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                tst = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                
                #temp1 = round(chan0.voltage,3)*100
                #temp2 = round(chan1.voltage,3)*100
                temp1 = round((chan0.voltage*100),1)
                temp2 = round((chan1.voltage*100),1)
                sensor3 = "0" # NOT USED
                sensor4 = "0" # NOT USED
                # 1 green flash
                led_pwm2.start(40)
                time.sleep(0.2)
                led_pwm2.start(0)
                time.sleep(0.1)
                
	#########################################################################
                LatDec = ""
                LonDec = ""
                Height = ""
                PDOP = ""
                try:
                        GPSser=serial.Serial(port4, 115200, timeout=2, rtscts=True, dsrdtr=True)
                        GPSser.readline()
                        response = GPSser.readline()
                        #print(response.decode())
                        if "$GNGGA" in str(response):
                                data2 = response.decode().split(",")

                                if data2[6] == "0":
                                        print("No satellite coverege")
                                        # 1 red flash
                                        led_pwm3.start(70)
                                        time.sleep(0.2)
                                        led_pwm3.start(0)
                                        #LatDec = "51.500"
                                        #LonDec = "-1.950"
                                        
                                else:        
                                        latDD = int(float(data2[2])/100)
                                        latSS = float(data2[2]) - latDD * 100
                                        LatDec = latDD + latSS / 60
                                        LatDec = round(LatDec, 8)
                                        #print (LatDec)
                                        if data2[3] == "S":
                                                LatDec = (LatDec * -1)
                                        LatDec = str(LatDec)

                                        lonDD = int(float(data2[4])/100)
                                        lonSS = float(data2[4]) - lonDD * 100
                                        LonDec = lonDD + lonSS / 60
                                        LonDec = round(LonDec, 8)
                                        #print (LonDec)
                                        if data2[5] == "W":
                                                LonDec = (LonDec * -1)
                                        LonDec = str(LonDec)

                                        PDOP = str(data2[8])
                                        Height = str(data2[9])
                                        GPS_device = "NAVI"
                                        # 1 blue flash
                                        led_pwm1.start(50)
                                        time.sleep(0.2)
                                        led_pwm1.start(0)
                                
                        else:
                                LatDec = ""
                                LonDec = ""
                                Height = ""
                                PDOP = ""
                        GPSser.close()

                except Exception:
                        print("cannot get GPS serial data")
                        #LatDec = ""
                        #LonDec = ""
                        #PDOP = ""
                        #print ("lat2 = ", LatDec)
                        #print ("lon2 = ", LonDec)
        ###########################################################################
                        
	###########################################################################    

                logfile = ("/home/pi/HDS/log/" + Plant_ID + "_log_" + dst + ".csv")
                #os.chmod(logfile, 0o777)
                csvlog = open (logfile, "a")
                csvlog.write(str(ID) + "," + Plant_ID + "," + mode + "," + dst + "," + tst + "," + LatDec + "," + LonDec + "," + str(Height) + "," + GPS_device + "," + str(PDOP) + "," + str(temp1) + "," + str(temp2) + "," + sensor3 + "," + sensor4 + "," + st + "," + str(temperature) + "," + str(wind_speed) + "," + str(precip) + "\n")
                csvlog.close()

                logfile = ("/home/pi/HDS/log/temp1.csv")
                #os.chmod(logfile, 0o777)
                csvlog = open (logfile, "a")
                csvlog.write(str(ID) + "," + Plant_ID + "," + mode + "," + dst + "," + tst + "," + LatDec + "," + LonDec + "," + str(Height) + "," + GPS_device + "," + str(PDOP) + "," + str(temp1) + "," + str(temp2) + "," + sensor3 + "," + sensor4 + "," + st + "," + str(temperature) + "," + str(wind_speed) + "," + str(precip) + "\n")
                csvlog.close()
		
	###########################################################################

                print("Data collected: ", loopNum)
                loopNum +=1
				
	###########################################################################

        #close GPS and open GPRS
        #GPSser.close()
        #openPPPD()
        
        ###########################################################################                

        with open('/home/pi/HDS/log/temp1.csv') as data_csv:
                rows = csv.reader(data_csv, delimiter=',')
                inputVal = ""
                try:
                        
                        for row in rows:
                                #print(row)
                                ID = row[0]
                                Plant_ID = row[1]
                                mode = row[2]
                                dst = row[3]
                                tst = row[4]
                                LatDec = row[5]
                                LonDec = row[6]
                                Height = row[7]
                                GPS_device = row[8]
                                PDOP = row[9]
                                temp1 = row[10]
                                temp2 = row[11]
                                sensor3 = row[12]
                                sensor4 = row[13]
                                st = row[14]
                                temp = row[15]
                                wind = row[16]
                                rain = row[17]
                                #print (ID, Plant_ID, dst, tst, LatDec, LonDec, Height, GPS_device, PDOP, temp1, temp2)

                                inputVal = inputVal + "('" + ID + "','" + Plant_ID + "','" + mode + "','" + dst + "','" + tst + "','" + LatDec + "','" + LonDec + "','" + Height + "','" + GPS_device + "','" + PDOP + "','" + temp1 + "','" + temp2 + "','" + sensor3 + "','" + sensor4 + "','" + st + "','" + temp + "','" + wind + "','" + rain + "'),"
                        inputVal = inputVal[:-1]
                        #print(inputVal)
                                
                        try:
                                mydb = mysql.connector.connect(
                                host="79.170.44.107",
                                user="cl25-ecube",
                                passwd="4fs/RD6Ky",
                                database="cl25-ecube"
                                )
                                
                                sql = "INSERT INTO system_data (ID, DeviceID, mode, Date, Time, Latitude, Longitude, Height, GPS_device, PDOP, Sensor1, Sensor2, Sensor3, Sensor4, Date_Time, Ambient_temp, Wind_speed, Rainfall) VALUES " + inputVal
                                #print(sql)
                                mycursor = mydb.cursor()
                                mycursor.execute(sql)
                                mydb.commit()

                                print("New record inserted, ID:", ID)
                                # 3 purple flashes
                                led_pwm1.start(50)
                                led_pwm3.start(50)
                                time.sleep(0.1)
                                led_pwm1.start(0)
                                led_pwm3.start(0)
                                time.sleep(0.1)
                                led_pwm1.start(50)
                                led_pwm3.start(50)
                                time.sleep(0.1)
                                led_pwm1.start(0)
                                led_pwm3.start(0)
                                time.sleep(0.1)
                                led_pwm1.start(50)
                                led_pwm3.start(50)
                                time.sleep(0.1)
                                led_pwm1.start(0)
                                led_pwm3.start(0)

                                
                                
                                
                        except Exception:
                                print("Could not insert data into mySQL DB")
                                led_pwm3.start(50)
                                time.sleep(0.1)
                                led_pwm3.start(0)

                except Exception:
                        print('corrupted data!')
                        os.remove('/home/pi/HDS/log/temp1.csv')
                        # 2 red flashes
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        time.sleep(0.1)
                        led_pwm3.start(70)
                        time.sleep(0.1)
                        led_pwm3.start(0)
                        
        mycursor = mydb.cursor()
        try:
                mycursor.execute("SELECT ID FROM system_data order by ID Desc limit 1")
                myresult = mycursor.fetchone()
                ID_DB = myresult[0]
                #print(ID_DB, ID)
                if (str(ID) == str(ID_DB)):
                        os.remove('/home/pi/HDS/log/temp1.csv')
                        print("temp file deleted")
                else:
                        print("temp data does not match DB")

        except Exception:
                print("could not connect to DB to match ID's")
                
                        
        ########################################################################
                        
        internet_test()
        
        ##########################################################################
       
ser.close()
mycursor.close()
mydb.close()
