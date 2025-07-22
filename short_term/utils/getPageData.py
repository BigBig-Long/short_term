import json

from short_term.utils.getPublicData import cityList

def getHomeGeoCharData(hourse_data):
    average_price_dic = average_price(hourse_data)
    cityDic = {}
    for key,value in average_price_dic.items():
        for j in cityList:
            for k in j['city']:
                if k.find(key) != -1:
                    cityDic[j['province']] = value
    cityDicList = []
    for key,value in cityDic.items():
        cityDicList.append({
            'name':key,
            'value':value
        })
    return cityDicList

def getHomeRadarData(hourse_data):
    cityDic = {}
    for i in hourse_data:
        if cityDic.get(i.city,-1) == -1:
            cityDic[i.city] = 1
        else:
            cityDic[i.city] += 1
    radarOne = []
    radarTwo = list(cityDic.values())
    for key, value in cityDic.items():
        radarOne.append({
            'name': key,
            'max': 100
        })
    return radarOne,radarTwo

def getHomeTagsData(hourse_data):
    maxPrice = 0
    maxHourseType = {}
    maxHourseSale_status = {}
    for i in hourse_data:
        if maxPrice < int(i.price):
            maxPrice = int(i.price)
        if maxHourseType.get(i.hourseType,-1) == -1:
            maxHourseType[i.hourseType] = 1
        else:
            maxHourseType[i.hourseType] += 1
        if maxHourseSale_status.get(i.sale_status,-1) == -1:
            maxHourseSale_status[i.sale_status] = 1
        else:
            maxHourseSale_status[i.sale_status] += 1
    maxHourseTypeSort = list(sorted(maxHourseType.items(),key=lambda x:x[1],reverse=True))
    maxHourseSale_statusSort = list(sorted(maxHourseSale_status.items(),key=lambda x:x[1],reverse=True))
    maxHourseSale = ''
    if maxHourseSale_statusSort[0][0] == '1':
        maxHourseSale = '在售'
    elif maxHourseSale_statusSort[0][0] == '2':
        maxHourseSale = '已售'
    elif maxHourseSale_statusSort[0][0] == '3':
        maxHourseSale = '出租中'
    elif maxHourseSale_statusSort[0][0] == '4':
        maxHourseSale = '已出租'
    elif maxHourseSale_statusSort[0][0] == '5':
        maxHourseSale = '预售'
    elif maxHourseSale_statusSort[0][0] == '6':
        maxHourseSale = '其他'

    return len(hourse_data),maxPrice,maxHourseTypeSort[0][0],maxHourseSale

def getHourseByHourseName(searchWord,hourse_data):
    searchList = []
    for hourse in hourse_data:
        if hourse.title.find(searchWord) != -1:
            searchList.append(hourse)
    return searchList

def average_price(hourse_data,type='city'):
    city_prices = {}
    city_counts = {}
    for house in hourse_data:
        if type=='city':
            city = house.city
        else:
            city = house.open_date
            if city == '':continue
        prices = int(house.price)
        if city in city_prices:
            city_prices[city] += prices
            city_counts[city] += 1
        else:
            city_prices[city] = prices
            city_counts[city] = 1

    average_prices = {}
    for city in city_prices:
        average_prices[city] = round(city_prices[city] / city_counts[city],1)

    return average_prices

def getPriceCharDataTwo(hourseList):
    average_pricesData = average_price(hourseList,'open_date')
    sorted_data = list(sorted(average_pricesData.items(),key=lambda x:x[0],reverse=True))
    return [x[0] for x in sorted_data],[x[1] for x in sorted_data]

def getPriceCharDataThree(hourseList):
    data = []
    for h in hourseList:
        data.append(
            h.totalPrice_range
        )
    return data

def getPriceCharOneData(hourseList):
    X = ['<=4000','4000-6000','6000-8000','8000-10000','10000-12000','12000-15000','15000-18000','>=20000']
    Y = [0 for x in range(len(X))]
    for h in hourseList:
        if int(h.price) <= 4000:
            Y[0] +=1
        elif int(h.price) <=6000:
            Y[1] +=1
        elif int(h.price) <=8000:
            Y[2] +=1
        elif int(h.price) <=10000:
            Y[3] +=1
        elif int(h.price) <=12000:
            Y[3] +=1
        elif int(h.price) <=15000:
            Y[4] +=1
        elif int(h.price) <=18000:
            Y[5] +=1
        elif int(h.price) >=20000:
            Y[6] +=1

    return X,Y


