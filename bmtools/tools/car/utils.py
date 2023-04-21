#coding=utf- 8
import scrapy

class InfoItem(scrapy.Item):
    vehicle_specification = scrapy.Field() # 车辆全称（带配置）
    vehicle_name = scrapy.Field()   # 车辆名称
    factory_price = scrapy.Field()  # 厂商指导价
    dealer_price = scrapy.Field()  # 经销商指导价
    vehicle_type = scrapy.Field()  # 车辆类型
    emission_standard = scrapy.Field()  # 环保标准
    max_power = scrapy.Field()  # 最大功率
    max_torque = scrapy.Field() # 最大扭矩
    gearbox_type = scrapy.Field()  # 变速箱类型
    fuel_consumption = scrapy.Field()    # 综合油耗(L/100km)
    engine_displacement = scrapy.Field()   # 引擎排量

class CarSpider(scrapy.Spider):
    name = 'car_spider'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        lis = response.xpath('body/dl//ul//li')
        ids = response.xpath('body/dl//ul//li/@id')
        names = response.xpath('body/dl//ul//li/h4/a/text()').extract()
        select_ids = []
        for li in lis:
            name = li.xpath('h4/a/text()').extract()
            if len(name) == 1:
                if self.car.strip().lower().replace(' ', '') in name[0].strip().lower().replace(' ', '') or name[0].strip().lower().replace(' ', '') in self.car.strip().lower().replace(' ', ''):
                    print(name[0])
                    select_id = li.xpath('@id')
                    select_ids.append(select_id[0])

        for id in select_ids:
            url = 'https://www.autohome.com.cn/' + id.extract()[1:] + '/#pvareaid=3311672'
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_next_page, dont_filter=True)

    def parse_next_page(self, response):
        for id in response.xpath('//dd//a[@class="name"]/@href').extract():
            url = 'https://www.autohome.com.cn' + id
            yield scrapy.Request(url=url, callback=self.parse_config_page, dont_filter=True)

    def parse_config_page(self, response):
        item = InfoItem()
        try:
            item['vehicle_specification'] = ''.join(response.xpath('//div[@class="athm-sub-nav__car__name"]/a//text()').extract()).strip()
            item['vehicle_name'] = response.xpath('//div[@class="information-tit"]/h2/text()').extract_first()
            item['factory_price'] = ''.join(response.xpath('//a[@id="cityDealerPrice"]//text()').extract()).strip()
            item['dealer_price'] = ''.join(response.xpath('//dl[@class="information-other"]/dd/div[@class="con"]//text()').extract()[:3]).strip()

            item['vehicle_type'] = response.xpath('//div[@class="param-list"]/div[1]/p/text()').extract_first() 
            item['engine_displacement'] = response.xpath('//div[@class="param-list"]/div[2]/p/text()').extract_first()
            item['max_power'] = response.xpath('//div[@class="param-list"]/div[3]/p/text()').extract_first()
            item['max_torque'] = response.xpath('//div[@class="param-list"]/div[4]/p/text()').extract_first()
            item['gearbox_type'] = response.xpath('//div[@class="param-list"]/div[5]/p/text()').extract_first()
            item['fuel_consumption'] = response.xpath('//div[@class="param-list"]/div[6]/p/text()').extract_first()
            item['emission_standard'] = response.xpath('//div[@class="param-list"]/div[7]/p/text()').extract_first()
            self.items.append(item)
            yield item
        except:
            pass

class ListItem(scrapy.Item):
    vehicle_names = scrapy.Field() # 车辆名称

