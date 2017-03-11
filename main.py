
import csv
import time
import string
import random
import json
#Time
TimePeriods = {'D':86400000,'W':604800000,'M':2419200000, 'Y':29030400000}
#GLOBAL INDEXES : Plug and play the current indexes

AUTHOR_INDEX = 0
GEN_CAT_INDEX = 1
TITLE_INDEX = 2
CALLOUT_INDEX = 3
SUMMARY_INDEX = 4
TYPE_INDEX = 5
LINKS_INDEX = 6
RESPONSES_INDEX = 7
WEIGHTS_INDEX = 8
IMG_URL_INDEX = 9
CATEGORY_INDEX = 10
EXPIRES_INDEX = 11
POINTS_INDEX = 12
READY_INDEX = 13

JSON_INDEX_SCHEMA ={
      "callout" : CALLOUT_INDEX,
      "category" : CATEGORY_INDEX,
      "expires" : EXPIRES_INDEX,
      "imageURL" : IMG_URL_INDEX,
      "points" : POINTS_INDEX,
      "summary" : SUMMARY_INDEX,
      "links" : LINKS_INDEX,
      "title" : TITLE_INDEX,
      "type" : TYPE_INDEX
    }

batch = []
Quibbls = {}

def writeRowToDump(row):
	timestamp = int(time.time())
	quibbl = {}
	for key in JSON_INDEX_SCHEMA:
		quibbl[key] = row[JSON_INDEX_SCHEMA[key]]
	quibbl['timestamp'] = timestamp
	
	try: #CSV Reads in as string. Checks to see if it is a shorthand identifier or expressed in milliseconds
		quibbl['expires'] = int(quibbl['expires'])
	except:
		try: 
			quibbl['expires'] = TimePeriods[quibbl['expires'].upper()]
		except:
			quibbl['expires'] = None
	return quibbl
	
def readInBatchFile():
	with open('batchupload.csv', 'rb') as batchfile:
	    batchreader = csv.reader(batchfile, quotechar='"')
	    for row in batchreader:
	        #row[CALLOUT_INDEX] = row[CALLOUT_INDEX].split(",") #Uncomment if you want Callouts to be a list of callouts
	    	#row[CALLOUT_INDEX] = [s.strip() for s in row[CALLOUT_INDEX]]
	        row[LINKS_INDEX] = row[LINKS_INDEX].split(",")
	    	row[LINKS_INDEX] = [s.strip() for s in row[LINKS_INDEX]]
	        batch.append(row)
	batchfile.close()

def main():
	readInBatchFile()
	generateBatch()
	dumpBatchToJSON()
	updateBatchCSV()

def generateBatch():
	global batch
	for row in batch[1:]:
		if row[READY_INDEX] == '1':
			quibble = writeRowToDump(row)
			quibbleID = id_generator(quibble['timestamp'])
			Quibbls[quibbleID] = quibble
			row[READY_INDEX] = '2'

def dumpBatchToJSON():
	global Quibbls
	timestamp = int(time.time())
	Quibbls = {"quibbls":Quibbls}
	with open(str(timestamp) + '-batch.json', 'w') as fp:
	    json.dump(Quibbls, fp, indent=2, sort_keys=True)
	return

def updateBatchCSV():
	with open("output.csv", "wb") as f:
	    writer = csv.writer(f)
	    for row in batch:
	        #row[CALLOUT_INDEX] = ','.join(row[CALLOUT_INDEX]) #Uncomment to make callouts a list of callouts
	        row[LINKS_INDEX] = ','.join(row[LINKS_INDEX])
	    	writer.writerow(row)

def id_generator(timestamp, size=10, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
   return str(timestamp) + '-' + ''.join(random.choice(chars) for _ in range(size))
if __name__ == "__main__":
	main()