def getDetailCharOne(hourseList):
    roomsDic = {}
    for i in hourseList:
        for room in i.rooms_desc:
            if roomsDic.get(room,-1) == -1:
                roomsDic[room] = 1
            else:
                roomsDic[room] += 1
    resData = []
    for key,value in roomsDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getDetailCharTwo(hourseList,type):
    if type=='big':
        xData = [
            '80-100',
            '100-110',
            '110-120',
            '120-130',
            '130-140',
            '140-150',
            '150-160',
            '160-170',
            '170-180',
            '200-n'
        ]
    else:
        xData = [
            '0-40',
            '40-60',
            '60-80',
            '80-100',
            '100-120',
            '120-150',
            '150-n'
        ]
    yData = [0 for x in range(len(xData))]
    for i in hourseList:
        if len(i.area_range) == 1 :continue
        if type == 'big':
            if float(i.area_range[1]) >= 80 and float(i.area_range[1]) < 100:
                yData[0] +=1
            elif float(i.area_range[1]) <= 110:
                yData[1] +=1
            elif float(i.area_range[1]) <= 120:
                yData[2] +=1
            elif float(i.area_range[1]) <= 130:
                yData[3] +=1
            elif float(i.area_range[1]) <= 140:
                yData[4] +=1
            elif float(i.area_range[1]) <= 150:
                yData[5] +=1
            elif float(i.area_range[1]) <= 160:
                yData[6] +=1
            elif float(i.area_range[1]) <= 170:
                yData[7] +=1
            elif float(i.area_range[1]) <= 180:
                yData[8] +=1
            elif float(i.area_range[1]) >= 200:
                yData[9] +=1
        else:
            if float(i.area_range[0]) <= 40:
                yData[0] +=1
            elif float(i.area_range[0]) <= 80:
                yData[1] +=1
            elif float(i.area_range[0]) <= 100:
                yData[2] +=1
            elif float(i.area_range[0]) <= 120:
                yData[3] +=1
            elif float(i.area_range[0]) <= 150:
                yData[4] +=1
            elif float(i.area_range[0]) <= 150:
                yData[5] +=1
            elif float(i.area_range[0]) > 150:
                yData[6] +=1

    return xData,yData

def getDicData(hourseList,fild):
    hourseDecorationDic = {}
    for h in hourseList:
        if fild == 'hourseDecoration' and h.hourseDecoration != '':
            if hourseDecorationDic.get(h.hourseDecoration, -1) == -1:
                hourseDecorationDic[h.hourseDecoration] = 1
            else:
                hourseDecorationDic[h.hourseDecoration] += 1
        elif fild == 'hourseType':
            if hourseDecorationDic.get(h.hourseType, -1) == -1:
                hourseDecorationDic[h.hourseType] = 1
            else:
                hourseDecorationDic[h.hourseType] += 1
        elif fild == 'tags':
            for tag in h.tags:
                if hourseDecorationDic.get(tag, -1) == -1:
                    hourseDecorationDic[tag] = 1
                else:
                    hourseDecorationDic[tag] += 1

    resData = []
    for key, value in hourseDecorationDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getTypeCharDataOne(hourseList):
    return getDicData(hourseList,'hourseDecoration')

def getTypeCharDataTwo(hourseList):
    return getDicData(hourseList,'hourseType')

def getAnthorCharOne(hourseList):
    cityDic = {}
    for i in hourseList:
        if i.on_time == '0000-00-00 00:00:00':
            if cityDic.get(i.city,-1) == -1:
                cityDic[i.city] = 1
            else:
                cityDic[i.city] += 1
    return list(cityDic.keys()),list(cityDic.values())