class FindCarSpider(scrapy.Spider):
    name = 'FindCar_spider'
    start_urls = ['https://www.autohome.com.cn/d/1_1-0.0_0.0-0-0-0-0-0-0-0-0/']

    def parse(self, response):
        rows = response.xpath('/html/body/div[2]/div[4]/div/div[1]/div[2]/div[1]/dl/dd/a')
        # print(rows)
        for row in rows:
            name = row.xpath('span/text()').extract()
            # print(name)
            if len(name) == 1:
                if self.vehicle_type.strip().lower().replace(' ', '') in name[0].strip().lower().replace(' ', ''):
                    url = 'https://www.autohome.com.cn' + row.xpath('@href').extract_first()
                    url = url.replace('1', self.price)
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse_vehicles, dont_filter=True)
    
    def parse_vehicles(self, response):
        item = ListItem()
        try:
            item['vehicle_names'] = response.xpath('//ul[@class="rank-list-ul"]/li/h4/a/text()').extract() 
            self.items.append(item)
            yield item
        except:
            pass

class RatingItem(scrapy.Item):
    overall_score = scrapy.Field() # 口碑评分
    space = scrapy.Field() # 空间
    driving_feel = scrapy.Field()   # 驾驶感受
    fuel_consumption = scrapy.Field()    # 综合油耗(L/100km)
    exterior = scrapy.Field()  # 外观
    interior = scrapy.Field()  # 内饰
    features = scrapy.Field()  # 配置

class RatingSpider(scrapy.Spider):
    name = 'Rating_spider'
    start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]

    def parse(self, response):
        lis = response.xpath('body/dl//ul//li')
        ids = response.xpath('body/dl//ul//li/@id')
        names = response.xpath('body/dl//ul//li/h4/a/text()').extract()
        select_ids = []
        for li in lis:
            name = li.xpath('h4/a/text()').extract()
            if len(name) == 1:
                if self.car.strip().lower().replace(' ', '') in name[0].strip().lower().replace(' ', ''):
                    print(name[0])
                    select_id = li.xpath('@id')
                    print(select_id[0])
                    select_ids.append(select_id[0])

        for id in select_ids:
            url = 'https://www.autohome.com.cn/' + id.extract()[1:] + '/#pvareaid=3311672'
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_next_page, dont_filter=True)
    
    def parse_next_page(self, response):
        for id in response.xpath('//dd//a[@class="name"]/@href').extract():
            url = 'https://www.autohome.com.cn' + id
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_rating_page, dont_filter=True)

    def parse_rating_page(self, response):
        for url in response.xpath('//div[@class="koubei-title__more"]/a/@href').extract():
            url = 'https:' + url
            print(url)
            yield scrapy.Request(url=url, callback=self.parse_config_page, dont_filter=True)

    def parse_config_page(self, response):
        item = RatingItem()
        # attributes = response.xpath('//ul[@class="score_tag__Wq2Z4"]/li/div/text()').extract_first() 
        # print(attributes)
        try:
            item['overall_score'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() 
            item['space'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            item['driving_feel'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            item['fuel_consumption'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            item['exterior'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            item['interior'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            item['features'] = response.xpath('//div[@class="score_star__yBrf7"]/em/text()').extract_first() #TODO
            self.items.append(item)
            yield item
        except:
            pass

class BrandItem(scrapy.Item):
    name = scrapy.Field() # 品牌名称
    ranking = scrapy.Field() # 排名
    country = scrapy.Field()   # 国别
    sales = scrapy.Field()    # 销量
    market_share = scrapy.Field()  # 占品牌份额

class BrandSpider(scrapy.Spider):
    name = 'Brand_spider'
    start_urls = ['https://xl.16888.com/brand-1.html', 'https://xl.16888.com/brand-2.html']

    def parse(self, response):
        rows = response.xpath('.//tr')
        print(rows)
        for row in rows:
            name = row.xpath('td[3]/a/text()').extract()
            if len(name) == 1:
                if self.brand.strip().lower().replace(' ', '') in name[0].strip().lower().replace(' ', ''):
                    print(name[0])
                    item = BrandItem()
                    try:
                        item['name'] = name[0]
                        item['ranking'] = row.xpath('td[1]/text()').extract_first()
                        item['country'] = row.xpath('td[4]/text()').extract_first()
                        item['sales'] = row.xpath('td[5]/text()').extract_first()
                        item['market_share'] = row.xpath('td[6]/text()').extract_first()
                        self.items.append(item)
                        yield item
                    except:
                        pass
