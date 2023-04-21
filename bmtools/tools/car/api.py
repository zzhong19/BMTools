from .utils import *
from ..tool import Tool
import requests
from bs4 import BeautifulSoup

def build_tool(config) -> Tool:
    tool = Tool(
        "Car Info",
        "Look up Car information",
        name_for_model="Car",
        description_for_model="Plugin for look up Car information",
        logo_url="https://cdn.weatherapi.com/v4/images/weatherapi_logo.png", #TODO
        contact_email="hello@contact.com",
        legal_info_url="hello@legal.com"
    )

    '''
    @tool.get("/get_car_info")
    def get_car_info(name : str = '奔驰GLC'):
        start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]
        for url in start_urls:
          response = requests.get(url)
          soup = BeautifulSoup(response.text, 'html.parser')
          lis = soup.findAll('li', attrs={'id' : True})
          for li in lis:
            car_name = li.find('a').text
            if name.strip().lower().replace(' ', '') in car_name.strip().lower().replace(' ', '') or car_name.strip().lower().replace(' ', '') in name.strip().lower().replace(' ', ''):
                id = li.get('id')[1:]
                car_url = 'https://www.autohome.com.cn/' + id + '/#pvareaid=3311672'
                car_response = requests.get(car_url)
                car_soup = BeautifulSoup(car_response.text, 'html.parser')
                dds = car_soup.findAll('dd')
                for dd in dds:
                  if dd.find('a', {'class': 'name'}):
                    spec_url = 'https://www.autohome.com.cn' + dd.find('a', {'class': 'name'}).get('href')
                    spec_response = requests.get(spec_url)
                    spec_soup = BeautifulSoup(spec_response.text, 'html.parser')
                    output = {}
                    output['车辆名称'] = ''.join(spec_soup.find('div', {'class': 'athm-sub-nav__car__name'}).find('a').text).strip()
                    # output['车辆全称'] = spec_soup.find('div', {'class': 'information-tit'}).find('h2').text
                    output['价格区间'] = car_soup.find('a', {'class': 'emphasis'}).text
                    output['级别'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[0].find('p').text
                    output['排量'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[1].find('p').text
                    output['最大功率'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[2].find('p').text
                    output['最大扭矩'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[3].find('p').text
                    output['变速箱'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[4].find('p').text
                    output['综合油耗'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[5].find('p').text
                    output['环保标准'] = spec_soup.find('div', {'class': 'param-list'}).findAll('div')[6].find('p').text
                    return output
    '''
    @tool.get("/get_car_description")
    def get_car_description(name : str = '奔驰GLC'):
        start_urls = ['http://www.autohome.com.cn/grade/carhtml/%s.html' % chr(ord('A') + i) for i in range(26)]
        for url in start_urls:
          response = requests.get(url)
          soup = BeautifulSoup(response.text, 'html.parser')
          lis = soup.findAll('li', attrs={'id' : True})
          for li in lis:
            car_name = li.find('a').text
            if name.strip().lower().replace(' ', '') in car_name.strip().lower().replace(' ', '') or car_name.strip().lower().replace(' ', '') in name.strip().lower().replace(' ', ''):
                id = li.get('id')[1:]
                car_url = 'https://www.autohome.com.cn/' + id + '/#pvareaid=3311672'
                car_response = requests.get(car_url)
                car_soup = BeautifulSoup(car_response.text, 'html.parser')
                article = car_soup.find('div', {'class', 'athm-sub-nav__channel athm-js-sticky'}).find('ul').findAll('li')[6]
                article_url = 'https://www.autohome.com.cn' + article.find('a').get('href')
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                pages = article_soup.findAll('p', {'class' : 'info-tx'})
                for page in pages:
                  if name.lower().replace(' ', '') in page.text.lower().replace(' ', ''):
                    page_url = 'https://www.autohome.com.cn' + page.find('a').get('href')
                    if 'news' in page_url:
                      print(page_url)
                      page_response = requests.get(page_url)
                      page_soup = BeautifulSoup(page_response.text, 'html.parser')
                      content = page_soup.find('div', {'id': 'articleContent'})
                      paragraph = content.findAll('p')
                      output = ""
                      for p in paragraph:
                        output += p.text
                      output = output.replace('\xa0','').replace('\u3000','').strip()
                      if '新车' in output:
                        if '（文/汽车之家' in output:
                          output = output.split('（文/汽车之家',1)[0]
                        return output

    '''  
    @tool.get("/get_car_list")
    def get_car_list(name : str = 'SUV', price : str = '90'):
        items = []
        runner = CrawlerRunner()
        crawler = runner.create_crawler(CarSpider)
        d = crawler.crawl(FindCarSpider, input='inputargument', vehicle_type=name, price=price, items = items)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        # process.start()
        if not items:
            # text_output = "没有找到此车型在价格区间的车辆"
            output = {}
        else:
            output = items[0]
            # text_output = f"以下是此车型在价格区间的车辆: \n"+", ".join([f"{key}: {output[key]}" for key in output.keys()])
        return output
    
    @tool.get("/get_car_rating")
    def get_car_rating(name : str = '奔驰GLC'):
        items = []
        runner = CrawlerRunner()
        crawler = runner.create_crawler(CarSpider)
        d = crawler.crawl(RatingSpider, input='inputargument', car=name, items = items)
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        # process.start()
        if not items:
            # text_output = "没有找到该车辆的评分"
            output = {}
        else:
            output = items[0]
            # text_output = f"以下是该车辆的评分: \n"+", ".join([f"{key}: {output[key]}" for key in output.keys()])
        return output
    
    @tool.get("/get_brand_info")
    def get_brand_info(name : str = '奔驰'):
        items = []
        process = CrawlerRunner()
        process.crawl(BrandSpider, input='inputargument', brand=name, items = items)
        process.start()
        if not items:
            # text_output = "没有找到该品牌的信息"
            output = {}
        else:
            output = items[0]
            # text_output = f"以下是该品牌的信息: \n"+", ".join([f"{key}: {output[key]}" for key in output.keys()])
        return output
    '''
    return tool
