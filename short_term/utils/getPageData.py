import json
import re

import pandas as pd

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
    average_pricesData = average_price(hourseList, 'open_date')

    valid_entries = {
        date: price for date, price in average_pricesData.items()
        if is_valid_date(date)  # 调用有效性校验函数
    }
    # 按时间升序排序
    sorted_data = sorted(valid_entries.items(), key=lambda x: x[0], reverse=False)

    dates = [x[0] for x in sorted_data]
    prices = [x[1] for x in sorted_data]
    return dates, prices


# 辅助函数：校验日期有效性（示例）
def is_valid_date(date_str):
    try:
        # 校验格式：YYYY-MM-DD（允许19/20开头的年份）
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            return False
        year, month, day = map(int, date_str.split('-'))
        if month < 1 or month > 12 or day < 1 or day > 31:
            return False
        # 校验闰年2月（可选）
        if month == 2 and day > 29:
            return False
        if month in [4, 6, 9, 11] and day > 30:
            return False
        return True
    except:
        return False


CITY_LEVEL_MAPPING = {
    # 一线城市
    '北京': '一线城市', '上海': '一线城市', '广州': '一线城市', '深圳': '一线城市',

    # 新一线城市
    '成都': '新一线城市', '杭州': '新一线城市', '重庆': '新一线城市', '武汉': '新一线城市',
    '苏州': '新一线城市', '西安': '新一线城市', '天津': '新一线城市', '南京': '新一线城市',
    '长沙': '新一线城市', '郑州': '新一线城市', '东莞': '新一线城市', '青岛': '新一线城市',
    '沈阳': '新一线城市', '宁波': '新一线城市', '昆明': '新一线城市', '佛山': '新一线城市',

    # 二线城市
    '无锡': '二线城市', '合肥': '二线城市', '福州': '二线城市', '厦门': '二线城市',
    '济南': '二线城市', '哈尔滨': '二线城市', '长春': '二线城市', '石家庄': '二线城市',
    '太原': '二线城市', '南昌': '二线城市', '南宁': '二线城市', '贵阳': '二线城市',
    '海口': '二线城市', '兰州': '二线城市', '银川': '二线城市', '西宁': '二线城市',

    # 三线城市
    '珠海': '三线城市', '汕头': '三线城市', '惠州': '三线城市', '江门': '三线城市',
    '常州': '三线城市', '徐州': '三线城市', '南通': '三线城市', '绍兴': '三线城市',
    '温州': '三线城市', '嘉兴': '三线城市', '烟台': '三线城市', '保定': '三线城市',
    '潍坊': '三线城市', '镇江': '三线城市', '临沂': '三线城市', '唐山': '三线城市',

    # 四线城市
    # '湖州': '四线城市', '盐城': '四线城市', '扬州': '四线城市', '赣州': '四线城市',
    # '洛阳': '四线城市', '临沂': '四线城市', '威海': '四线城市', '泰安': '四线城市',
    # '遵义': '四线城市', '吉林': '四线城市', '邯郸': '四线城市', '临沂': '四线城市',
    #
    # # 五线城市
    # '赤峰': '五线城市', '昭通': '五线城市', '曲靖': '五线城市', '玉林': '五线城市',
    # '大理': '五线城市', '安阳': '五线城市', '株洲': '五线城市', '新乡': '五线城市',
    # '焦作': '五线城市', '平顶山': '五线城市', '商丘': '五线城市', '周口': '五线城市',

    # 其他城市
    '其他城市': '其他'
}

def get_price_distribution():
    df = pd.read_csv('./spider/hourse_info_cleaned.csv', encoding='utf-8')
    df = df[['city', 'price']].dropna(subset=['city', 'price'])

    df['city_level'] = df['city'].map(CITY_LEVEL_MAPPING).fillna('其他城市')

    # 定义价格区间
    bins = [0, 4000, 6000, 8000, 10000, 12000, 15000, 18000, 20000, float('inf')]
    labels = ['<=4000', '4000-6000', '6000-8000', '8000-10000',
              '10000-12000', '12000-15000', '15000-18000', '18000-20000', '>20000']

    # 分组统计
    df['price_range'] = pd.cut(df['price'], bins=bins, labels=labels, right=False)
    grouped = df.groupby(['city_level', 'price_range']).size().unstack(fill_value=0)
    total = grouped.sum(axis=1)
    grouped_pct = grouped.div(total, axis=0)

    return grouped_pct



def getTop10CityAvgPrice():
    df = pd.read_csv('./spider/hourse_info_cleaned.csv')

    # 只保留有用的字段，假设有 "city" 和 "price" 字段
    df = df[['city', 'price']].dropna()

    # 按城市计算平均价格，并排序取前十
    city_avg = df.groupby('city')['price'].mean().round(1).sort_values(ascending=False).head(15)

    # 返回城市列表和对应的平均价格
    top_cities = city_avg.index.tolist()
    avg_prices = city_avg.values.tolist()
    return top_cities, avg_prices, df[df['city'].isin(top_cities)]

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



