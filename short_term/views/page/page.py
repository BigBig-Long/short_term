import numpy as np
from flask import Blueprint, render_template, redirect, request, session
import random
import uuid
import os
from short_term.utils.getPageData import getHomeGeoCharData, getHomeTagsData, getHomeRadarData, getHourseByHourseName, \
    getPriceCharOneData, getPriceCharDataTwo, getPriceCharDataThree, getDetailCharOne, getDetailCharTwo, \
    getTypeCharDataOne, getTypeCharDataTwo, getAnthorCharOne, getAnthorCharTwo, getAnthorCharThree, average_price, \
    getDecorationAnalysisData, getYearAnalysisData, get_type_char_data, getTop10CityAvgPrice
from short_term.utils.getPublicData import getAllHourse_infoMap, getHouseSalesData, getUserHisotryData, getHourseInfoById, addHourseInfo, deleteHourseInfo, editHourseInfo, getCitiesList, addHisotry
from short_term.utils.Test import GET_hourse_type_List, Get_Louceng_Data, Get_priceTrend_Option, Get_crossAnalysisData, Get_cycleOption, Get_averagePrice, get_hottest_community, get_building_type_counts, Get_averageTime, district_counts, Get_priceAreaData
from short_term.pred import index
from short_term.utils.getPageData import getRegionData, getRoomsData, getTagsData, getRegionPriceStackData

"""
作者注释：如果你发现在PyCharm里出现了未检测到index.html页面的警告，但是运行时并没有出错，这是因为：
        Flask 的模板搜索机制​​是：
            首先在蓝图指定的 template_folder (模版文件夹) 中查找
            然后在全局的 templates 目录查找
            最后在其他已注册蓝图的模板目录查找
        即使第一个位置没找到，可能在后续位置找到了，不信你试一下
        使用：
        pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')
        print(f"蓝图模板文件夹: {pb.template_folder}")
        查看蓝图模版文件夹是谁，这里会发现是 short_term/templates，把views里面的templates的index.html复制一份到templates里这个警告就会消失了
"""


pb = Blueprint('page', __name__, url_prefix='/page', template_folder='templates')

@pb.route('/home')
def home():
    username = session.get('username')

    hourse_data = getAllHourse_infoMap()

    geoCharData = getHomeGeoCharData(hourse_data)

    hourse_dataLen, maxPrice, maxHourseType, maxHourseSale = getHomeTagsData(hourse_data)

    radarOne, radarTwo = getHomeRadarData(hourse_data)

    # 2018-2024年成交量信息
    house_sales = getHouseSalesData()

    historyList, predMaxLen, maxPricePred, maxCity, cityPriceList = getUserHisotryData(username)

    return render_template('index.html'
                           , username=username,
                           geoCharData=geoCharData,
                           hourse_dataLen=hourse_dataLen,
                           maxPrice=maxPrice,
                           maxHourseType=maxHourseType,
                           maxHourseSale=maxHourseSale,
                           radarTwo=radarTwo,
                           radarOne=radarOne,
                           historyList=historyList,
                           predMaxLen=predMaxLen,
                           maxPricePred=maxPricePred,
                           maxCity=maxCity,
                           cityPriceList=cityPriceList,
                           house_sales=house_sales
                           )



@pb.route('/search', methods=['GET', 'POST'])
def search():
    username = session.get('username')
    hourse_data = getAllHourse_infoMap()
    maxLen = len(hourse_data)
    if request.method == 'GET':
        hourseListRandom = [hourse_data[random.randint(0, maxLen)] for x in range(5)]
        cities = [x.city for x in hourseListRandom]
    else:
        hourseListRandom = getHourseByHourseName(request.form['searchWord'], hourse_data)
        cities = [x.city for x in hourseListRandom]

    return render_template('search.html'
                           , username=username,
                           cities=cities,
                           hourseListRandom=hourseListRandom
                           )

@pb.route('/tableData', methods=['GET', 'POST'])
def tableData():
    username = session.get('username')
    hourse_data = getAllHourse_infoMap()
    return render_template('tableData.html'
                           , username=username,
                           hourse_data=hourse_data
                           )

@pb.route('/detail', methods=['GET', 'POST'])
def detail():
    username = session.get('username')
    id = request.args.get('id')
    hourseInfo = getHourseInfoById(id)
    return render_template('detail.html'
                           , username=username,
                           hourseInfo=hourseInfo
                           )

