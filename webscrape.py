import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pymysql.cursors

# Data Models
class Author:
        def __init__(self,name,dob,description):
                self.name=name
                self.dob=dob
                self.description=description

class Data:
        def __init__(self,author,quote,tags):
                self.author=author
                self.quote=quote
                self.tags=tags

#connect to db
connection = pymysql.connect(host='localhost',user='root',password='root',db='webscrape',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)


def add_data(data):
        try:
            with connection.cursor() as cursor:
                sql = "SELECT `id` FROM `author` WHERE `name`=%s"
                cursor.execute(sql, (data.author.name))
                result = cursor.fetchone()
                id=-1
                qid=-1
                if result==None:
                        with connection.cursor() as c:
                                sql = "INSERT INTO `author` (`name`, `dob`, `description`) VALUES (%s, %s, %s)"
                                c.execute(sql, (data.author.name,data.author.dob,data.author.description))
                                id=c.lastrowid
                        connection.commit()
                else:
                        id=result['id']
                with connection.cursor() as c:
                                sql = "INSERT INTO `quotes` (`author_id`, `quote`) VALUES (%s, %s)"
                                c.execute(sql, (id,data.quote))
                                qid=c.lastrowid
                connection.commit()
                with connection.cursor() as c:
                                sql = "INSERT INTO `tags` (`quote_id`, `tag`) VALUES (%s, %s)"
                                for tag in data.tags:
                                        c.execute(sql, (qid,tag))
                connection.commit()
        except pymysql.Error as e:
                print(e)
        
# get the web page
r = requests.get("http://toscrape.com")
#use beautiful soup to structure the html
soup = bs(r.content, 'html.parser')
#find the link to quotes
url_to_quotes=soup.find("a",text=re.compile("A website"))['href']
# get the web page
r = requests.get(url_to_quotes)
#use beautiful soup to structure the html
soup = bs(r.content, 'html.parser')
# pretify the output
soup.pretify
stop=False
page=1;
while stop == False:
        print('Scaraping Page %i' %page)
        #get quote details
        for quote_div in soup.find_all("div", {"class":"quote"}):
            quote = quote_div.find("span", {"class":"text"}).text
            author_name = quote_div.find("small",{"class":"author"}).text
            tags = [tag.text for tag in quote_div.find_all("a",{"class":"tag"})]
            # Get the author details
            asoup = bs(requests.get(urljoin(url_to_quotes,quote_div.find("a")['href'])).content, 'html.parser')
            author_dob=asoup.find("span",{"class":"author-born-date"}).text
            author_description = asoup.find("div",{"class":"author-description"}).text.strip()
            add_data(Data(Author(author_name,author_dob,author_description),quote,tags))
        if soup.find('li','next') ==None:   # Check if next page does'nt exists
                stop=True
        else:   # If next page exists, Goto next page
                next_page=soup.find('li','next').find('a')['href']
                soup = bs(requests.get(urljoin(url_to_quotes,next_page)).content, 'html.parser')
                page+=1
connection.close()
