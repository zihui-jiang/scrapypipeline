import json
import scrapy

class JobSpider(scrapy.Spider):
    name = 'job_spider'
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobs_project.pipelines.YourPipeline': 300,
        },
    }

    def start_requests(self):
        yield scrapy.Request(
            url='file:///path/to/your/json/file.json',
            callback=self.parse_page,
        )

    def parse_page(self, response):
        data = json.loads(response.text)
        for job in data['jobs']:
            yield job
