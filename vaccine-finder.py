import sys
import pyttsx3
import datetime
import requests
import winsound
import schedule
import time
from datetime import datetime

AGE_FILTER = sys.argv[1]
DISTRICT_ID = sys.argv[2] # Determine Districts of interest from here 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/16'
SCAN_FREQUENCY_SECONDS = 30
APPOINTMENT_COUNT_THRESHOLD = 3 # Notify ONLY when 3 or more seats are available

def job():
	print("---------------------Checking At "+str_date(1)+"-----------------------")
	VAC_FINDER_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
	fd = str_date(0)
	VAC_FINDER_URL += "?district_id="+str(DISTRICT_ID)+"&date="+fd+""
	centers = fetch_all_vac_centers(VAC_FINDER_URL)
	r = find_open_centers(centers,AGE_FILTER)
	if not r:
		print("No Slots Available !")
	else:
		play_tone()
		to_speech(r)

def store_user_inputs():
	try:
		AGE_FILTER = sys.argv[1]
		DISTRICT_ID = sys.argv[2]
	except:
		sys.exit("[Error]: Missing required fields :'python vaccine-finder <age-filter> <district-id>'")
	try:
		SCAN_FREQUENCY_SECONDS = sys.argv[3]
		APPOINTMENT_COUNT_THRESHOLD = sys.argv[4]
	except:
		print("Optional parameters (<scan_frequency> & <appointment-count-threshold>) not provided")

def str_date(t):
	#t=1 => Long, Other Values => Short
	now = datetime.now()
	if t==1:
		dt_string = now.strftime("%d-%m-%Y %H:%M:%S")
	else:
		dt_string = now.strftime("%d-%m-%Y")
	return dt_string

def play_tone():
	print("================== Open Appointments Found ===================")
	winsound.PlaySound('notify.wav',winsound.SND_FILENAME)

def to_speech(txt):
	engine = pyttsx3.init()
	rate = engine.getProperty('rate')
	rate = 500
	engine.setProperty('rate', 200)
	volume = engine.getProperty('volume')
	engine.setProperty('volume',1.0)
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.say(str(txt))
	engine.runAndWait()
	engine.stop()
	engine.runAndWait()

def fetch_all_vac_centers(url):
	res=""
	try:
		resp = requests.get(url)
		res = resp.json()["centers"]
	except requests.exceptions.RequestException as e:
		print("[Error]: Connectivity to internet lost!")
	return res

def find_open_centers(centers,age):
	res = ""
	for c in centers:
		for s in c['sessions']:
			if(s['min_age_limit']==age and s['available_capacity_dose1'] > APPOINTMENT_COUNT_THRESHOLD):
				#res = c['name']+" => "+c['address']+" => "+c['district_name']+" => "+c['block_name']+" => "+str(c['pincode'])+" => "+s['date']+" => "+str(s['min_age_limit'])+" => "+str(s['available_capacity_dose1'])
				#res += "\n\nCenter: "+c['name']+" of "+c['district_name']+" district, "+c['block_name']+" block on "+s['date']+", "+str(s['min_age_limit'])+"+, "+str(s['available_capacity_dose1'])+" seats. "
				res += "District: "+c['district_name']+" ,"+str(s['available_capacity_dose1'])+" seats. "
				print(res)
	return res

store_user_inputs()
schedule.every(SCAN_FREQUENCY_SECONDS).seconds.do(job)
print("-----------------------------------------------")
print("Hold tight! The script will run in "+str(SCAN_FREQUENCY_SECONDS)+" seconds.")
print("Filter Criteria:")
print("1.) Age: "+str(AGE_FILTER)+"+")
print("2.) District-Id: "+str(DISTRICT_ID))
print("3.) Scan Frequency: "+str(SCAN_FREQUENCY_SECONDS)+" seconds")
print("4.) Notify ONLY when "+str(APPOINTMENT_COUNT_THRESHOLD)+"+ appointments are available")
print("Note: Districts for state of Karnataka can be found here: https://cdn-api.co-vin.in/api/v2/admin/location/districts/16")
print("-----------------------------------------------")
while True:
    schedule.run_pending()
    time.sleep(1)