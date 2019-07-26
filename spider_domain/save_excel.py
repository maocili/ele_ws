# coding=utf-8
import os
import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_xls(path, sheet_name, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlwt.Workbook()  # 新建一个工作簿
    sheet = workbook.add_sheet(sheet_name)  # 在工作簿中新建一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            sheet.write(i, j, value[i][j])  # 像表格中写入数据（对应的行和列）
    workbook.save(path)  # 保存工作簿
    print("xls格式表格初始化写入数据成功！")


def write_excel_xls_append(path, value):
    index = len(value)  # 获取需要写入数据的行数
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(path)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")


def read_excel_xls(path):
    workbook = xlrd.open_workbook(path)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    for i in range(0, worksheet.nrows):
        for j in range(0, worksheet.ncols):
            print(worksheet.cell_value(i, j), "\t", end="")  # 逐行逐列读取数据


def init_excel(shop_info,filename):
    # 初始化表头
    value_title = [[], ]
    for i in shop_info:
        value_title[0].append(i)
    value_title[0].append('目标地址')

    book_name_xls = filename
    sheet_name_xls = '1'
    write_excel_xls(book_name_xls, sheet_name_xls, value_title)


def save_excel(shop_info, filename,lis):
    if not os.path.exists(filename):
        init_excel(shop_info,filename)
    value=[[],]
    for item in shop_info:
        value[0].append(shop_info[item])
    value[0].append(lis)
    write_excel_xls_append(filename, value)

# shop_info = {'商户id': 'E2126339878494162457', '商户名称': '小猪先森美食铺(美食广场店)', '月销量': 16, '配送费': '配送费¥4', '起送价': 20,
#              '配送价': 4, '营业时间': '10:00/21:00', '配送时间': 30, '商家评分': 5, '是否新店': False, '类别': '盖浇饭|烧烤|',
#              '经度': 30.311603, '维度': 120.385057, '是否品牌': False, '商家活动': '新用户下单立减15元|',
#              '商家logo': 'https://fuss10.elemecdn.com/7/29/732be1478f292d696a0ac75f6869ajpeg.jpeg?imageMogr/format/webp/thumbnail/!130x130r/gravity/Center/crop/130x130/',
#              '配送方式': '蜂鸟专送', '爬取时间': 'Tue Jul 23 17:20:07 2019', '商家地址': '', '商家电话': '123'}
# save_excel(shop_info,'data.xls')

