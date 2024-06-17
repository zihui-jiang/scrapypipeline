# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapypipelinePipeline:
    def process_item(self, item, spider):
        self.cursor.execute(
            "INSERT INTO raw_table (title, company, location, date_posted) VALUES (%s, %s, %s, %s)",
            (item['title'], item['company'], item['location'], item['date_posted'])
        )
        self.connection.commit()

        return item
    
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            dbname='mydatabase',
            user='myuser',
            password='mypassword',
            host='postgres'
        )
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        
        self.connection.close()
