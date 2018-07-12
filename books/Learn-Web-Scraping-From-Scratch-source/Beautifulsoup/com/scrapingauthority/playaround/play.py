from bs4 import BeautifulSoup
import urllib2

#Open page
##########################

#set user agent
request = urllib2.Request('https://scrapethissite.com/pages/simple/')
request.add_header('User-Agent', 'ScrapingAuthority Scraper(ScrapingAuthority.com')

#open page
open = urllib2.urlopen(request)

# use python's built-in parser though you can use lxml or other thrid party parser
page = BeautifulSoup(open, 'html.parser')

#title of page
title = page.title.text

##########################

#Selector
##########################
#css--> ountry name
country_name_tags_selector = page.select('.row .col-md-4.country .country-name')



#Headline3, the first one
h3 = page.h3.get_text()


#all country name tag by class name, and tag
country_name_tags = page.find_all('h3', class_ = 'country-name')

#extracting text
country_names = []
for country_name_tag in country_name_tags :
    country_names.append(country_name_tag.get_text())
##########################


#pagination
##########################

link_tags = page.find_all('a')
links = []
for link_tag in link_tags:
    links.append(link_tag.get('href'))

##########################