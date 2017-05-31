# Input: 
# Image -> image location on file (after saving with PHP)
# Labels (optional)
# Preferred time (range of dates)

# Processing:
# Extract ad dim -> get aspect ratio
# Extract ad labels (using Google Vision)

# For Preferred Time:
# 	on those dates, find page number with highest occurrence of ad labels -> n
# 	check if n >= threshold for any of the dates
# 	if yes:
# 		pick date with highest n
# 		give chosen page number
# 		check common aspect ratios for that page
# 		if ad AR is similar to any, recommend
# 		else suggest closest AR (may be multiple)
# 	if no:
# 		(ad not viable on Preferred dates)
# 		scan month, find [date][page] number with highest occurrence of ad labels -> n
# 		check common aspect ratios for that page
# 		if ad AR is similar to any, recommend
# 		else suggest closest AR (may be multiple)

import requests, sys, json, nltk, base64
from PIL import Image

#  input will be python algo_rough.py <image path> <file with labels path> <start date YYYY/MM/DD> <end date <YYYY/MM/DD>

def getUsefulInfo(res) :
    final = {}
    for annotation in res["responses"] :
        if "labelAnnotations" in annotation.keys() :
            final["imageLabels"] = list()
            for label in annotation["labelAnnotations"] :
                final["imageLabels"].append(label["description"])

        if "textAnnotations" in annotation.keys() :
            final["textContent"] = annotation["textAnnotations"][0]["description"]

        if "imagePropertiesAnnotation" in annotation.keys() :
            final["colors"] = annotation["imagePropertiesAnnotation"]["dominantColors"]["colors"]

    return final

def get_info_from_local_image(img_string) :
    body = {
        "requests": [
            {
                "image": {
                    "content": img_string
                },
                "features": [
                    {
                        "type": "LABEL_DETECTION"
                    },
                    {
                        "type": "TEXT_DETECTION"
                    }
                    # ,
                    # {
                    #     "type": "IMAGE_PROPERTIES"
                    # }
                    # The output of this is kinda weird. Let's not use it until we figure out a creative way of using the hundred colors it outputs.
                ]
            }
        ]
    }
    r = requests.post("https://vision.googleapis.com/v1/images:annotate?key=" + api_key, json=body)
    return getUsefulInfo(r.json())

def text2labels(text) :
    lines = text
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(lines)
    nouns = [word.encode('ascii', 'ignore') for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    return nouns

api_key = "AIzaSyBiSeSxbhQ97Drl6S84xFAPzntmu88QWOk"

filepath = sys.argv[1]
labelfile = sys.argv[2]
startdate = sys.argv[3]
enddate = sys.argv[4]

# print startdate, enddate
# import os
# os._exit(0)

# Image file operations
fp = open(filepath, "rb")
img = Image.open(fp)
width, height = img.size
fp.close()

with open(filepath, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

img_text = get_info_from_local_image(encoded_string)
adContentLabels = text2labels(img_text['textContent'])
adImageLabels = [t.encode('ascii', 'ignore') for t in img_text['imageLabels']]

# Label file operations
with open(labelfile, "r+") as lp:
	clientContentLabels = eval(lp.read())

adContentLabels.extend(clientContentLabels)

dateFlag = False

with open("janDataFinal.txt", "r+") as jsfp:
	data = json.load(jsfp)

# Processing
# Need to add support for cross-month date ranges
start_date_num = int(startdate[-2:])
end_date_num = int(enddate[-2:])

num_pages = end_date_num - start_date_num
date_list = [startdate]

cur_date = startdate
for i in range(num_pages-1):
	ldigit = int(cur_date[-1])
	if ldigit == 9:
		cur_date = cur_date[:-2]+str(int(cur_date[-2])+1)+"0"
	else:
		cur_date = cur_date[:-1]+str(ldigit+1)
	date_list.append(cur_date)
date_list.append(enddate)

max_pages = 0

for dt in date_list:
	if len(data[dt]["TOI"]) > max_pages:
		max_pages = len(data[dt]["TOI"])

pageMax = 0
recPage = 0
recDate = ""
threshold = 50

for dt in date_list:
	page_count = dict()
	for page in range(len(data[dt]["TOI"])):
		for ad in data[dt]["TOI"][page]["ads"]:
			for lbl in ad["contentLabels"]:
				for aCL in adContentLabels:
					if aCL.lower() in lbl.lower() or lbl.lower() in aCL.lower():
						page_index = page + 1
						if page_index in page_count.keys():
							page_count[page_index] += 1
						else:
							page_count[page_index] = 1
	
	curMax = max(page_count)
	if curMax > pageMax:
		pageMax = curMax
		recPage = max(page_count.iterkeys(), key=lambda k: page_count[k])
		recDate = dt

if pageMax > threshold:
	print "1"
	print recPage
	print recDate
else:
	pageMax = 0
	recPage = 0

	for dt in data.keys():
		if dt not in date_list:
			page_count = dict()
			for page in range(len(data[dt]["TOI"])):
				for ad in data[dt]["TOI"][page]["ads"]:
					for lbl in ad["contentLabels"]:
						for aCL in adContentLabels:
							if aCL.lower() in lbl.lower() or lbl.lower() in aCL.lower():
								page_index = page + 1
								if page_index in page_count.keys():
									page_count[page_index] += 1
								else:
									page_count[page_index] = 1
			curMax = max(page_count)
			if curMax > pageMax:
				pageMax = curMax
				recPage = max(page_count.iterkeys(), key=lambda k: page_count[k])
				recDate = dt

	if pageMax > threshold:
		print "0"
		print recPage
		print recDate
	else:
		print "-1"

recPageHeading = data[recDate]["TOI"][recPage-1]["heading"]
print recPageHeading

adAspectRatio = float(width)/height
adAspectRatio = int(adAspectRatio * 10)
if adAspectRatio % 2 == 1:
	adAspectRatio = adAspectRatio + 1
adAspectRatio = float(adAspectRatio) / 10

arSet = set()

for ad in data[recDate]["TOI"][recPage-1]["ads"]:
	arSet.add(ad["aspect_ratio"])

if adAspectRatio not in arSet:
	recAdAspectRatio = min(list(arSet), key=lambda x:abs(x-adAspectRatio))
else:
	recAdAspectRatio = adAspectRatio

print recAdAspectRatio