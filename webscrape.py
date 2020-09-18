# import requests
import re
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import urllib.request as urllib2
import pymysql.cursors
from credential import Credential
from connection import Connection

# Data Models


class Author:
    def __init__(self, name, dob, description):
        self.name = name
        self.dob = dob
        self.description = description


class Data:
    def __init__(self, author, quote, tags):
        self.author = author
        self.quote = quote
        self.tags = tags


def add_data(connection, data):
    try:
        result = Connection.get_single_data(connection, ['id'], ['author'], [
                                            'name'], [data.author.name])
        id = -1
        qid = -1
        if result == None:
            id = Connection.insert_data(connection, ['name', 'dob', 'description'], 'author', [
                                        data.author.name, data.author.dob, data.author.description])
        else:
            id = result['id']
        qid = Connection.insert_data(
            connection, ['author_id', 'quote'], 'quotes', [id, data.quote])
        qid = Connection.insert_data(connection, ['quote_id', 'tag'], 'tags', [
                                     qid, ",".join(data.tags)])
    except pymysql.Error as err:
        print(err)


def main():
    try:
        myCredential = Credential()
        connection_obj = Connection(myCredential)
        connection = connection_obj.connect_db("localhost", "webscrape")
    except pymysql.Error as err:
        print(err)

    # get access to the web page using urllib2
    html_code = urllib2.urlopen("http://toscrape.com").read()
    parsed_html_code = bs(html_code, 'html.parser')

    # find the link to quotes
    url_to_quotes = parsed_html_code.find(
        "a", text=re.compile("A website"))['href']

    # get the web page
    html_code = urllib2.urlopen(url_to_quotes).read()
    parsed_html_code = bs(html_code, 'html.parser')

    # Scrapping All Pages
    stop = False
    page = 1
    while stop == False:
        print('Scaraping Page %i' % page)
        # get quote details
        for quote_div in parsed_html_code.find_all("div", {"class": "quote"}):
            quote = quote_div.find("span", {"class": "text"}).text
            author_name = quote_div.find("small", {"class": "author"}).text
            tags = [tag.text for tag in quote_div.find_all(
                "a", {"class": "tag"})]

            # Get the author details
            author_parsed_html_code = bs(urllib2.urlopen(
                urljoin(url_to_quotes, quote_div.find("a")['href'])).read(), 'html.parser')
            author_dob = author_parsed_html_code.find(
                "span", {"class": "author-born-date"}).text
            author_description = author_parsed_html_code.find(
                "div", {"class": "author-description"}).text.strip()

            author_obj = Author(author_name, author_dob, author_description)
            data_obj = Data(author_obj, quote, tags)
            add_data(connection, data_obj)

        # Check if next page does'nt exists
        if parsed_html_code.find('li', 'next') == None:
            stop = True
        else:   # If next page exists, Goto next page
            next_page = parsed_html_code.find('li', 'next').find('a')['href']
            parsed_html_code = bs(urllib2.urlopen(
                urljoin(url_to_quotes, next_page)).read(), 'html.parser')
            page += 1

    print("For test purpose: id-1")
    result = Connection.get_single_data(connection, ['id'], ['author'], [
                                        'name'], ['Albert Einstein'])
    print(result)
    connection.close()
    print("Task Done!!!")


if __name__ == '__main__':
    main()