def getAnthorCharTwo(hourseList):
    sale_statusDic = {}
    for h in hourseList:
        if h.sale_status == '1':
            if sale_statusDic.get('在售',-1) == -1:
                sale_statusDic['在售'] = 1
            else:
                sale_statusDic['在售'] += 1
        elif h.sale_status == '2':
            if sale_statusDic.get('已售',-1) == -1:
                sale_statusDic['已售'] = 1
            else:
                sale_statusDic['已售'] += 1
        elif h.sale_status == '3':
            if sale_statusDic.get('出租中',-1) == -1:
                sale_statusDic['出租中'] = 1
            else:
                sale_statusDic['出租中'] += 1
        elif h.sale_status == '4':
            if sale_statusDic.get('已出租',-1) == -1:
                sale_statusDic['已出租'] = 1
            else:
                sale_statusDic['已出租'] += 1
        elif h.sale_status == '5':
            if sale_statusDic.get('预售',-1) == -1:
                sale_statusDic['预售'] = 1
            else:
                sale_statusDic['预售'] += 1
        elif h.sale_status == '6':
            if sale_statusDic.get('其他',-1) == -1:
                sale_statusDic['其他'] = 1
            else:
                sale_statusDic['其他'] += 1
    resData = []
    for key, value in sale_statusDic.items():
        resData.append({
            'name': key,
            'value': value
        })
    return resData

def getAnthorCharThree(hourseList):
    return [x['name'] for x in getDicData(hourseList,'tags')],[x['value'] for x in getDicData(hourseList,'tags')]

def getDicData(hourseList,fild):
    hourseDecorationDic = {}
    for h in hourseList:
        if fild == 'hourseDecoration' and h.hourseDecoration != '':
            if hourseDecorationDic.get(h.hourseDecoration, -1) == -1:
                hourseDecorationDic[h.hourseDecoration] = 1
            else:
                hourseDecorationDic[h.hourseDecoration] += 1
        elif fild == 'hourseType':
            if hourseDecorationDic.get(h.hourseType, -1) == -1:
                hourseDecorationDic[h.hourseType] = 1
            else:
                hourseDecorationDic[h.hourseType] += 1
        elif fild == 'tags':
            for tag in h.tags:
                if hourseDecorationDic.get(tag, -1) == -1:
                    hourseDecorationDic[tag] = 1
                else:
                    hourseDecorationDic[tag] += 1

    resData = []
    for key, value in hourseDecorationDic.items():
        resData.append({
            'name':key,
            'value':value
        })
    return resData

def getTypeCharDataOne(hourseList):
    return getDicData(hourseList,'hourseDecoration')

def getTypeCharDataTwo(hourseList):
    return getDicData(hourseList,'hourseType')


# utils/getPageData.py
def getRegionData(hourseList):
    # 初始化数据结构：{区域: {房屋类型: 数量}}
    region_type_dict = {}

    for h in hourseList:
        region = h.region
        house_type = h.hourseType  # 房屋类型字段

        if not region or not house_type:
            continue

        # 初始化区域
        if region not in region_type_dict:
            region_type_dict[region] = {}

        # 统计房屋类型数量
        region_type_dict[region][house_type] = region_type_dict[region].get(house_type, 0) + 1

    # 转换为 ECharts 所需格式
    categories = list(region_type_dict.keys())  # 区域列表
    series = []

    # 获取所有可能的房屋类型
    all_house_types = set()
    for region_data in region_type_dict.values():
        all_house_types.update(region_data.keys())

    # 为每种房屋类型创建一个系列
    for house_type in all_house_types:
        data = []
        for region in categories:
            data.append(region_type_dict[region].get(house_type, 0))

        series.append({
            'name': house_type,
            'type': 'bar',
            'stack': '总量',  # 设置堆叠
            'data': data
        })

    return {
        'categories': categories,
        'series': series
    }


def getRegionPriceStackData(hourseList):
    """
    生成区域-房屋类型均价数据，用于堆叠图
    返回格式: [{'region': '区域名', 'house_types': [{'type': '类型名', 'average_price': 均价}, ...]}, ...]
    """
    # 初始化数据结构: {区域: {房屋类型: [价格列表]}}
    region_type_prices = {}

    for h in hourseList:
        region = h.region
        house_type = h.hourseType
        price = h.price

        if not region or not house_type or not price:
            continue

        try:
            price_num = float(price)

            # 初始化区域
            if region not in region_type_prices:
                region_type_prices[region] = {}

            # 初始化房屋类型价格列表
            if house_type not in region_type_prices[region]:
                region_type_prices[region][house_type] = []

            region_type_prices[region][house_type].append(price_num)
        except ValueError:
            continue  # 跳过无效价格

    # 计算均价并格式化结果
    result = []
    for region, type_prices in region_type_prices.items():
        house_types = []
        for house_type, prices in type_prices.items():
            # 计算均价并保留两位小数
            avg_price = round(sum(prices) / len(prices), 2)
            house_types.append({
                'type': house_type,
                'average_price': avg_price
            })
        result.append({
            'region': region,
            'house_types': house_types
        })

    return result

