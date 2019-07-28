# coding=utf-8
import json
import os
import sys
import time
import requests
from selenium import webdriver
from spider_domain.save_excel import save_excel
from spider_domain.more_xz import *

header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
logo_url = 'https://fuss10.elemecdn.com/{s1}/{s2}/{s3}.{s4}?imageMogr/format/webp/thumbnail/!130x130r/gravity/Center/crop/130x130/'


# def build(text):
#     cookie = ''
#     for i in text:
#         cookie += i['name']+'='+i['value']+';'
#     return cookie


def randomUserAgent():
    headers = [
        'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 8.1.0; ALP-AL00 Build/HUAWEIALP-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)',
        'Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.10 (Baidu; P1 6.0.1)',
        'Mozilla/5.0 (Linux; Android 8.1.0; PACM00 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.1.0)',
        'Mozilla/5.0 (Linux; Android 7.1.1; OPPO R11 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 7.1.1)',
        'Mozilla/5.0 (Linux; Android 5.1.1; OPPO R9 Plustm A Build/LMY47V; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.12 baiduboxapp/10.12.0.12 (Baidu; P1 5.1.1)',
        'Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/48.0.2564.116 Mobile Safari/537.36 T7/9.1 baidubrowser/7.18.21.0 (Baidu; P1 6.0.1)',
        'Mozilla/5.0 (Linux; Android 6.0.1; OPPO A57 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 6.0.1)',
        'Mozilla/5.0 (Linux; Android 6.0.1; OPPO R9s Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 6.0.1)',
        'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; OPPO R7s Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)',
        'Mozilla/5.0 (Linux; Android 8.0.0; SM-N9500 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)',
        'Mozilla/5.0 (Linux; Android 7.0; SM-G9208 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/7.4 baiduboxapp/8.2.5 (Baidu; P1 7.0)',
        'Mozilla/5.0 (Linux; U; Android 5.1; zh-CN; m2 note Build/LMY47D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/10.9.2.712 U3/0.8.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 5.1; zh-cn; m2 note Build/LMY47D) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.8 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1',
        'Mozilla/5.0 (Linux; Android 8.0.0; MI 6 Build/OPR1.170623.027) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36 Maxthon/3235',
        'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.2.2',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.8.2 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1'
    ]
    return headers[int(time.time()) % len(headers)]


def login_View(mobile_phone):
    options = webdriver.ChromeOptions()
    options.add_argument('user-agent="' + randomUserAgent() + '"')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    browser = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
    # browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://h5.ele.me/login/')
    time.sleep(5)
    element = browser.find_element_by_xpath('//input[@maxlength=11]')
    element.send_keys(mobile_phone)
    time.sleep(1)
    sub_btn = browser.find_element_by_xpath("//button[@class='CountButton-3e-kd']")
    sub_btn.click()
    print('请手动输入验证码，然后确定，时间40秒')
    input('跳转到首页按回车>>')
    print(browser.current_url)
    index_url = browser.current_url
    cookies = browser.get_cookies()
    browser.quit()
    # browser.close()
    # print(cookies)
    if (str(index_url) in ('https://h5.ele.me/msite/')):
        with open("cookies.txt", "w") as fp:
            json.dump(cookies, fp)
        print('cookies文件保存成功')
        # self.read_cookies_file()
        return cookies
    else:
        print('登录失败')
        login_View(mobile_phone)


def build_cookie(cookie_list):
    # print(cookie_list)
    cookie_context = ''
    for i in cookie_list:
        cookie_context += i['name'] + '=' + i['value'] + '; '
    cookie = {
        'cookie': cookie_context
    }
    return cookie


