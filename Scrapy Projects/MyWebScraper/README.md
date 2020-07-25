
# PROJECT INFORMATION #


	This is the Scrapy project to crawl data from website. Here I used Selenium to scrap data from lazy loader.

	In this project I have scraped data from JustDial and it has saved in JSON format. Generated json looks like as follows.

[
    {
        "name": "Shree S S Properties and De..",
        "rateing": 4.1,
        "phone": "9152120789",
        "address": "Niti Khand 2-Indir.. "
    },
    {
        "name": "Sky Home Real Estate",
        "rateing": 4.0,
        "phone": "9152385411",
        "address": "Plaza Gyan Khand 1.. "
    },

]



	Following are the some instructions about project.

1. Prerequisite

	$ pip install Scrapy

	$ pip install selenium


2. Creating a project

	$ scrapy startproject MyWebScraper

		where "MyWebScraper" is project name.

	$ cd MyWebScraper


3. Create Spider

	Create spider under "spider" directory.


4. Run Project

	 ~/MyWebScraper$ scrapy crawl justdial

		where "justdial" is `name` of spider file which is declare in "JustDialSpider.py" file.


5. All Scraped Data will save inside the "SCRAPED_DATA" folder.


