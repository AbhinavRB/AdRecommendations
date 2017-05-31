# Input :
#     Page number
#     Total pages
#     Date of paper
#
# Output : (for date +- 3)
#     Aspect ratio - page
#     content labels - ad data for page +- 5%
#     image labels - ad data for page +- 5%
#     #advertiser - ad data for page +- 5% -- not doing now

import sys, datetime, pickle, json

newspaper = "TOI"

with open("janDataFinal.pkl", "r") as pklFile:
    data = pickle.load(pklFile)

def getFrequencies(date, npaper, page_perc, key) :
    # page_perc - tuple of (start_percentage, end_percentage)

    return_obj = dict()

    if date not in data.keys() :
        print "no date found", date
        return dict()

    pages = data[date][npaper]

    total_pages = len(pages)
    reqd_pages = pages[int(page_perc[0]/100.0*total_pages) : int(page_perc[1]/100.0*total_pages)]

    for page in reqd_pages :
        for ad in page['ads'] :
            if type(ad[key]) == list :
                for val in ad[key] :
                    return_obj[val] = return_obj.get(val, 0) + 1

            else:
                val = ad[key]
                return_obj[val] = return_obj.get(val, 0) + 1

    return return_obj

def agencyAlgorithm(page_no, total_pages, date) :
    global newspaper

    freq_obj = dict()
    keys = ["aspect_ratio", 'contentLabels', 'imageLabels']

    for k in keys :
        freq_obj[k] = dict()

    date_split = date.split("/")
    dt = datetime.date(int(date_split[0])-1, int(date_split[1]), int(date_split[2]))


    perc = page_no / total_pages
    page_perc = (max(int(perc) - 5, 0), min(int(perc) + 5, total_pages))

    for n in range(-3, 4) :
        dt_new = dt + datetime.timedelta(days=n)

        for k in keys :
            ret = getFrequencies(dt_new.strftime('%Y/%m/%d'), newspaper, page_perc, k)

            for k2 in ret.keys() :
                freq_obj[k][k2] = ret[k2] + freq_obj[k].get(k2, 0)


    sorted_freq_obj = dict()
    for k in keys :
        sorted_freq_obj[k] = sorted(freq_obj[k], key=freq_obj[k].get, reverse=True)

    unicodeFlag = 0
    required_dict = dict()

    for k in keys :
        top_x_output = 10
        required_dict[k] = [(x, freq_obj[k][x]) for x in sorted_freq_obj[k][:top_x_output]]

        # if unicodeFlag > 0:
        #     print [t.encode('ascii', 'ignore') for t in sorted_freq_obj[k][:top_x_output]]
        # else:
        #     print sorted_freq_obj[k][:top_x_output]
        # unicodeFlag += 1
    
    for k in keys :
        print k, [x[0] for x in required_dict[k]]
    # For Graphing :
    for k in keys:
        print "\n\n"+k+"\n"+str([x[0] for x in required_dict[k]])+"\n"+str([x[1] for x in required_dict[k]])

    # for k in keys :
    #     print k, sorted(freq_obj.items(), key=lambda x: x[1])[:5]


if len(sys.argv) < 4 :
    page_no = int(input("Enter page number : "))
    total_pages = int(input("Enter total number of pages : "))
    date = raw_input("Enter date in the format YYYY/MM/DD : ")

else :
    page_no = int(sys.argv[1])
    total_pages = int(sys.argv[2])
    date = sys.argv[3]

agencyAlgorithm(page_no, total_pages, date)

