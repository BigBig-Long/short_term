from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from model.Trading import Trading  # 确保这个导入路径正确



def GET_hourse_type_List():
    # 获取所有户型数据
    hourse_type_List = [x.house_type for x in Trading.query.all()]
    total = len(hourse_type_List)  # 总数

    # 统计每种户型的数量
    type_count = {}
    for house_type in hourse_type_List:
        type_count[house_type] = type_count.get(house_type, 0) + 1

    # 计算百分比并格式化数据
    result_data = []
    for house_type, count in type_count.items():
        percentage = (count / total) * 100
        result_data.append({
            'name': house_type,
            'value': round(percentage, 2)  # 保留两位小数
        })

    return result_data


def Get_Louceng_Data():
    # 获取所有楼层数据
    Louceng_Data = [x.floor_level for x in Trading.query.all()]

    # 初始化计数器
    low_count = 0
    middle_count = 0
    high_count = 0

    # 统计每种楼层的数量
    for floor in Louceng_Data:
        if floor == '低楼层':
            low_count += 1
        elif floor == '中楼层':
            middle_count += 1
        elif floor == '高楼层':
            high_count += 1

    # 返回统计结果列表
    return [low_count, middle_count, high_count]


def Get_cycleOption():
    # 获取所有成交周期数据
    cycleOption_Data = [x.transaction_period for x in Trading.query.all()]

    # 初始化计数器
    intervals = {
        '0-15天': 0,
        '16-30天': 0,
        '31-60天': 0,
        '61-90天': 0,
        '91-120天': 0,
        '120天以上': 0
    }

    # 统计每个区间的数量
    for period in cycleOption_Data:
        if period is not None:  # 确保数据不为空
            period = int(period)  # 转换为整数
            if 0 <= period <= 15:
                intervals['0-15天'] += 1
            elif 16 <= period <= 30:
                intervals['16-30天'] += 1
            elif 31 <= period <= 60:
                intervals['31-60天'] += 1
            elif 61 <= period <= 90:
                intervals['61-90天'] += 1
            elif 91 <= period <= 120:
                intervals['91-120天'] += 1
            elif period > 120:
                intervals['120天以上'] += 1

    # 返回统计结果列表
    return list(intervals.values())


def Get_priceTrend_Option():
    # 获取所有成交周期数据
    trading_data = Trading.query.all()

    # 初始化价格统计字典
    price_stats = {
        '2013以前': {'transaction_price': [], 'listing_price': []},
        '2014': {'transaction_price': [], 'listing_price': []},
        '2015': {'transaction_price': [], 'listing_price': []},
        '2016': {'transaction_price': [], 'listing_price': []},
        '2017': {'transaction_price': [], 'listing_price': []},
        '2017以后': {'transaction_price': [], 'listing_price': []}
    }

    # 统计每个时间段的价格
    for record in trading_data:
        if record.transaction_date:
            year = record.transaction_date.year
            if year < 2014:
                key = '2013以前'
            elif year == 2014:
                key = '2014'
            elif year == 2015:
                key = '2015'
            elif year == 2016:
                key = '2016'
            elif year == 2017:
                key = '2017'
            else:
                key = '2017以后'

            price_stats[key]['transaction_price'].append(record.transaction_price)
            price_stats[key]['listing_price'].append(record.listing_price)

    # 计算每个时间段的平均价格
    result = {
        'years': [],
        'transaction_price': [],
        'listing_price': []
    }
    for year, prices in price_stats.items():
        result['years'].append(year)
        result['transaction_price'].append(
            sum(prices['transaction_price']) / len(prices['transaction_price']) if prices['transaction_price'] else 0)
        result['listing_price'].append(
            sum(prices['listing_price']) / len(prices['listing_price']) if prices['listing_price'] else 0)

    return result


from flask_sqlalchemy import SQLAlchemy
from model.Trading import Trading  # 确保这个导入路径正确


def Get_crossAnalysisData():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化统计字典
    cross_analysis = {
        '低楼层': {'3室2厅': 0, '3室1厅': 0, '2室2厅': 0, '2室1厅': 0, '1室1厅': 0},
        '中楼层': {'3室2厅': 0, '3室1厅': 0, '2室2厅': 0, '2室1厅': 0, '1室1厅': 0},
        '高楼层': {'3室2厅': 0, '3室1厅': 0, '2室2厅': 0, '2室1厅': 0, '1室1厅': 0}
    }

    # 统计每个户型和楼层的成交量
    for record in trading_data:
        if record.floor_level in cross_analysis and record.house_type in cross_analysis[record.floor_level]:
            cross_analysis[record.floor_level][record.house_type] += 1

    # 将统计结果转换为 ECharts 需要的格式
    result = []
    floors = ['低楼层', '中楼层', '高楼层']
    house_types = ['3室2厅', '3室1厅', '2室2厅', '2室1厅', '1室1厅']
    for i, floor in enumerate(floors):
        for j, house_type in enumerate(house_types):
            result.append([i, j, cross_analysis[floor][house_type]])

    return result