def get_rank_id(cookies, xz):
    # 通过cookie获取所有的店铺信息
    # https://h5.ele.me/restapi/shopping/v3/restaurants?
    # latitude=39.910352&longitude=116.410882&offset=8&
    # limit=8&extras[]=activities&extras[]=tags&extra_filters=home&rank_id=b83075d8743b4f879c3f4c9d49fd113e&terminal=h5
    print(cookies)
    print(xz)
    data = {
        'latitude': xz[0],
        'longitude': xz[1],
        'offset': 0,
        'limit': 10,
        'rank_id': ''
    }

    URL = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit={limit}&extras[]=activities&extras[]=tags&extra_filters=home&rank_id={rank_id}&terminal=h5'.format(
        **data)
    print(URL)
    # URL='https://h5.ele.me/restapi/shopping/v3/restaurants'
    flag = 3
    while flag >= 0:
        html = requests.get(url=URL, cookies=cookies, headers=header)
        print('获取列表', html.text)
        if (html.status_code != 200):
            #如果不为200，直接重新尝试获取列表
            print('账号获取失败')
            time.sleep(1)
            flag-=1
            break
        json_context = json.loads(html.text)
        print(json_context)
        try:
            #如取到rank id直接返回
            ret_data = json_context['meta']['rank_id']
            flag = -1
            return ret_data
        except Exception as e:
            print('账号登陆失败(正在重试)', flag)
            time.sleep(1)
            flag -= 1
    input('账号登陆失败(回车结束)')
    sys.exit(1)



def get_shop_list(cookies, xz):
    # 商家id 商家名称 商家地址 营业时间 配送费 月销量 起送价 配送价 平均送餐时间 商家评分 是否是新店 类别 商家电话 是否推荐 经纬度 是否品牌 商家活动 商家logo 配送方式 爬取时间
    RANK_ID = get_rank_id(cookies, xz)
    FLAG = True
    data = {
        'latitude': xz[0],
        'longitude': xz[1],
        'offset': 0,
        'limit': 30,
        'rank_id': RANK_ID
    }
    while FLAG:
        URL = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&limit={limit}&extras[]=activities&extras[]=tags&extra_filters=home&rank_id={rank_id}&terminal=h5'.format(
            **data)
        # print('条目',data['offset'])
        html = requests.get(url=URL, cookies=cookies, headers=header)
        print(html.status_code)
        if html.status_code != 200:
            # FLAG = False
            # data = {
            #     'latitude': xz[0],
            #     'longitude': xz[1],
            #     'offset': 0,
            #     'limit': 30,
            #     'rank_id': RANK_ID
            # }
            break
        if json.loads(html.text)['has_next']:
            with open("spider_domain\shop_list.json", "a", encoding='utf-8') as fp:
                fp.writelines(html.text + '\n')
            data['offset'] += 30
        else:
            FLAG = False
            break




def anazly_json(filename, cookies, xz,lis):
    # 商家地址  商家电话
    '''
    #https://h5.ele.me/restapi/booking/v1/cart_client
    # {sub_channel: "", business_type: 0, geohash: "wtmkmcgf5tv4", user_id: 175546728, add_on_type: 0,…}
    # add_on_type: 0
    # additional_actions: [71]
    # business_type: 0
    # come_from: "mobile"
    # entities: [[,…]]
    # entities_with_ingredient: [[]]
    # geohash: "wtmkmcgf5tv4"
    # operating_sku_ids: []
    # packages: [[]]
    # restaurant_id: "E15161045254581752312"
    # sub_channel: ""
    # tying_sku_entities: [[]]
    # user_id: 175546728
    '''
    with open(os.path.split(os.path.realpath(__file__))[0] + '/shop_list.json', 'r', encoding='utf-8')as f:
        file = f.readlines()
    for i in file:
        json_list = json.loads(i)
        for item in json_list['items']:
            shop_info = {}
            # 商户id
            shop_info['商户id'] = item['restaurant']['id']
            # 名称
            shop_info['商户名称'] = item['restaurant']['name']
            # 月销量
            shop_info['月销量'] = item['restaurant']['recent_order_num']
            # 配送费 句子
            shop_info['配送费'] = item['restaurant']['piecewise_agent_fee']['description']
            # 起送价
            shop_info['起送价'] = item['restaurant']['float_minimum_order_amount']
            # 配送价 单价格
            shop_info['配送价'] = item['restaurant']['float_delivery_fee']
            # 营业时间
            shop_info['营业时间'] = item['restaurant']['opening_hours'][0]
            # 配送时间
            shop_info['配送时间'] = item['restaurant']['order_lead_time']
            # 商家评分
            shop_info['商家评分'] = item['restaurant']['rating']
            # 是否新店
            shop_info['是否新店'] = item['restaurant']['is_new']
            # 类别
            flavors = ''
            try:
                for flavor in item['restaurant']['flavors']:
                    flavors += flavor['name'] + '|'
            except:
                flavors = ''
            shop_info['类别'] = flavors
            # 经度
            shop_info['经度'] = item['restaurant']['latitude']
            # 维度
            shop_info['维度'] = item['restaurant']['longitude']
            # 是否品牌
            shop_info['是否品牌'] = item['restaurant']['is_premium']
            # 商家活动
            activities = ''
            for activitie in item['restaurant']['activities']:
                activities += activitie['description'] + '|'
            shop_info['商家活动'] = activities
            # 商家logo
            s = item['restaurant']['image_path']
            logoDict = {
                "s1": s[0:1],
                's2': s[1:3],
                's3': s[3:],
                's4': 'png' if s[-3:] == 'png' else 'jpeg'
            }
            shop_info['商家logo'] = logo_url.format(**logoDict)
            # 配送方式
            try:
                shop_info['配送方式'] = item['restaurant']['delivery_mode']['text']
            except:
                shop_info['配送方式'] = '商家配送'
            # 爬取时间
            shop_info['爬取时间'] = time.asctime(time.localtime(time.time()))

            # 店铺url地址item['restaurant']['scheme']
            cart = get_cart_client(item['restaurant']['id'], cookies, xz)  # 商铺地址和电话需要分开进入页面爬取
            if cart['商家地址'] == '' or cart['商家电话'] == '':
                break
            shop_info['商家地址'] = cart['商家地址']
            shop_info['商家电话'] = cart['商家电话']
            print(shop_info['商户id'])
            save_excel(shop_info, filename=filename + '.xls',lis=lis)
    print("完成写入数据")
    os.remove('spider_domain/shop_list.json')


