# Web Scraping

## Introduction

To scrape the quotes and author details from the website.

## Pre-requisites

* Python 3.8.5
* Beautifulsoup4
* requests
* urllib
* PyMySQL

## Setup

To install this modules type the following commands in cmd:

```
pip install requests beautifulsoup4 PyMySQL urllib3 

```

## Database Setup

* Install XAMPP or WAMP.
* Run the MySQL server.
* Go to **localhost/phpmyadmin** and login.
* Create a database with name **webscrape**.
* Go to import and select the **database_schema.sql**.

## Usage

Open the command line where the script is present. To execute the script type `python webscrape.py`. You should see the database for the new entries.