import os, json

with open("jan2016.txt", "r") as f:
	file = json.load(f)["ads"]

	for dt in range(len(file)):
		date = file[dt]["date"]
		for pg in range(len(file[dt]["pages"])):
			for ad in range(file[dt]["pages"][pg]["NoOfAds"]):
				id = file[dt]["pages"][pg]["ads"][ad]["ID"]
				url = "http://epaperbeta.timesofindia.com/NasData/Publications/TheTimesOfIndia/Bangalore/"+date+"/Article/"+id.split('_')[3]+"/"+id+".jpg"

url = "http://epaperbeta.timesofindia.com/NasData/Publications/TheTimesOfIndia/Bangalore/2017/01/18/Article/001/18_01_2017_001_023.jpg"
				
os.system("python RESTapi.py "+url+" >> output.txt")