# coding= utf-8
from spider_domain import *
from selenium import webdriver
lis = []

def getCity(name):

    try:
        browser = webdriver.Chrome('./chromedriver.exe')
        # browser = webdriver.Chrome()
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
            print(lis)
            return lis
        else:
            return None
    except:
        return None
    finally:
        browser.quit()


if __name__ == "__main__":
    print('默认地点为北京市')
    while True:
        filename = input("保存文件名必选*(不用文件后缀)>> ")
        if (filename != ""): break
    while True:
        addr = input('输入地址 >> ')
        lis = addr.split(",")
        if lis == ['']:
            lis=['北京']
        if len(lis) != 0:
            addrs = getCity(lis[0])
        if (addrs != None): break
        print('输入地点有误,请重新再输入')
    if (len(addrs) != 2): sys.exit(1)

    #以上代码为获取地表经纬度
    #以下为爬虫部分


    smain.start(addrs,filename,lis)