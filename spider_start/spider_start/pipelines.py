# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class MongoDBPipeline:
    """
    MongoDB pipeline 

    Returns:
        item : data array to be uploaded on MongoDB Online database.
    """
    collection_name = "anscripts"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(MONGO_DB_URL)
        self.db = self.client["my_database"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitePipeline:
    """
    SQLite pipeline

    Returns:
        item : data row to be uploaded on SQLite database.
    """

    def open_spider(self, spider):
        """
        Initializes SQLite database connection 
        and creates table if it doesn't exist.
        """
        self.connection = sqlite3.connect("anscripts.db")
        self.c = self.connection.cursor()

        try:
            self.c.execute('''
                CREATE TABLE anscripts (
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass
        
    def close_spider(self, spider):
        """
        Closes SQLite database connection.
        """  
        self.connection.close()

    def process_item(self, item, spider):
        """
        Process scraped data and inserts them into an sqlite db.

        Args:
            item (row data): scraped trancripts row data.

        Returns:
            _type_: _description_
        """
        self.c.execute('''
            INSERT INTO anscripts (title, plot, transcript, url) VALUES (?, ?, ?, ?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('transcript'),
            item.get('url')
        ))
        self.connection.commit()
        return item
