import json, pickle

f1 = open("jan2016.txt", "r+")
f2 = open("output4.txt", "r+")

contentLabels = dict()
imageLabels = dict()

flag = True
i = 0

f2text = f2.read().split("\n-----\n")

for ff in range(len(f2text)):
    # f2id = f2text[ff][:18]
    # f2text[ff] = f2text[ff][19:]
    f2id = f2text[ff].split("\n")[0]
    # print str(ff)+": "+f2id
    f2text[ff] = f2text[ff][19:]
    # f2text[ff] = f2text[ff][1]
    try:
        pos = f2text[ff].index('[', 3, len(f2text[ff])-1)
        contentLabels[f2id] = eval(f2text[ff][:pos])
        imageLabels[f2id] = [ilt.encode('ascii', 'ignore') for ilt in eval(f2text[ff][pos:])]
    except:
        contentLabels[f2id] = []
        imageLabels[f2id] = []

f2.close()

# print len(contentLabels)


megaData = dict()

f1text = json.load(f1)["ads"]

f1.close()

for dt in range(len(f1text)):
    dateX = f1text[dt]["date"].encode('ascii', 'ignore')
    megaData[dateX] = dict()
    megaData[dateX]["TOI"] = list()
    for page in f1text[dt]["pages"]:
        temp = dict()
        temp["heading"] = page["pageHeading"].encode('ascii', 'ignore')
        temp["ads"] = list()
        for a in page["ads"]:
            temp2 = dict()
            temp2["width"] = float(a["width"][:-2].encode('ascii', 'ignore'))
            temp2["height"] = float(a["height"][:-3].encode('ascii', 'ignore'))
            temp2["aspect_ratio"] = temp2["width"]/temp2["height"]
            # Bin aspect ratio
            a_id = a["ID"].encode('ascii', 'ignore')
            temp2["imageLabels"] = imageLabels[a_id]
            temp2["contentLabels"] = contentLabels[a_id]
            temp["ads"].append(temp2)
        megaData[dateX]["TOI"].append(temp)

# megaData = json.dumps(megaData)
# print type(megaData)
# print megaData

fPkl = open("jsonDataFile.pkl", "wb")

pickle.dump(megaData, fPkl)