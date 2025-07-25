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


def getDicData(hourseList, fild):
    """
    通用数据统计函数，根据指定字段对房屋列表进行分组计数
    :param hourseList: 房屋信息列表，每个元素为包含房屋属性的对象
    :param fild: 需统计的字段名，支持'hourseDecoration'(装修情况)、'hourseType'(房屋类型)、'tags'(标签)
    :return: 统计结果列表，每个元素为{'name': 字段值, 'value': 计数}
    """
    # 初始化统计字典，键为字段值，值为出现次数
    hourseDecorationDic = {}

    for h in hourseList:
        # 处理房屋装修情况统计（过滤空值）
        if fild == 'hourseDecoration' and h.hourseDecoration != '':
            # 若字典中无该键则初始化计数为1，否则计数+1
            if hourseDecorationDic.get(h.hourseDecoration, -1) == -1:
                hourseDecorationDic[h.hourseDecoration] = 1
            else:
                hourseDecorationDic[h.hourseDecoration] += 1

        # 处理房屋类型统计（无需过滤空值，直接统计）
        elif fild == 'hourseType':
            if hourseDecorationDic.get(h.hourseType, -1) == -1:
                hourseDecorationDic[h.hourseType] = 1
            else:
                hourseDecorationDic[h.hourseType] += 1

        # 处理标签统计（标签为列表，需遍历每个标签单独计数）
        elif fild == 'tags':
            for tag in h.tags:
                if hourseDecorationDic.get(tag, -1) == -1:
                    hourseDecorationDic[tag] = 1
                else:
                    hourseDecorationDic[tag] += 1

    # 转换统计结果为指定格式的列表
    resData = []
    for key, value in hourseDecorationDic.items():
        resData.append({
            'name': key,  # 字段值
            'value': value  # 出现次数
        })
    return resData


def getTypeCharDataTwo(hourseList):
    """获取房屋类型统计数据（调用通用统计函数）"""
    return getDicData(hourseList, 'hourseType')


def getTypeCharDataOne(hourseList):
    """获取房屋装修情况统计数据（调用通用统计函数）"""
    return getDicData(hourseList, 'hourseDecoration')


def getAnthorCharOne(hourseList):
    """
    统计特定时间字段为空的房屋所在城市分布
    :param hourseList: 房屋信息列表
    :return: 两个列表，分别为城市名列表和对应城市的房屋数量列表
    """
    cityDic = {}
    for i in hourseList:
        # 筛选时间字段为'0000-00-00 00:00:00'的房屋
        if i.on_time == '0000-00-00 00:00:00':
            # 统计城市出现次数
            if cityDic.get(i.city, -1) == -1:
                cityDic[i.city] = 1
            else:
                cityDic[i.city] += 1
    # 返回城市名列表和对应的数量列表
    return list(cityDic.keys()), list(cityDic.values())


def getAnthorCharTwo(hourseList):
    """
    统计房屋销售状态分布（在售/已售/出租中/已出租/预售/其他）
    :param hourseList: 房屋信息列表
    :return: 统计结果列表，每个元素为{'name': 状态名, 'value': 计数}
    """
    sale_statusDic = {}
    for h in hourseList:
        # 根据销售状态编码映射为中文名称并计数
        if h.sale_status == '1':
            key = '在售'
        elif h.sale_status == '2':
            key = '已售'
        elif h.sale_status == '3':
            key = '出租中'
        elif h.sale_status == '4':
            key = '已出租'
        elif h.sale_status == '5':
            key = '预售'
        elif h.sale_status == '6':
            key = '其他'
        else:
            continue  # 跳过未定义的状态

        # 更新计数
        if sale_statusDic.get(key, -1) == -1:
            sale_statusDic[key] = 1
        else:
            sale_statusDic[key] += 1

    # 转换为指定格式的结果列表
    resData = []
    for key, value in sale_statusDic.items():
        resData.append({
            'name': key,
            'value': value
        })
    return resData