@pb.route('/addHourse', methods=['GET', 'POST'])
def addHourse():
    username = session.get('username')
    if request.method == 'GET':
        return render_template('addHourse.html'
                               , username=username,
                               )
    else:
        cover = request.files.get('cover')
        coverFilename = str(uuid.uuid4()) + '.' + cover.filename.replace('"', '').split('.')[-1]
        save_path = os.path.join(os.getcwd(), 'static', 'hourseImg', coverFilename)
        cover.save(save_path)
        addHourseInfo({
            'title': request.form.get('title'),
            'city': request.form.get('city'),
            'region': request.form.get('region'),
            'address': request.form.get('address'),
            'rooms_desc': request.form.get('rooms_desc'),
            'area_range': request.form.get('area_range'),
            'price': request.form.get('price'),
            'hourseDecoration': request.form.get('hourseDecoration'),
            'company': request.form.get('company'),
            'hourseType': request.form.get('hourseType'),
            'tags': request.form.get('tags'),
            'cover': 'http://localhost:5000/static/hourseImg/' + coverFilename
        })
        return redirect('/page/tableData')

@pb.route('/deleteHourse', methods=['GET'])
def deleteHourse():
    id = request.args.get('id')
    deleteHourseInfo(id)
    return redirect('/page/tableData')

@pb.route('/editHourse', methods=['GET', 'POST'])
def editHourse():
    username = session.get('username')
    if request.method == 'GET':
        id = request.args.get('id')
        hourseInfo = getHourseInfoById(id)
        return render_template('editHourse.html'
                               , username=username,
                               hourseInfo=hourseInfo,
                               id=id
                               )
    else:
        id = request.args.get('id')
        cover = request.files.get('cover')
        if cover:
            coverFilename = str(uuid.uuid4()) + '.' + cover.filename.replace('"', '').split('.')[-1]
            save_path = os.path.join(os.getcwd(), 'static', 'hourseImg', coverFilename)
            cover.save(save_path)
            cover_url = 'http://localhost:5000/static/hourseImg/' + coverFilename
        else:
            cover_url = '0'

        editHourseInfo({
            'title': request.form.get('title'),
            'city': request.form.get('city'),
            'region': request.form.get('region'),
            'address': request.form.get('address'),
            'rooms_desc': request.form.get('rooms_desc'),
            'area_range': request.form.get('area_range'),
            'price': request.form.get('price'),
            'hourseDecoration': request.form.get('hourseDecoration'),
            'company': request.form.get('company'),
            'hourseType': request.form.get('hourseType'),
            'tags': request.form.get('tags'),
            'cover': cover_url
        }, id)
        return redirect('/page/tableData')

@pb.route('/priceChar', methods=['GET'])
def priceChar():
    username = session.get('username')
    citiesList = getCitiesList()
    defaultCity = request.args.get('city') if request.args.get('city') else citiesList[0]
    hourseList = getAllHourse_infoMap(defaultCity)

    X, Y = getPriceCharOneData(hourseList)
    X1, Y1 = getPriceCharDataTwo(hourseList)
    Data = getPriceCharDataThree(hourseList)

    topCities, avgPrices, df = getTop10CityAvgPrice()

    box_data = {}
    for city in df['city'].unique():
        city_prices = df[df['city'] == city]['price'].values
        stats = np.percentile(city_prices, [0, 25, 50, 75, 100]).tolist()
        box_data[city] = stats

    # 按平均价格排序城市
    sorted_cities = sorted(box_data.keys(), key=lambda x: np.median(box_data[x]), reverse=True)

    # 构造 ECharts 所需格式
    chart_data = {
        "cities": sorted_cities,
        "box_data": [box_data[city] for city in sorted_cities]
    }

    return render_template('priceChar.html', username=username, citiesList=citiesList, X=X, Y=Y, defaultCity=defaultCity, X1=X1, Y1=Y1, Data=Data,topCities=topCities, avgPrices=avgPrices, chart_data=chart_data)

@pb.route('/detailChar', methods=['GET'])
def detailChar():
    hourseList = getAllHourse_infoMap()
    username = session.get('username')
    detailCharOneData = getDetailCharOne(hourseList)
    type = request.args.get('type') if request.args.get('type') else 'small'
    X, Y = getDetailCharTwo(hourseList, type)
    return render_template('detailChar.html', username=username, detailCharOneData=detailCharOneData, X=X, Y=Y)

