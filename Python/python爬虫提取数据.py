import requests
import time
import csv  # 导入csv模块
for page in range(1,11):  	# 一共10页
    url1 = 'http://zdscxx.moa.gov.cn:8080/nyb/updateFrequencyConditions'
    url2 = 'http://zdscxx.moa.gov.cn:8080/nyb/getFrequencyData'
    data = {
        'page':page,
        'rows':'20',
        'type':'周度数据',
        'subType':'农产品批发价格',
        'level':'0',
        'time':'["2021-19","2025-18"]',
        'product':'蔬菜'
    }
    headers = {
        'Cookie': 'wdcid=5d2466f408916300; http_waf_cookie=83e63922-e867-4d7dc51d3f83ecc53f120ad612260bd1a77a; _yfxkpy_ssid_10002896=%7B%22_yfxkpy_firsttime%22%3A%221745831904474%22%2C%22_yfxkpy_lasttime%22%3A%221746329295844%22%2C%22_yfxkpy_visittime%22%3A%221746329295844%22%2C%22_yfxkpy_cookie%22%3A%2220250428171824476278503705874605%22%2C%22_yfxkpy_returncount%22%3A%221%22%7D; wdlast=1746329297; wdses=02fce6f551891761',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
        'Host': 'www.moa.gov.cn',
        'Origin': 'http://zdscxx.moa.gov.cn:8080',
        'Referer': 'http://zdscxx.moa.gov.cn:8080/nyb/pc/frequency.jsp',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 将写入模式从 "w" 改为 "a" 实现追加写入
    f = open("data.csv", "a", encoding="utf-8",newline='')  # 修改模式为追加
    csvwriter = csv.writer(f)
    # 只在第一次运行时写入表头（如果文件已存在可能需要手动删除）
    if page == 0:
        csvwriter.writerow(['时间','品类','指标','地区','单位','数值'])

    s = requests.session()	# <requests.sessions.Session at 0x24b202c27f0>
    r1 = s.post(url1,data=data,headers=headers)	# <Response [200]>
    r2 = s.post(url2,data=data,headers=headers)	# <Response [200]>
    content = r2.json()		# 得到json数据
    data_list = content['result']['pageInfo']['table']
    for item in data_list:
        v_data = {}
        v_data['时间'] = item['time']
        v_data['品类'] = item['product']
        v_data['指标'] = item['item']
        v_data['地区'] = item['area']
        v_data['单位'] = item['unit']
        v_data['数值'] = item['value']
        csvwriter.writerow(v_data.values())
    # 关闭操作保持不变
    time.sleep(3)
    f.close()
    print(f'第{page}页爬取成功')
    r1.close()
    r2.close()
    s.close()
print('over!')