def getAnthorCharThree(hourseList):
    """
    提取房屋标签的名称和对应数量列表（用于图表展示）
    :param hourseList: 房屋信息列表
    :return: 两个列表，分别为标签名称列表和对应数量列表
    """
    # 先通过通用函数获取标签统计结果，再拆分名称和数量
    tag_data = getDicData(hourseList, 'tags')
    return [x['name'] for x in tag_data], [x['value'] for x in tag_data]


# utils/getPageData.py
def getRegionData(hourseList):
    """
    生成区域-房屋类型的数量统计，用于堆叠柱状图数据
    :param hourseList: 房屋信息列表
    :return: ECharts所需格式的数据，包含categories(区域)和series(各类型数据)
    """
    # 初始化数据结构：{区域: {房屋类型: 数量}}
    region_type_dict = {}

    for h in hourseList:
        region = h.region  # 区域
        house_type = h.hourseType  # 房屋类型
        # 跳过区域或房屋类型为空的数据
        if not region or not house_type:
            continue

        # 初始化区域对应的字典（若不存在）
        if region not in region_type_dict:
            region_type_dict[region] = {}

        # 累加该区域下该房屋类型的数量
        region_type_dict[region][house_type] = region_type_dict[region].get(house_type, 0) + 1

    # 转换为ECharts堆叠图所需格式
    categories = list(region_type_dict.keys())  # 区域列表（x轴分类）
    series = []  # 数据系列（各房屋类型的柱状图数据）

    # 获取所有可能的房屋类型（用于生成系列）
    all_house_types = set()
    for region_data in region_type_dict.values():
        all_house_types.update(region_data.keys())

    # 为每种房屋类型创建一个数据系列
    for house_type in all_house_types:
        data = []
        # 按区域顺序填充该类型的数量（无数据则为0）
        for region in categories:
            data.append(region_type_dict[region].get(house_type, 0))
        # 添加系列数据（设置堆叠属性）
        series.append({
            'name': house_type,  # 房屋类型名称
            'type': 'bar',  # 图表类型为柱状图
            'stack': '总量',  # 启用堆叠效果
            'data': data  # 各区域的数量数据
        })

    return {
        'categories': categories,  # 区域分类
        'series': series  # 堆叠图数据系列
    }


def getRegionPriceStackData(hourseList):
    """
    生成区域-房屋类型的均价统计，用于堆叠图展示
    :param hourseList: 房屋信息列表
    :return: 格式化数据，格式为：
             [{'region': '区域名', 'house_types': [{'type': '类型名', 'average_price': 均价}, ...]}, ...]
    """
    # 初始化数据结构: {区域: {房屋类型: [价格列表]}}
    # 存储每个区域下每种房屋类型的所有价格，用于后续计算均价
    region_type_prices = {}

    for h in hourseList:
        region = h.region  # 区域
        house_type = h.hourseType  # 房屋类型
        price = h.price  # 价格

        # 跳过区域、类型或价格为空的数据
        if not region or not house_type or not price:
            continue

        try:
            # 将价格转换为数值（处理可能的字符串格式）
            price_num = float(price)

            # 初始化区域字典（若不存在）
            if region not in region_type_prices:
                region_type_prices[region] = {}

            # 初始化该区域下房屋类型的价格列表（若不存在）
            if house_type not in region_type_prices[region]:
                region_type_prices[region][house_type] = []

            # 将价格添加到对应列表
            region_type_prices[region][house_type].append(price_num)

        except ValueError:
            # 跳过无法转换为数值的无效价格
            continue

    # 计算均价并格式化结果
    result = []
    for region, type_prices in region_type_prices.items():
        house_types = []
        # 计算该区域下每种房屋类型的均价
        for house_type, prices in type_prices.items():
            # 均价 = 总价 / 数量，保留两位小数
            avg_price = round(sum(prices) / len(prices), 2)
            house_types.append({
                'type': house_type,
                'average_price': avg_price
            })
        # 按区域整理结果
        result.append({
            'region': region,
            'house_types': house_types
        })

    return result


