import json, pickle

with open("dataFileFormatted.txt", "r+") as df:
	data = json.load(df)

for dt in data.keys():
	for pg in range(len(data[dt]["TOI"])):
		for ad in range(len(data[dt]["TOI"][pg]["ads"])):
			ar = data[dt]["TOI"][pg]["ads"][ad]["aspect_ratio"] * 10
			ar = int(ar)
			if ar % 2 == 1:
				ar += 1
			ar = float(ar)/10
			data[dt]["TOI"][pg]["ads"][ad]["aspect_ratio"] = ar

# json_text = json.dumps(data)
# with open("janDataFinal.txt", "w+") as f:
# 	f.write(json_text)

fPkl = open("janDataFinal.pkl", "wb")

pickle.dump(data, fPkl)