from collections import defaultdict

from collections import defaultdict


def getDetailCharOne(hourseList):
    """
    (按要求修改版)
    统计房型数量，并完全跳过无法识别或为空的数据。
    - 翻译 '1'-'5' 为中文。
    - 合并 '6' 及以上为 "五室以上"。
    - 忽略所有空值和不符合上述规则的数据。
    """
    # 定义房型数字到文本的映射关系
    room_map = {
        '1': '一室',
        '2': '两室',
        '3': '三室',
        '4': '四室',
        '5': '五室',
    }

    type_counts = defaultdict(int)

    for i in hourseList:
        # 1. 如果整个房子的 rooms_desc 属性不存在、为None或为空列表，则直接跳过这个房子。
        if not hasattr(i, 'rooms_desc') or not i.rooms_desc:
            continue

        # 2. 遍历一个房子的所有房型描述
        for room in i.rooms_desc:
            room_str = str(room).strip()

            # 3. 如果房型描述是空字符串，也跳过
            if not room_str:
                continue

            # 4. 优先匹配 1-5 室
            if room_str in room_map:
                type_name = room_map[room_str]
                type_counts[type_name] += 1
            # 5. 如果不是 1-5 室，尝试看是否为更大的数字
            else:
                try:
                    # 只有大于等于6的数字才进行统计
                    if int(room_str) >= 6:
                        type_counts['五室以上'] += 1
                    # 其他所有情况（如'0'或无法转换的文本）都将被忽略，不做任何事
                except ValueError:
                    # 如果 room_str 不能转换为整数 (例如是'别墅'等文本)，也跳过
                    continue

    # 6. 将统计结果转换为 ECharts 需要的列表格式
    resData = []
    for name, value in type_counts.items():
        resData.append({
            'name': name,
            'value': value
        })

    return resData

# 这是修正后的版本，请用它替换您现有的 getDetailCharTwo 函数
def getDetailCharTwo(hourseList, type):
    """
    统计房屋列表中不同面积区间的房屋数量 (重构修复版)。
    """
    # 定义不同分析类型的配置
    # 格式: (标签, 区间下限(包含), 区间上限(不包含))
    # None 代表无穷大或无穷小
    configs = {
        'big': {
            'area_index': 1,  # 使用最大面积 i.area_range[1]
            'bins': [
                ('80-100', 80, 100), ('100-110', 100, 110),
                ('110-120', 110, 120), ('120-130', 120, 130),
                ('130-140', 130, 140), ('140-150', 140, 150),
                ('150-160', 150, 160), ('160-170', 160, 170),
                ('170-180', 170, 180), ('180-200', 180, 200),
                ('200-n', 200, float('inf')),  # 使用无穷大表示上限
            ]
        },
        'small': {
            'area_index': 0,  # 使用最小面积 i.area_range[0]
            'bins': [
                ('0-40', float('-inf'), 40), ('40-60', 40, 60),
                ('60-80', 60, 80), ('80-100', 80, 100),
                ('100-120', 100, 120), ('120-150', 120, 150),
                ('150-n', 150, float('inf')),
            ]
        }
    }

    config = configs.get(type, configs['small'])  # 如果type无效，默认使用'small'
    area_index = config['area_index']
    bins = config['bins']

    xData = [b[0] for b in bins]
    yData = [0] * len(xData)

    for hourse in hourseList:
        # 数据校验
        if not hasattr(hourse, 'area_range') or not isinstance(hourse.area_range, list) or len(
                hourse.area_range) <= area_index:
            continue

        try:
            area = float(hourse.area_range[area_index])
        except (ValueError, TypeError):
            continue

        # 遍历区间进行统计 (这是正确的逻辑)
        for i, (label, lower_bound, upper_bound) in enumerate(bins):
            if lower_bound <= area < upper_bound:
                yData[i] += 1
                break  # 找到区间后就停止内层循环，避免重复计数

    return xData, yData

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


def getYearAnalysisData(hourseList):
    yearDic = {}
    for h in hourseList:
        # 先判断日期是否为空或无效
        if not h.open_date or str(h.open_date).strip() in ['', 'N/A', 'nan']:
            continue  # 跳过空值或无效日期

        # 提取年份（假设open_date格式为YYYY-MM-DD）
        try:
            year = h.open_date.split('-')[0]
            # 简单验证年份格式（4位数字）
            if len(year) == 4 and year.isdigit():
                # 统计每年的数量
                if year in yearDic:
                    yearDic[year] += 1
                else:
                    yearDic[year] = 1
        except (AttributeError, IndexError):
            # 处理无法分割的异常情况（如格式错误）
            continue

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
