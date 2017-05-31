import requests, os
def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

apiKey = 'bf995586a58895'

# for img in os.listdir('./ImageData'):
#     print ocr_space_file('./ImageData/'+img, False, apiKey)

print ocr_space_url('http://epaperbeta.timesofindia.com/NasData/Publications/TheTimesOfIndia/Bangalore/2015/02/19/Article/002/19_02_2015_002_003.jpg', False, apiKey)