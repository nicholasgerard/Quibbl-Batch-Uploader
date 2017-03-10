
import csv

TAG_INDEX = 3

BRAND_INDEX = 5

with open('batchupload.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, quotechar='"')
    collection = []
    for row in spamreader:
        row[TAG_INDEX] = row[TAG_INDEX].split(",")
        row[BRAND_INDEX] = row[BRAND_INDEX].split(",")
        collection.append(row)
    print collection
def writeRowToDump(row):
	return 