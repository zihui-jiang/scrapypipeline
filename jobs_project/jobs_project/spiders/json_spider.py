import json
import scrapy
import logging
from jobs_project.items import JobItem

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobs_project.pipelines.MyPipeline': 300,
        },
    }

    def __init__(self, **kwargs):
        # your code here
        pass

    def close_spider(self, spider):
        self.connection.close()

    def start_requests(self):
        # your code here
        # make sure you can send a request locally at the file
        # if you can't get this to work, do not waste too much time here
        # instead load the json file inside parse_page
        yield scrapy.Request(
        url='file:///usr/src/app/s02.json',
        callback=self.parse_page,
        )

    def parse_page(self, response):
        # your code here
        # load json files using response.text
        # loop over data
        # return items
        data = json.loads(response.text)
        jobs = data['jobs']
        for job in jobs:
            job_data = job['data']
            item = JobItem()
            item['slug'] = job_data.get('slug')
            item['language'] = job_data.get('language')
            item['req_id'] = job_data.get('req_id')
            item['title'] = job_data.get('title')
            item['description'] = job_data.get('description')
            item['city'] = job_data.get('city')
            item['state'] = job_data.get('state')
            item['country_code'] = job_data.get('country_code')
            item['postal_code'] = job_data.get('postal_code')
            item['latitude'] = job_data.get('latitude')
            item['longitude'] = job_data.get('longitude')
            item['apply_url'] = job_data.get('apply_url')
            # Add other fields as needed
            logging.info(f"Yielding job: {item}")
            yield item
