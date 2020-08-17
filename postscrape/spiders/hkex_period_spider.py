import scrapy
import json
from datetime import datetime,timedelta
from postscrape.items import StockItem

class HkexshSpider(scrapy.Spider):
    name = "hkexperiod"

    #allowed_domains = ["hkexnews.hk"]

    start_urls = [
        'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sh',
        'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=sz',
        'https://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk'
    ]

    def parse(self, response):
        searchdate = response.xpath('//*[@id="pnlResult"]/h2/span/text()')[0].extract().split(' ')[1].replace('/','')
        strtodate = datetime.strptime(searchdate, '%Y%m%d')        
        market = response.url.split('/')[-1].split('=')[1]
        for row in response.xpath('//*[@id="mutualmarket-result"]//tbody//tr'):
            if strtodate.isoweekday() == 6:
                continue

            if row.css('.col-stock-code div::text') is not None:
                item = StockItem()
                item['date'] = searchdate
                item['market'] = market
                item['stockcode'] = row.css('.col-stock-code div::text')[1].extract()
                item['stockname'] =  row.css('.col-stock-name div::text')[1].extract()
                item['shareholding'] =  row.css('.col-shareholding div::text')[1].extract()
                #item['shareholdingpercent'] =  row.css('.col-shareholding-percent div::text')[1].extract()
                if len(row.css('.col-shareholding-percent div::text')) >= 2:
                    item['shareholdingpercent'] =  row.css('.col-shareholding-percent div::text')[1].extract()
                else:
                    item['shareholdingpercent'] = '0%'
                yield item
        
        parsedate = (datetime.strptime(searchdate, '%Y%m%d') - timedelta(1)).strftime('%Y/%m/%d')

        if parsedate >= '2020/08/03':
            print(parsedate)
            yield scrapy.FormRequest(
                url = response.url,
                formdata = {
                    '__VIEWSTATE':response.xpath('//*[@id="__VIEWSTATE"]/@value')[0].extract(),
                    '__VIEWSTATEGENERATOR':response.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0].extract(),
                    '__EVENTVALIDATION':response.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0].extract(),
                    'today':str(datetime.today().strftime('%Y%m%d')),
                    'sortBy': 'stockcode',
                    'sortDirection':'asc',
                    'txtShareholdingDate': parsedate,
                    'btnSearch':'搜尋'
                },
                callback=self.parse
            )

    def after_post(self, response):
        searchdate = response.xpath('//*[@id="pnlResult"]/h2/span/text()')[0].extract().split(' ')[1].replace('/','')
        strtodate = datetime.strptime(searchdate, '%Y%m%d')
        market = response.url.split('/')[-1].split('=')[1]
        for row in response.xpath('//*[@id="mutualmarket-result"]//tbody//tr'):
            if strtodate.isoweekday() == 6:
                continue

            if row.css('.col-stock-code div::text') is not None:
                item = StockItem()
                item['date'] = searchdate
                item['market'] = market
                item['stockcode'] = row.css('.col-stock-code div::text')[1].extract()
                item['stockname'] =  row.css('.col-stock-name div::text')[1].extract()
                item['shareholding'] =  row.css('.col-shareholding div::text')[1].extract()
                #item['shareholdingpercent'] =  row.css('.col-shareholding-percent div::text')[1].extract()
                if len(row.css('.col-shareholding-percent div::text')) >= 2:
                    item['shareholdingpercent'] =  row.css('.col-shareholding-percent div::text')[1].extract()
                else:
                    item['shareholdingpercent'] =  '0%'
                yield item