def getRoomsData(hourseList):
    """
    统计房屋户型（几室）的分布情况
    :param hourseList: 房屋信息列表
    :return: 统计结果列表，每个元素为{'name': 'X室', 'value': 数量}
    """
    roomsDic = {}  # 键为"X室"，值为出现次数

    for h in hourseList:
        try:
            # 处理户型描述字段（可能是JSON字符串或列表）
            if isinstance(h.rooms_desc, str):
                # 若为字符串，尝试解析为列表（如"['1', '2']" -> ['1', '2']）
                rooms = json.loads(h.rooms_desc)
            elif isinstance(h.rooms_desc, list):
                # 若已是列表，直接使用
                rooms = h.rooms_desc
            else:
                # 其他类型（如None）则跳过
                continue

            # 统计每个户型的出现次数（格式化为"X室"）
            for room in rooms:
                key = f"{room}室"  # 转换为"1室"、"2室"等格式
                roomsDic[key] = roomsDic.get(key, 0) + 1

        except Exception as e:
            # 捕获解析异常（如JSON格式错误），跳过错误数据
            print(f"解析 rooms_desc 失败: {e}")
            continue

    # 转换为指定格式的结果列表
    return [{'name': k, 'value': v} for k, v in roomsDic.items()]


def getTagsData(hourseList):
    """
    统计房屋标签的出现次数，用于词云等展示
    :param hourseList: 房屋信息列表
    :return: 统计结果列表，每个元素为{'name': '标签名', 'value': 出现次数}
    """
    tagsDic = {}  # 键为标签名，值为出现次数

    for h in hourseList:
        try:
            # 处理标签字段（可能是JSON字符串或列表）
            if isinstance(h.tags, str):
                # 若为字符串，尝试解析为列表
                tags = json.loads(h.tags)
            elif isinstance(h.tags, list):
                # 若已是列表，直接使用
                tags = h.tags
            else:
                # 其他类型则跳过
                continue

            # 统计每个标签的出现次数
            for tag in tags:
                tagsDic[tag] = tagsDic.get(tag, 0) + 1

        except Exception as e:
            # 捕获解析异常，跳过错误数据
            print(f"解析标签失败: {e}")
            continue

    # 转换为词云所需格式
    return [{'name': k, 'value': v} for k, v in tagsDic.items()]


def getYearAnalysisData(hourseList):
    """
    统计房屋开盘年份的分布情况（按年份升序排列）
    :param hourseList: 房屋信息列表
    :return: 统计结果列表，每个元素为{'name': '年份', 'value': 数量}
    """
    yearDic = {}  # 键为年份字符串（如"2020"），值为数量

    for h in hourseList:
        # 跳过空值或无效日期（如空字符串、'N/A'等）
        if not h.open_date or str(h.open_date).strip() in ['', 'N/A', 'nan']:
            continue

        try:
            # 从日期中提取年份（假设格式为"YYYY-MM-DD"）
            year = h.open_date.split('-')[0]
            # 验证年份格式（4位数字）
            if len(year) == 4 and year.isdigit():
                # 累加年份计数
                if year in yearDic:
                    yearDic[year] += 1
                else:
                    yearDic[year] = 1

        except (AttributeError, IndexError):
            # 处理异常（如日期格式错误导致无法分割）
            continue

    # 按年份升序排序并转换为指定格式
    resData = []
    for key in sorted(yearDic.keys()):
        resData.append({
            'name': key,
            'value': yearDic[key]
        })
    return resData


def get_type_char_data():
    """返回房屋类型和装修情况的统计函数引用"""
    return getTypeCharDataOne, getTypeCharDataTwo


# 房屋装修情况分析数据获取函数
def getDecorationAnalysisData(hourseList):
    """获取房屋装修情况的统计数据（调用通用统计函数）"""
    return getDicData(hourseList, 'hourseDecoration')