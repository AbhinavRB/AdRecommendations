import requests, sys, json, nltk

api_key = "AIzaSyBiSeSxbhQ97Drl6S84xFAPzntmu88QWOk"


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

def get_info_from_image_uri(img_url) :
    body = {
        "requests": [
            {
                "image": {
                    "source": {
                        "imageUri": img_url
                    }
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

# f2 = open("output4.txt", "w")

def text2labels(text) :
    lines = text
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(lines)
    nouns = [word.encode('ascii', 'ignore') for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    return nouns


import base64

with open("ImageData/ad1.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

img_text = get_info_from_local_image(encoded_string)
print text2labels(img_text['textContent'])
print img_text['imageLabels']

# with open("jan2016.txt", "r") as f:
#     file = json.load(f)["ads"]

#     for dt in range(len(file)):
#         date = file[dt]["date"]
#         for pg in range(len(file[dt]["pages"])):
#             for ad in range(file[dt]["pages"][pg]["NoOfAds"]):
#                 id = file[dt]["pages"][pg]["ads"][ad]["ID"]
#                 url = "http://epaperbeta.timesofindia.com/NasData/Publications/TheTimesOfIndia/Bangalore/"+date+"/Article/"+id.split('_')[3]+"/"+id+".jpg"

#                 data =  get_info_from_image_uri(url)
#                 f2.write(id+"\n")
#                 fc = True
#                 for k in data.keys():
#                     try:
#                         # print "Doing..."
#                         if fc:
#                             f2.write(str(text2labels(str(data[k]))))
#                             # print text2labels(str(data[k]))
#                             fc = False
#                         else:
#                             f2.write(str(data[k]))
#                             # print str(data[k])
#                             fc = True
#                     except:
#                         pass
#                 f2.write("\n-----\n")
#                 # print "\n-----\n"


# f2.close()