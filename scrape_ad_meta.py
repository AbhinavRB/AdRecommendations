import requests

paper_id = "31806"
eg_id = "10_11_2016_024_003"

def getAdMetaData(ad_id) :
	# p = requests.get("http://epaperbeta.timesofindia.com/Gallery.aspx?id="+ad_id+"&type=A&eid="+paper_id)
	p = requests.post("http://epaperbeta.timesofindia.com/ajax/epaperAjaxMethods.AjaxUtilsMethods,ePaperAjaxMethods.ashx?_method=GetEmailsandUrls&_session=rw", data="strfromat="+ad_id)
	print p.text

getAdMetaData(eg_id)
