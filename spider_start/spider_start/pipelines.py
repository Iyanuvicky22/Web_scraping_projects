# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
import pymongo
import sqlite3


class MongoDBPipeline:
    collection_name = "anscripts"

    def open_spider(self, spider):
        self.client = pymongo.MongoClient("mongodb+srv://apotiks:zMXKkcXJ_WfmJ3J@webscraping.b9fnrut.mongodb.net/?appName=WebScraping")
        self.db = self.client["my_database"]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item


class SQLitePipeline:

    def open_spider(self, spider):
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
        self.connection.close()

    def process_item(self, item, spider):
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
        
    
    