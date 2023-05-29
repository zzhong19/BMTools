from ..tool import Tool
import requests
from bs4 import BeautifulSoup
import re

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

    @tool.get("/get_car_description")
    def get_car_desc(name : str = '奔驰GLC'):
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
                if car_soup.find('div', {'class', 'athm-sub-nav__channel athm-js-sticky'}):
                  article = car_soup.find('div', {'class', 'athm-sub-nav__channel athm-js-sticky'}).find('ul').findAll('li')[6]
                  article_url = 'https://www.autohome.com.cn' + article.find('a').get('href')
                else:
                  article = car_soup.find('div', {'class', 'models_nav'}).findAll('a')[3]
                  article_url = 'https://www.autohome.com.cn/' + article.get('href')
                article_response = requests.get(article_url)
                article_soup = BeautifulSoup(article_response.text, 'html.parser')
                pages = article_soup.findAll('p', {'class' : 'info-tx'})
                for page in pages:
                  page_url = 'https://www.autohome.com.cn' + page.find('a').get('href')
                  page_response = requests.get(page_url)
                  page_soup = BeautifulSoup(page_response.text, 'html.parser')
                  content = page_soup.find('div', {'id': 'articleContent'})
                  if content:
                    paragraph = content.findAll('p')
                    output = ""
                    for p in paragraph:
                      output += p.text
                    output = output.replace('\xa0','').replace('\u3000','').strip()
                    if '专业评测]' in output or '新车上市]' in output or '购车手册]' in output or '原创试驾]' in output:
                      if '（文/汽车之家' in output:
                        output = output.split('（文/汽车之家',1)[0]
                      if '（图片来源' in output:
                        output = output.split('（图片来源',1)[0] 
                      return output
    '''
    @tool.get("/suggest_car_names_given_vehicle_type_and_price")               
    def suggest_car_names_given_vehicle_type_and_price(name : str = 'SUV', price : str = '90'):
        start_url = 'https://www.autohome.com.cn/car/'
        if '-' in price:
          price = price.replace('-', '_')
          if '万' in price:
            price = price.replace('万', '')
        else:
          price = re.findall(r'\d+', price)[0]
          if int(price) > 10000:
            price = str(int(int(price) / 10000))
          price = price + '_' + price
        print(price)
        response = requests.get(start_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        all = soup.findAll('a', {'target': '_self'})
        for a in all:
          car_type = a.text
          if car_type.strip() == '':
            continue
          if name.strip().lower().replace(' ', '') in car_type.strip().lower().replace(' ', '') or car_type.strip().lower().replace(' ', '') in name.strip().lower().replace(' ', ''):
            car_url = 'https://www.autohome.com.cn' + a.get('href')
            if '/0_0' in car_url:
              car_url = car_url.replace('/0_0', '/' + price)
            else:
              car_url = car_url + price + '-0.0_0.0-0-0-0-0-0-0-0-0/'
            try:
              car_response = requests.get(car_url)
              car_soup = BeautifulSoup(car_response.text, 'html.parser')
              output = []
              uls = car_soup.findAll('ul', {'class': 'rank-list-ul'})
              for ul in uls:
                output.append(ul.find('li').find('h4').find('a').text)
              return output
            except:
              continue
    '''
    return tool