def getRoomsData(hourseList):
    roomsDic = {}
    for h in hourseList:
        try:
            # 检查 rooms_desc 的类型
            if isinstance(h.rooms_desc, str):
                # 如果是字符串，尝试解析为 JSON
                rooms = json.loads(h.rooms_desc)
            elif isinstance(h.rooms_desc, list):
                # 如果已经是列表，直接使用
                rooms = h.rooms_desc
            else:
                # 其他类型（如 None）则跳过
                continue

            # 统计房间数
            for room in rooms:
                roomsDic[room + '室'] = roomsDic.get(room + '室', 0) + 1
        except Exception as e:
            print(f"解析 rooms_desc 失败: {e}")
            continue  # 跳过错误数据

    return [{'name': k, 'value': v} for k, v in roomsDic.items()]


# utils/getPageData.py

def getTagsData(hourseList):
    tagsDic = {}
    for h in hourseList:
        try:
            # 处理 tags 可能是字符串或列表的情况
            if isinstance(h.tags, str):
                tags = json.loads(h.tags)
            elif isinstance(h.tags, list):
                tags = h.tags
            else:
                continue  # 跳过无效数据

            # 统计标签出现次数
            for tag in tags:
                tagsDic[tag] = tagsDic.get(tag, 0) + 1
        except Exception as e:
            print(f"解析标签失败: {e}")
            continue

    # 转换为词云所需格式
    return [{'name': k, 'value': v} for k, v in tagsDic.items()]

# 1. 全局数据：各城市未交房数（所有城市，不随选择变化）
def getAnthorCharOne(hourseList):
    cityDic = {}
    for i in hourseList:
        if i.on_time == '0000-00-00 00:00:00':
            if cityDic.get(i.city,-1) == -1:
                cityDic[i.city] = 1
            else:
                cityDic[i.city] += 1
    return list(cityDic.keys()),list(cityDic.values())

def getAnthorCharTwo(hourseList):
    sale_statusDic = {}
    for h in hourseList:
        if h.sale_status == '1':
            if sale_statusDic.get('在售',-1) == -1:
                sale_statusDic['在售'] = 1
            else:
                sale_statusDic['在售'] += 1
        elif h.sale_status == '2':
            if sale_statusDic.get('已售',-1) == -1:
                sale_statusDic['已售'] = 1
            else:
                sale_statusDic['已售'] += 1
        elif h.sale_status == '3':
            if sale_statusDic.get('出租中',-1) == -1:
                sale_statusDic['出租中'] = 1
            else:
                sale_statusDic['出租中'] += 1
        elif h.sale_status == '4':
            if sale_statusDic.get('已出租',-1) == -1:
                sale_statusDic['已出租'] = 1
            else:
                sale_statusDic['已出租'] += 1
        elif h.sale_status == '5':
            if sale_statusDic.get('预售',-1) == -1:
                sale_statusDic['预售'] = 1
            else:
                sale_statusDic['预售'] += 1
        elif h.sale_status == '6':
            if sale_statusDic.get('其他',-1) == -1:
                sale_statusDic['其他'] = 1
            else:
                sale_statusDic['其他'] += 1
    resData = []
    for key, value in sale_statusDic.items():
        resData.append({
            'name': key,
            'value': value
        })
    return resData


def getYearAnalysisData(hourseList):
    yearDic = {}
    for h in hourseList:
        # 提取年份（假设open_date格式为YYYY-MM-DD）
        year = h.open_date.split('-')[0]
        # 统计每年的数量
        if year in yearDic:
            yearDic[year] += 1
        else:
            yearDic[year] = 1
    # 转换为列表并按年份排序（升序）
    resData = []
    for key in sorted(yearDic.keys()):
        resData.append({
            'name': key,
            'value': yearDic[key]
        })
    return resData


def get_type_char_data():
    return getTypeCharDataOne, getTypeCharDataTwo

# 房屋装修情况分析数据获取函数
def getDecorationAnalysisData(hourseList):
    return getDicData(hourseList, 'hourseDecoration')

def getAnthorCharThree(hourseList):
    return [x['name'] for x in getDicData(hourseList,'tags')],[x['value'] for x in getDicData(hourseList,'tags')]


