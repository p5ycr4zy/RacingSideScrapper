#!/usr/bin/python
# -*- coding: utf-8 -*-
# Last updated on: March 20, 2013

# All the import stuffs#
# If you don't have anything, please have that or I can help you to get that!
from mechanize import Browser
# You might need to change the following line based on your
# BeautifulSoup location
from bs4 import BeautifulSoup
import csv
import re

# ----------Import ENDs here-------------

def main():
    # Landing page URL as specified
    SEARCH_URL = 'http://www.racingandsports.com.au/form-guide/'
    br = Browser()  #Initiating browser

    br.set_handle_robots(False) # To tackle robot.txt
    response = br.open(SEARCH_URL).read()
    soup = BeautifulSoup(response)
    f = open("output.html", "w")    # local temporary file to work with!
    f.write(str(soup))
    f.close()

    ## Creating CSV file
    csv_output = csv.writer(open("output.csv", "wb"))   # output.csv is the output file name!
    csv_output.writerow(["Track","RcNo","TAB","Horse","WT","BP", "JOCKEY", "JRat", "TRAINER", "TRat"]) # Setting first row with all column titles

    for a_tr in soup.findAll("a", attrs={ "class" : "nf" }):
        #print temp['href']
        if len(str(a_tr))< 85:
            new_soup = BeautifulSoup(str(a_tr))
            temp = new_soup.find('a',href=True)
            NEW_SEARCH_URL = SEARCH_URL+temp['href']
            print NEW_SEARCH_URL
            print a_tr
            ## Extracting race_track
            temp = str(a_tr).split("\">")[1]
            race_track = temp.split("<")[0]
            ## DONE [Extracting race_track]
            ## Working with all the races
            #meeting.asp?raceno=2&meeting=29545
            race_number = str(NEW_SEARCH_URL).split("=")[1]
            race_pagelist = [NEW_SEARCH_URL]
            #meeting.asp?raceno=2&meeting=29545
            ## Appending all the race_pages to a list
            for x in range(2,10):
                new_race_page = SEARCH_URL+"meeting.asp?raceno="+str(x)+"&meeting="+race_number
                race_pagelist.append(new_race_page)
            #print race_pagelist
            
            race_no = 0
            for race_page in (race_pagelist):
                value_to_write = []
                print race_page
                print "--------------------------------------------"
                print "Race Number:", race_no, "for", race_track
                print "--------------------------------------------"
                value_to_write.extend([race_track,race_no])
                try:
                    # Working on each individual site
                    new_br = Browser()
                    new_br.set_handle_robots(False)
                    new_response = new_br.open(race_page).read()
                    new_soup = BeautifulSoup(new_response)
                    race_no += 1
                    # Getting all the BID values
                    bid_val = []
                    bid_val = new_soup.findAll('div', id=re.compile('RHS11'))
                    print bid_val
                    print bid_val[0]
                    temp_bid = BeautifulSoup(str(bid_val[0]))
                    paragraphs = temp_bid.findAll('strong')
                    #items = re.findall('<strong>(.*?)</strong>', temp_bid, re.S)
                    key_values = []
                    for cont in paragraphs:
                        print cont.contents
                        key_values.append(str(cont.contents))
                    #print paragraphs.contents
                    list_val = re.findall('.*?\</strong>(.*?)\<strong>.*?', str(temp_bid))
                    last_val = str(temp_bid).split("</strong>")
                    

                    #([^/]+)$
                    print "last_val:", last_val
                    temp_last_val = str(last_val[-1]).split("\t\t")
                    list_val.append(temp_last_val[0])
                    for l_val in list_val:
                        print "new val:", l_val
                        
                    # working with dictionary
                    bid_values = {}
                    print "Key:", key_values
                    for key, value in zip(key_values, list_val):
                        bid_values[str(key)] = value
                    
                    print bid_values
                            
                    
                    for a_tbody in new_soup.findAll("tbody", { "id" : "offTblBdy" }):
                        columns = BeautifulSoup(str(a_tbody).decode('utf-8', 'ignore')).findAll('td')
                        value_to_write = []
                        value_to_write.extend([race_track,race_no])
                        #race_no += 1
                        #html.decode('utf-8', 'ignore')
                        counter = 0
                        for td in columns:
                            value = (td.contents[0]).encode('latin1')
                            if (not value.startswith("<")) and counter!= 7:
                                if (value) and (not (value.isspace())):
                                    print (value).strip()+"\t",
                                    value_to_write.append(value.strip())
                                else:
                                    print "null"+"\t",
                                    value_to_write.append("null")
                            counter += 1
                            ## Critical Section
                            ## How I am maintaing each row values from each page
                            if counter % 10 == 0:
                                counter = 0
                                print
                                print "LENGTH", len(value_to_write) 
                                #csv_output.writerow
                                #for word in value_to_write:
                                ## Writing the whole row to the output file
                                csv_output.writerow(value_to_write)
                                ## initializing empty list for the next row!
                                value_to_write = []
                                value_to_write.extend([race_track,race_no])                                    
                except:
                    break
    print "Done"

if  __name__ =='__main__':
    main()