# page.py 文件中的 typeChar 函数
@pb.route('/typeChar', methods=['GET'])
def typeChar():
    username = session.get('username')
    citiesList = getCitiesList()
    defaultCity = request.args.get('city') if request.args.get('city') else citiesList[0]
    hourseList = getAllHourse_infoMap(defaultCity)

    # 使用延迟导入的函数
    getTypeCharDataOne, getTypeCharDataTwo = get_type_char_data()
    typeCheOneData = getTypeCharDataOne(hourseList)
    typeCheTwoData = getTypeCharDataTwo(hourseList)

    # 新增数据处理
    roomsData = getRoomsData(hourseList)
    tagsData = getTagsData(hourseList)
    regionData = getRegionData(hourseList)
    region_price_stack_data = getRegionPriceStackData(hourseList)

    return render_template('typeChar.html',
                           username=username,
                           citiesList=citiesList,
                           defaultCity=defaultCity,
                           typeCheOneData=typeCheOneData,
                           typeCheTwoData=typeCheTwoData,
                           regionData=regionData,
                           roomsData=roomsData,
                           tagsData=tagsData,
                           region_price_stack_data=region_price_stack_data)

@pb.route('/anthorChar', methods=['GET'])
def anthorChar():
    username = session.get('username')
    hourseList = getAllHourse_infoMap()
    X, Y = getAnthorCharOne(hourseList)
    charTwoData = getAnthorCharTwo(hourseList)
    X1, Y1 = getAnthorCharThree(hourseList)

    # 获取年限分析和房屋装修情况分析数据
    yearAnalysisData = getYearAnalysisData(hourseList)
    decorationAnalysisData = getDecorationAnalysisData(hourseList)

    return render_template('anthorChar.html',
                           username=username,
                           X=X, Y=Y,
                           charTwoData=charTwoData,
                           X1=X1, Y1=Y1,
                           yearAnalysisData=yearAnalysisData,
                           decorationAnalysisData=decorationAnalysisData)

@pb.route('/companyCloud', methods=['GET'])
def companyCloud():
    username = session.get('username')
    hourse_type_List = GET_hourse_type_List()
    Louceng_Data = Get_Louceng_Data()
    cycleOption_Data = Get_cycleOption()
    price_data = Get_priceTrend_Option()
    crossAnalysisData = Get_crossAnalysisData()

    return render_template(
        'companyCloud.html',
        username=username,
        hourse_type_List=hourse_type_List,
        Louceng_Data=Louceng_Data,
        cycleOption_Data=cycleOption_Data,
        transaction_price=price_data['transaction_price'],
        listing_price=price_data['listing_price'],
        crossAnalysisData=crossAnalysisData,
        average_price=average_price,
    )

@pb.route('/tagCloud', methods=['GET'])
def tagCloud():
    username = session.get('username')
    average_price = Get_averagePrice()
    averageTime = Get_averageTime()
    hottest_community, heat_index = get_hottest_community()
    districts, counts = district_counts()
    building_type_counts = get_building_type_counts()
    priceAreaData = Get_priceAreaData()
    return render_template(
        'tagCloud.html',
        username=username,
        average_price=average_price,
        averageTime=averageTime,
        hottest_community=hottest_community,
        heat_index=heat_index,
        districts=districts,
        counts=counts,
        priceAreaData=priceAreaData,
        building_type_counts=building_type_counts,
    )

@pb.route('/pricePred', methods=['GET', 'POST'])
def pricePred():
    username = session.get('username')
    priceResult = 0
    citiesList = getCitiesList()
    if request.method == 'GET':
        return render_template('pricePred.html', username=username, citiesList=citiesList, priceResult=priceResult)
    else:
        statusResult = 1
        if request.form.get('sale_status') == '在售':
            statusResult = 1
        elif request.form.get('sale_status') == '已售':
            statusResult = 2
        elif request.form.get('sale_status') == '出租中':
            statusResult = 3
        elif request.form.get('sale_status') == '已出租':
            statusResult = 4
        elif request.form.get('sale_status') == '预售':
            statusResult = 5
        elif request.form.get('sale_status') == '其他':
            statusResult = 6

        model = index.model_train(index.getData())
        priceResult = index.pred(model, request.form.get('city'), int(request.form.get('rooms_desc')), int(request.form.get('area_range')), request.form.get('hourseType'), statusResult)
        addHisotry(request.form.get('city'), priceResult, username)
        return render_template('pricePred.html', username=username, citiesList=citiesList, priceResult=priceResult)