def get_cart_client(id, cookies, xz):
    # 用于获取商铺页面的一些数据

    url = 'https://h5.ele.me/restapi/bgs/poi/reverse_geo_coding?latitude={0}&longitude={1}'.format(xz[0], xz[1])
    issuccess=3
    while issuccess >= 0:
        try:
            geo_html = requests.get(url=url, headers=header, cookies=cookies)
            geo_json = json.loads(geo_html.text)
            issuccess = -1
        except:
            time.sleep(1)
            issuccess -= 1

    geo = geo_json['geohash']
    cart_url = 'https://h5.ele.me/restapi/booking/v1/cart_client'
    data = {
        'add_on_type': '0',
        'additional_actions': [71],
        'business_type': '0',
        'come_from': "mobile",
        'entities': [[]],
        'entities_with_ingredient': [[]],
        'geohash': "wtms7qyr0tq",
        'operating_sku_ids': [],
        'packages': [[]],
        'restaurant_id': id,
        'sub_channel': "",
        'tying_sku_entities': [[]],
    }
    issuccess = 3
    while issuccess >= 0:
        try:
            cart_html = requests.post(url=cart_url, cookies=cookies, data=data)
            cart_dict = json.loads(cart_html.text)
            issuccess = -1
        except:
            time.sleep(1)
            issuccess -= 1
    try:
        ret_data = {'商家地址': cart_dict['cart']['restaurant']['address'],
                    '商家电话': cart_dict['cart']['restaurant']['phone']}
        return ret_data
    except Exception as e:
        print(e)
        time.sleep(1)
        print(cart_html.text)
        return {'商家地址': '', '商家电话': ''}

def start_without_login(xz, filename,lis):

    with open('./cookies.txt','r') as f:
        cookie = f.read()
    #转化为list
    cookie = json.loads(cookie)
    cookies = build_cookie(cookie)

    more_xz = xz_more(xz)
    for index,xz in enumerate(more_xz):
        print('采集:',index)
        get_shop_list(cookies, xz)
    print('完成信息获取，开始分析')
    anazly_json(filename, cookies, xz,lis[0])

def start(xz, filename,lis):
    cookie = ''
    while True:
        # 电话获取cookie
        phone_number = input("输入电话:")
        if len(phone_number) == 11:
            print("您的电话是", phone_number)
            cookie = login_View(phone_number)
            if cookie != '':
                break

    cookies = build_cookie(cookie)

    more_xz = xz_more(xz)
    for index,xz in enumerate(more_xz):
        print('采集:',index)
        get_shop_list(cookies, xz)
    print('完成信息获取，开始分析')
    anazly_json(filename, cookies, xz,lis[0])

# anazly_json('data')
