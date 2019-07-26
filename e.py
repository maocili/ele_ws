import time, sys, re
# import json
# import requests
# import xlwt
# from requests.cookies import RequestsCookieJar
# from selenium import webdriver
from spider_domain import *
lis = []


class e():
    def __init__(self, fileName):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "x-shard": '',
            "referer": "https://h5.ele.me/",
            "Accept-Encoding": 'gzip'
        }
        self.item_url = "http://h5.ele.me/restapi/shopping/v3/restaurants?latitude={latitude}&longitude={longitude}&offset={offset}&{limit}=10"
        self.count = 1
        self.worksheet = xlwt.Workbook(encoding='utf-8', style_compression=0)
        self.fileName = fileName
        self.index = 1
        self.logoUrl = 'https://fuss10.elemecdn.com/{s1}/{s2}/{s3}.{s4}?imageMogr/format/webp/thumbnail/!130x130r/gravity/Center/crop/130x130/'
        self.commentUrl = 'http://h5.ele.me/pizza/ugc/restaurants/{id}/batch_comments?has_content=false&offset=0&limit=1&terminal=android'
        self.status = False
        self.tryCount = 0
        self.proxy = {'http': ''}
        self.proxyUrl = 'https://proxyapi.mimvp.com/api/fetchopen.php?orderid=860205480104102292&num=1&http_type=1&anonymous=3&request_method=3&result_fields=1,2&result_format=json'
        self.currentIndex = 0
        self.session = requests.session()

    def read_cookies_file(self):
        try:
            self.cookies_dict = dict()
            with open("cookies.txt", "r") as fp:
                cookies = json.load(fp)
                for cookie in cookies:
                    self.cookies_dict[cookie['name']] = cookie['value']
            return True
        except:
            return False

    def parse_item(self, j):
        for i in j['items']:
            item = {}
            ii = i['restaurant']
            item['商家id'] = ii['id']
            item['商家名称'] = ii['name']
            item['商家地址'] = ii['address']
            item['营业时间'] = ','.join(ii['opening_hours']).replace('/', '-')
            item['配送费'] = ii['piecewise_agent_fee']['tips']
            item['月销售'] = ii['recent_order_num']
            send = ii['piecewise_agent_fee']['rules']
            send = dict(send[0])
            item['起送价'] = "￥%d" % send['price']
            item['配送价'] = '￥' + str(send['fee'])
            item['平均送餐时间'] = str(ii['order_lead_time']) + '分钟'
            item['商家评分'] = ii['rating']
            item['是否是新店'] = '是' if ii['is_new'] else '否'
            item['类别'] = ''
            for j in ii['flavors']:
                item['类别'] += j['name'] + '|'
            item['商家电话'] = ii['phone']
            item['是否是推荐'] = '是' if ii['is_star'] else '否'
            item['经纬度'] = str(ii['latitude']) + ',' + str(ii['longitude'])
            item['是否品牌店'] = '是' if ii['is_premium'] else '否'
            business_info = ii['business_info']
            item['商家活动'] = ','.join(re.findall('"text": "(.*?)"', business_info))
            s = ii['image_path']
            logoDict = {
                "s1": s[0:1],
                's2': s[1:3],
                's3': s[3:],
                's4': 'png' if s[-3:] == 'png' else 'jpeg'
            }
            item['商家logo'] = self.logoUrl.format(**logoDict)
            try:
                item['配送方式'] = ii['delivery_mode']['text']
            except:
                item['配送方式'] = '商家配送'

            # self.parse_comment(item)
            self.save_item(item)

    def parse_comment(self, item, s=None):
        '''
        爬取评论数量
        '''
        time.sleep(8)
        self.header['x-shard'] = 'shopid=' + item['商家id']
        if (s == None):
            s = requests.get(self.commentUrl.format(id=item['商家id']), headers=self.header)
        j = json.loads(s.text)
        try:
            item['评论总数'] = j['tags'][0]['count']
        except KeyError:
            for i in range(20):
                time.sleep(0.5)
                try:
                    print('使用代理')
                    time.sleep(20)
                    self.getProxyIp()
                    # self.header['user-agent'] = UserAgent(verify_ssl=False).random
                    s = requests.get(self.commentUrl.format(id=item['商家id']), headers=self.header, proxies=self.proxy,
                                     timeout=5)
                    if s.status_code == 200:
                        self.parse_comment(item, s)
                        break
                except Exception as e:
                    print(e)
                    print('尝试', i)
            else:
                self.status = True
                print('代理获取失败')
                sys.exit(1)

        self.save_item(item)

    def getProxyIp(self):
        res = requests.get(self.proxyUrl)
        j = json.loads(res.text)
        time.sleep(0.5)
        if j['code'] == 0:
            self.proxy['http'] = j['result'][0]['ip:port']
            return True
        elif j['code'] == "14":
            print('检查到代理提取过快,5分钟后自动提取')
            time.sleep(300)
            self.getProxyIp()
        else:
            return False

    def parse_goodz(self, offset, latitude=30.232436, longitude=120.127921):
        data = {
            'latitude': str(latitude),
            'longitude': str(longitude),
            'offset': str(offset),
            'limit': str(30),
        }
        time.sleep(8)
        if self.proxyKK():
            res = requests.get(self.item_url.format(**data), headers=self.header, cookies=self.cookies_dict,
                               proxies=self.proxy)
        else:
            res = requests.get(self.item_url.format(**data), headers=self.header, cookies=self.cookies_dict)
        j = json.loads(res.text)
        try:
            if j['name'] == 'UNAUTHORIZED':
                print('cookies 失效了')
                self.getCookie()
                self.read_cookies_file()
                for i in range(3):
                    if self.proxyKK():
                        res = self.session.get(self.item_url.format(**data), headers=self.header,
                                               cookies=self.cookies_dict, proxies=self.proxy)
                    else:
                        res = requests.get(self.item_url.format(**data), headers=self.header, cookies=self.cookies_dict)
                    j = json.loads(res.text)
                    print('尝试', i)

                    try:
                        if j['name'] == 'UNAUTHORIZED':
                            print('cookies 失效了')
                            self.getCookie()
                            self.read_cookies_file()
                        else:
                            break
                    except:
                        break
                else:
                    self.status = True
                    print('cookies  获取次数过多')
                    sys.exit(1)
        except:
            pass

        self.parse_item(j)
        if not j['has_next']:
            print('爬取完成')
            self.save_xls()
            self.currentIndex += 1
            if len(lis) == self.currentIndex:
                self.status = True
                sys.exit(1)
            else:
                if lis[self.currentIndex] == '':
                    self.currentIndex += 1
                addrs = getCity(lis[self.currentIndex])
                next(self, addrs)

    def excel_full(self):
        if self.count >= 65535:
            self.sheet = self.worksheet.add_sheet(self.fileName + str(self.index))
            self.index += 1
            self.count = 1

    def save_item(self, content):
        content['爬取时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content['关键字'] = lis[self.currentIndex]
        c = 0
        print(content)
        for key in content:
            if self.count == 1:
                self.sheet.write(0, c, key)
            self.sheet.write(self.count, c, label=content[key])
            c += 1
        self.count += 1
        print('当前爬取个数', self.count)
        self.excel_full()
        self.save_xls()

    def save_xls(self):
        self.worksheet.save(self.fileName + '.xls')

    def getCookie(self, mode=0, info={}):
        while True:
            mobile_phone = input('输入手机号 >> ')
            p2 = re.compile(r'^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
            phonematch = p2.match(mobile_phone)
            if (phonematch): break
            print('输入手机号有误,请重新再输入')
        self.login_View(mobile_phone)

    def randomUserAgent(self):
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

    def login_View(self, mobile_phone):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent="' + self.randomUserAgent() + '"')
        # browser = webdriver.Chrome('./chromedriver.exe', chrome_options=options)
        browser = webdriver.Chrome(chrome_options=options)
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
        if (str(index_url) in ('https://h5.ele.me/msite/')):
            with open("cookies.txt", "w") as fp:
                json.dump(cookies, fp)
            print('cookies文件保存成功')
            # start(cookies)
            self.read_cookies_file()

        else:
            print('登录失败')
            self.login_View(mobile_phone)

    def proxyKK(self):
        return False
        res = requests.get('http://kps.kdlapi.com/api/getkps/?orderid=994832645898416&num=1&pt=1&format=json&sep=1')
        j = json.loads(res.text)
        if j['code'] == 0:
            self.proxy['http'] = j['data']['proxy_list'][0]
            return True
        else:
            return False

    def start(self, lat=39.881552, lng=116.435508):
        lat = str('%.6f' % float(lat))
        lng = str('%.6f' % float(lng))
        if (not self.read_cookies_file()):
            # 无法获得cookie文件

            self.getCookie()
            pass
        if self.currentIndex == 0:
            self.sheet = self.worksheet.add_sheet(self.fileName, cell_overwrite_ok=True)
        self.page = 0
        while True:
            try:
                self.parse_goodz(self.page * 30, latitude=lat, longitude=lng)
                self.page += 1
                self.tryCount = 0
            except PermissionError:
                print('该Excel已经被打开')
                input('>>')
                sys.exit(1)
            except:
                if self.status: sys.exit(0)
                self.tryCount += 1
                if (self.tryCount >= 10):
                    sys.exit(1)
                self.getCookie()
                self.parse_goodz(self.page * 30, latitude=lat, longitude=lng)
                self.page += 1
            finally:
                self.save_xls()


def getCity(name):
    try:
        # browser = webdriver.Chrome('./chromedriver.exe')
        browser = webdriver.Chrome()
        browser.get('http://www.gpsspg.com/maps.htm')
        # btn = browser.find_element_by_xpath('//a[@id="sm_1"]')
        # btn.click()
        time.sleep(3)
        element = browser.find_element_by_xpath('//input[@type="text"]')
        element.send_keys(name)
        time.sleep(1)
        sub_btn = browser.find_element_by_xpath('//input[@id="s_btn"]')
        sub_btn.click()
        time.sleep(4)
        value = browser.find_element_by_xpath('//span[@id="curr_xy"]')
        location = value.text
        if location != None:
            location = str(location)
            location = location.replace('北纬', ',')
            location = location.split(',')
            lis = []
            lis.append(location[0].strip())
            lis.append(location[1].strip())
            return lis
        else:
            return None
    except:
        return None
    finally:
        browser.quit()
        # browser.close()


def next(e, addrs):
    lat = addrs[0]
    lng = addrs[1]
    e.start(lat, lng)


if __name__ == "__main__":
    print('默认地点为北京市')
    while True:
        filename = input("保存文件名必选*(不用文件后缀)>> ")
        if (filename != ""): break
    while True:
        addr = input('输入地址 多个地址以英文逗号分隔>> ')
        lis = addr.split(",")
        if len(lis) != 0:
            addrs = getCity(lis[0])
        if (addrs != None): break
        print('输入地点有误,请重新再输入')

    if (len(addrs) != 2): sys.exit(1)

    e = e(filename)
    next(e, addrs)
