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
from __future__ import division, unicode_literals
import requests, sys, json, nltk, base64
from PIL import Image
import math
from textblob import TextBlob as tb

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
pureAdContentLabels = adContentLabels
adImageLabels = [t.encode('ascii', 'ignore') for t in img_text['imageLabels']]

# Label file operations
with open(labelfile, "r+") as lp:
	clientContentLabels = eval(lp.read())
	for cXL in clientContentLabels:
		req = requests.get("http://www.serelex.org/find/en-patternsim-ukwac-wiki/" + cXL)
		res = req.json()

		try:
			adContentLabels.extend([rx[u'word'].encode('ascii', 'ignore') for rx in res[u'relations'][:5]])
		except:
			pass

adContentLabels.extend(clientContentLabels)

dateFlag = False

# Load dataset
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

result_dict = dict()

for dt in date_list:
	page_count = dict()
	for page in range(len(data[dt]["TOI"])):
		page_index = page + 1
		for ad in data[dt]["TOI"][page]["ads"]:
			for lbl in ad["contentLabels"]:
				for aCL in adContentLabels:
					if aCL.lower() in lbl.lower() or lbl.lower() in aCL.lower():
						if page_index in page_count.keys():
							page_count[page_index] += 1
						else:
							page_count[page_index] = 1
	
	result_dict[dt] = page_count	

result_list = list()

for k in result_dict.keys():
	# print k+": "+str(sorted(result_dict[k], key=lambda j: result_dict[k][j], reverse=True)[:5])
	for j in result_dict[k].keys():
		result_list.append({"date": k, "page": j, "count": result_dict[k][j]})
 
result_list = sorted(result_list, key=lambda x: x["count"], reverse=True)[:5]

# print str(result_list)

bloblist = list()

totalPagesList = list()

for rl in result_list:
	totalPagesList.append(len(data[rl["date"]]['TOI']))
	strList = list()
	for ad in data[rl["date"]]['TOI'][rl["page"]-1]['ads']:
		strList.extend(ad['contentLabels'])
	bloblist.append(tb(" ".join(strList)))

# print bloblist

# TF-IDF defs
def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

scoreList = list()
bestLabelList = list()

for i, blob in enumerate(bloblist):
	# print "Page: " + str(i)
	scores = {word: tfidf(word, blob, bloblist) for word in pureAdContentLabels}
	sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
	scoreList.append(sum(x[1] for x in sorted_words[:5])/5)
	bestLabelList.append([x[0] for x in sorted_words][:10])

# Final output starts here
for i in range(len(result_list)):
	print str(result_list[i]["date"]) + ":" + str(result_list[i]["page"]) +":" +  str(result_list[i]["count"]) +":" +  str(scoreList[i]) + ":" + str(totalPagesList[i])

recDate = result_list[scoreList.index(max(scoreList))]["date"]
recPage = result_list[scoreList.index(max(scoreList))]["page"]

print recDate + "--" + str(recPage)

recLabels = bestLabelList[scoreList.index(max(scoreList))]
print recLabels

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