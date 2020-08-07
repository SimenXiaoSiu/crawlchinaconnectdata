import scrapy
import json
from datetime import datetime

class HkexshSpider(scrapy.Spider):
    name = "hkexsh"

    #allowed_domains = ["www.hkexnews.hk/"]

    start_urls = [
        'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh'
        #'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz'
    ]

    def parse(self, response):
        return scrapy.FormRequest(
            url = response.url,
            formdata = {
                '__VIEWSTATE':response.xpath('//*[@id="__VIEWSTATE"]/@value')[0].extract(),
                '__VIEWSTATEGENERATOR':response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0].extract(),
                '__EVENTVALIDATION':response.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0].extract(),
                'today':str(datetime.today().strftime('%Y%m%d')),
                'sortBy': 'shareholdingpercent',
                'sortDirection':'Desc',
                'txtShareholdingDate':'2020/07/30',
                'btnSearch':'搜尋'
            },
            callback=self.after_post
        )

    def after_post(self, response):
        searchdate = response.xpath('//*[@id="pnlResult"]/h2/span/text()')[0].extract().split(' ')[1].replace('/','')
        market = response.url.split('/')[-1].split('=')[1]
        for row in response.xpath('//*[@id="mutualmarket-result"]//tbody//tr'):
            if row.css('.col-stock-code div::text') is not None:
                yield {
                    'date': searchdate,
                    'market': market,
                    'stockcode': row.css('.col-stock-code div::text')[1].extract(),
                    'stockname': row.css('.col-stock-name div::text')[1].extract(),
                    'shareholding': row.css('.col-shareholding div::text')[1].extract(),
                    'shareholdingpercent': row.css('.col-shareholding-percent div::text')[1].extract()
                }

    def convert_date(self, fromdate):
        return fromdate.split('/')[0] + fromdate.split('/')[1] + fromdate.split('/')[2]
    
    def date_remove_slash(self, fromdate):
        return fromdate.replace('/','')