def Get_priceAreaData():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化数据列表
    price_area_data = []

    # 遍历所有成交数据，提取面积、价格，并设置气泡大小为6
    for record in trading_data:
        if record.building_area and record.transaction_price:
            price_area_data.append([
                float(record.building_area),  # 面积
                float(record.transaction_price),  # 价格
                6  # 气泡大小
            ])

    return price_area_data

def Get_averagePrice():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化总价格和成交数量
    total_price = 0
    count = 0

    # 遍历所有成交数据，累加价格并统计数量
    for record in trading_data:
        if record.transaction_price:  # 确保价格字段存在
            total_price += float(record.transaction_price)  # 将价格累加
            count += 1  # 成交数量加1

    # 计算平均成交价格
    if count > 0:  # 避免除以0的情况
        average_price = total_price / count
    else:
        average_price = 0  # 如果没有成交记录，平均价格为0
    average_price = round(average_price, 2)
    return average_price

def Get_averageTime():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化总价格和成交数量
    total_period = 0
    count = 0

    # 遍历所有成交数据，累加价格并统计数量
    for record in trading_data:
        if record.transaction_price:  # 确保价格字段存在
            total_period += float(record.transaction_period)  # 将价格累加
            count += 1  # 成交数量加1

    # 计算平均成交价格
    if count > 0:  # 避免除以0的情况
        average_period  = total_period / count
    else:
        average_period = 0  # 如果没有成交记录，平均价格为0
    average_period = round(average_period, 2)
    return average_period


def get_hottest_community():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化一个字典来存储每个小区的市场热度指数
    community_heat_index = {}

    # 遍历所有成交数据
    for record in trading_data:
        if record.transaction_price and record.transaction_period is not None:
            community_name = record.community_name

            # 如果小区名称不在字典中，初始化
            if community_name not in community_heat_index:
                community_heat_index[community_name] = {
                    'total_price': 0,
                    'total_speed_index': 0,
                    'total_feature_index': 0,
                    'count': 0
                }

            # 累加成交价格
            community_heat_index[community_name]['total_price'] += record.transaction_price

            # 计算成交速度指数（成交周期越短，指数越高）
            speed_index = 1 / (record.transaction_period + 1)  # 避免除以0
            community_heat_index[community_name]['total_speed_index'] += speed_index

            # 计算房屋特征指数（根据面积、装修情况等因素）
            feature_index = (record.building_area / 200) + (record.decoration == '精装修') + (record.elevator == '有')
            community_heat_index[community_name]['total_feature_index'] += feature_index

            # 增加成交数量
            community_heat_index[community_name]['count'] += 1

    # 计算每个小区的市场热度指数
    for community, stats in community_heat_index.items():
        avg_price = stats['total_price'] / stats['count']
        avg_speed_index = stats['total_speed_index'] / stats['count']
        avg_feature_index = stats['total_feature_index'] / stats['count']
        avg_count_index = stats['count'] / len(trading_data)

        # 设置权重
        alpha = 0.3
        beta = 0.4
        gamma = 0.2
        delta = 0.1

        # 计算市场热度指数
        heat_index = alpha * avg_speed_index + beta * avg_price + gamma * avg_count_index + delta * avg_feature_index
        community_heat_index[community]['heat_index'] = heat_index

    # 找出市场热度指数最高的小区
    hottest_community = max(community_heat_index, key=lambda k: community_heat_index[k]['heat_index'])

    # 保留两位小数
    heat_index = round(community_heat_index[hottest_community]['heat_index'], 2)

    return hottest_community, heat_index

def district_counts():
    # 获取所有成交数据
    trading_data = Trading.query.all()

    # 初始化一个字典来存储每个区域的成交数量
    district_counts = {}

    # 遍历所有成交数据，统计每个区域的成交数量
    for record in trading_data:
        if record.district:
            district = record.district
            if district in district_counts:
                district_counts[district] += 1
            else:
                district_counts[district] = 1

    # 将字典转换为两个列表，用于前端
    districts = list(district_counts.keys())
    counts = list(district_counts.values())
    return districts, counts

def get_building_type_counts():
    building_type_counts = {
        '板楼': 0,
        '塔楼': 0,
        '板塔结合': 0
    }
    # 获取所有成交数据
    trading_data = Trading.query.all()
    for record in trading_data:
        if record.building_structure:
            building_type = record.building_structure
            if building_type in building_type_counts:
                building_type_counts[building_type] += 1
    return building_type_counts
