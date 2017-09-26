#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 3 Assignment http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv """

import argparse,csv,datetime,operator,re,urllib2

def downloadData(url):
    """Gets CSV file"""
    urlfile = urllib2.urlopen(url)
    return urlfile


def processData(content):
    """Proceses CSV file"""
    csvData = csv.reader(content)
    dateFormat = "%Y-%m-%d %H:%M:%S"
    hits = 0
    imgHits = 0 
    safari = chrome = firefox = msie = 0

    times = {}
    for i in range(0,24):
        times[i] = 0
        
    for row in csvData:
        result = {"path":row[0], "date":row[1], "browser": row[2], "status": row[3], "size": row[4]}

        date = datetime.datetime.strptime(result["date"], dateFormat)
        times[date.hour] = times[date.hour] + 1

        hits += 1
        if re.search(r"\.(?:jpg|jpeg|gif|png)$", result["path"], re.I | re.M):
            imgHits += 1

        elif re.search("chrome/\d+", result["browser"], re.I):
            chrome += 1

        elif re.search("safari", result["browser"], re.I) and not re.search("chrome/\d+", result["browser"], re.I):
            safari += 1

        elif re.search("firefox", result["browser"], re.I):
            firefox += 1

        elif re.search("msie", result["browser"], re.I):
            msie += 1

    imageRequest = (float(imgHits) / hits) * 100
    browsers = {"Safari": safari, "Chrome": chrome, "Firefox": firefox, "MSIE": msie}

  
    stimes = sorted(times.items(), key = operator.itemgetter(1), reverse=True)
    for i in stimes:
        print "Hour %02d has %s hits." % (i[0], i[1])
        
    print "Image requests account for {0:0.1f}% of all requests.".format(imageRequest)
    print "The most popular bowser is %s." % (max(browsers.iteritems(), key=operator.itemgetter(1))[0])



def main():
    url_parser = argparse.ArgumentParser()
    url_parser.add_argument("--url", help="Enter the URL of CSV file:")
    args = url_parser.parse_args()

    if args.url:
        try:
            csvData = downloadData(args.url)
            processData(csvData)       

        except urllib2.URLError as e:
            print "Invalid URL."
    else:
        print "Please type the URL."

if __name__ == "__main__":
    main()
    
    
