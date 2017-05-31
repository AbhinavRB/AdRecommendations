from google.cloud import vision

def getInfo(uri) :
	vision_client = vision.Client()
	image = vision_client.image(source_uri=uri)

	texts = image.detect_text()
	print('Texts:')

	for text in texts:
		print('\n"{}"'.format(text.description))

	labels = image.detect_labels()
	print('Labels:')

	for label in labels:
		print(label.description, label.score)

url = "http://epaperbeta.timesofindia.com/NasData/Publications/TheTimesOfIndia/Bangalore/2015/02/19/Article/002/19_02_2015_002_003.jpg"
getInfo(url)