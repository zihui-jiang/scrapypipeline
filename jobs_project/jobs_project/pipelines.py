# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import logging
import redis
import os

class MyPipeline:
    def process_item(self, item, spider):
        id = f"scrapy:item:{item['slug']}"
        # Check if item already exists in Redis
        if self.redis.exists(id):
            logging.info(f"Item already processed: {item['slug']}")
            return item
        
        logging.info(f"Insert item: {id}")
        try:
            self.cursor.execute("""
            INSERT INTO raw_table (slug, language, req_id, title, description, city, state, country_code, postal_code, latitude, longitude, apply_url) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item['slug'],
                item['language'],
                item['req_id'],
                item['title'],
                item['description'],
                item['city'],
                item['state'],
                item['country_code'],
                item['postal_code'],
                item['latitude'],
                item['longitude'],
                item['apply_url']
            ))

            self.connection.commit()

            # Cache item in Redis
            self.redis.set(id, 1)
        except Exception as e:
            self.connection.rollback()
            logging.error(f"Error inserting item: {e}")
        return item   
        
    
    
    def open_spider(self, spider):
        self.connection = psycopg2.connect(
            dbname='mydatabase',
            user='myuser',
            password='mypassword',
            host='postgres'
        )
        self.cursor = self.connection.cursor()
        ## Create  table if none exists
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_table (
            id SERIAL PRIMARY KEY,
            slug VARCHAR(255),
            language VARCHAR(50),
            req_id VARCHAR(50),
            title VARCHAR(255),
            description TEXT,
            city VARCHAR(100),
            state VARCHAR(100),
            country_code VARCHAR(10),
            postal_code VARCHAR(20),
            latitude FLOAT,
            longitude FLOAT,
            apply_url TEXT);
        """)

        self.redis = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=os.getenv('REDIS_PORT', 6379),
                db=0
            )
        spider.log('Database and Redis connections established', level=logging.INFO)
        

    def close_spider(self, spider):
        logging.info('Closing database and Redis connections')
        if self.connection:
            self.connection.close()
        if self.redis:
            self.redis.close()
