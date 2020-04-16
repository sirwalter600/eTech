#################################  CONIFG FILE  ################################

import mysql.connector
import serial, time
import datetime
import csv
import subprocess

################################################################################

#with open('/home/pi/HDS/config/config.csv') as data_csv:
with open('/home/pi/HDS/config/config.csv') as data_csv:
	rows = csv.reader(data_csv, delimiter=',')
	try:
                        
		for row in rows:
			#print(row)
			Device_ID = row[0]
			mode = row[1]
			client = row[2]
			software = row[3]
			last_update = row[4]
			comments = row[5]

	
	except Exception:
		print("cannot read config file")
		Device_ID = 'unknown'
		mode = 'paver'
		client = ''
		software = ''
		last_update = ''
		comments = ''

################################################################################

# mode = 'paver'             ### paver, roller, plant, other ###
#Device_ID = 'HDS_tech001'      ### HDS serial number ###

try:
	mydb = mysql.connector.connect(
	host="79.170.44.107",
	user="cl25-ecube",
	passwd="4fs/RD6Ky",
	database="cl25-ecube"
	)

	mycursor = mydb.cursor()
	sql = "SELECT * FROM config WHERE device_ID = Device_ID;"
	mycursor.execute(sql)
	myresult = mycursor.fetchone()
	#print(myresult)
	
	Device_ID_DB, mode_DB, client_DB, software_DB, last_update_DB, comments_DB = myresult
	
	try:
		configfile = ('/home/pi/HDS/config/config.csv')
		#configfile = ('/home/pi/HDS/config/config.csv')
		configfile = open (configfile, "w")
		#os.chmod(logfile, 0o777)

		configfile.write(Device_ID_DB + "," + mode_DB + "," + client_DB + "," + software_DB + "," + str(last_update_DB) + "," + comments_DB)
		configfile.close()
		
		Device_ID = Device_ID_DB
		mode = mode_DB
		client = client_DB
		software = software_DB
		last_update = last_update_DB
		comments = comments_DB
	
	except Exception:
		print("could not update text file")
	
except Exception:
	print("could not get data")
	Device_ID = Device_ID
	mode = mode
	client = client
	software = software
	last_update = last_update
	comments = comments
	
################################################################################

print(Device_ID)
print(mode)
print(client)
print(software)
print(last_update)
print(comments)





