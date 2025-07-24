import json
from datetime import datetime
from short_term.db import database
from short_term.model.History import History
from short_term.model.Hourse_info import Hourse_info
from short_term.model.User import User
from short_term.utils.query import querys

cityList = [
    {'province': '北京', 'city': ['北京市']},
    {'province': '天津', 'city': ['天津市']},
    {'province': '河北',
     'city': ['石家庄市', '唐山市', '秦皇岛市', '邯郸市', '邢台市', '保定市', '张家口市', '承德市', '沧州市', '廊坊市',
              '衡水市']},
    {'province': '山西',
     'city': ['太原市', '大同市', '阳泉市', '长治市', '晋城市', '朔州市', '晋中市', '运城市', '忻州市', '临汾市',
              '吕梁市']},
    {'province': '内蒙古',
     'city': ['呼和浩特市', '包头市', '乌海市', '赤峰市', '通辽市', '鄂尔多斯市', '呼伦贝尔市', '巴彦淖尔市',
              '乌兰察布市', '兴安盟', '锡林郭勒盟', '阿拉善盟']},
    {'province': '辽宁',
     'city': ['沈阳市', '大连市', '鞍山市', '抚顺市', '本溪市', '丹东市', '锦州市', '营口市', '阜新市', '辽阳市',
              '盘锦市', '盘锦市', '朝阳市', '葫芦岛市']},
    {'province': '吉林',
     'city': ['长春市', '吉林市', '四平市', '辽源市', '通化市', '白山市', '松原市', '白城市', '延边']},
    {'province': '黑龙江',
     'city': ['哈尔滨市', '齐齐哈尔市', '鸡西市', '鹤岗市', '双鸭山市', '大庆市', '伊春市', '佳木斯市', '七台河市',
              '牡丹江市', '黑河市', '绥化市',
              '大兴安岭地区', ]},
    {'province': '上海', 'city': ['上海市']},
    {'province': '江苏',
     'city': ['南京市', '无锡市', '徐州市', '常州市', '苏州市', '南通市', '连云港市', '淮安市', '盐城市', '扬州市',
              '镇江市', '泰州市', '宿迁市']},
    {'province': '浙江',
     'city': ['杭州市', '宁波市', '温州市', '嘉兴市', '湖州市', '绍兴市', '金华市', '衢州市', '舟山市', '台州市',
              '丽水市']},
    {'province': '安徽',
     'city': ['合肥市', '芜湖市', '蚌埠市', '淮南市', '马鞍山市', '淮北市', '铜陵市', '安庆市', '黄山市', '滁州市',
              '阜阳市', '宿州市', '六安市', '亳州市',
              '池州市', '宣城市']},
    {'province': '福建',
     'city': ['福州市', '厦门市', '莆田市', '三明市', '泉州市', '漳州市', '南平市', '龙岩市', '宁德市']},
    {'province': '江西',
     'city': ['南昌市', '景德镇市', '萍乡市', '九江市', '新余市', '鹰潭市', '赣州市', '吉安市', '宜春市', '抚州市',
              '上饶市']},
    {'province': '山东',
     'city': ['济南市', '青岛市', '淄博市', '枣庄市', '东营市', '烟台市', '潍坊市', '济宁市', '泰安市', '威海市',
              '日照市', '莱芜市', '临沂市', '德州市',
              '聊城市', '滨州市', '菏泽市']},
    {'province': '河南',
     'city': ['郑州市', '开封市', '洛阳市', '平顶山市', '安阳市', '鹤壁市', '新乡市', '焦作市', '济源市', '濮阳市',
              '许昌市', '漯河市', '三门峡市', '南阳市',
              '商丘市', '信阳市', '周口市', '驻马店市']},
    {'province': '湖北',
     'city': ['武汉市', '黄石市', '十堰市', '宜昌市', '襄阳市', '鄂州市', '荆门市', '孝感市', '荆州市', '黄冈市',
              '咸宁市', '随州市', '恩施', '仙桃市',
              '潜江市', '天门市', '神农架林区']},
    {'province': '湖南',
     'city': ['长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市', '张家界市', '益阳市', '郴州市',
              '永州市', '怀化市', '娄底市', '湘西']},
    {'province': '广东',
     'city': ['广州市', '韶关市', '深圳市', '珠海市', '汕头市', '佛山市', '江门市', '湛江市', '茂名市', '肇庆市',
              '惠州市', '梅州市', '汕尾市', '河源市',
              '阳江市', '清远市', '东莞市', '中山市', '东沙群岛', '潮州市', '揭阳市', '云浮市']},
    {'province': '广西',
     'city': ['南宁市', '柳州市', '桂林市', '梧州市', '北海市', '防城港市', '钦州市', '贵港市', '玉林市', '百色市',
              '贺州市', '河池市', '来宾市', '崇左市']},
    {'province': '海南',
     'city': ['海口市', '三亚市', '三沙市', '五指山市', '琼海市', '儋州市', '文昌市', '万宁市', '东方市', '定安县',
              '屯昌县', '澄迈县', '临高县', '白沙',
              '昌江', '乐东', '陵水', '保亭', '琼中']},
    {'province': '重庆', 'city': ['重庆市']},
    {'province': '四川',
     'city': ['成都市', '自贡市', '攀枝花市', '泸州市', '德阳市', '绵阳市', '广元市', '遂宁市', '内江市', '乐山市',
              '南充市', '眉山市', '宜宾市', '广安市',
              '达州市', '雅安市', '巴中市', '资阳市', '阿坝', '甘孜', '凉山']},
    {'province': '贵州',
     'city': ['贵阳市', '六盘水市', '遵义市', '安顺市', '铜仁市', '黔西南', '毕节市', '黔东南', '黔南']},
    {'province': '云南',
     'city': ['昆明市', '曲靖市', '玉溪市', '保山市', '昭通市', '丽江市', '普洱市', '临沧市', '楚雄', '红河', '文山',
              '西双版纳', '大理', '德宏', '怒江',
              '迪庆']},
    {'province': '西藏自治区',
     'city': ['拉萨市', '昌都地区', '山南地区', '日喀则地区', '那曲地区', '阿里地区', '林芝地区']},
    {'province': '陕西',
     'city': ['西安市', '铜川市', '宝鸡市', '咸阳市', '渭南市', '延安市', '汉中市', '榆林市', '安康市', '商洛市']},
    {'province': '甘肃',
     'city': ['兰州市', '嘉峪关市', '金昌市', '白银市', '天水市', '武威市', '张掖市', '平凉市', '酒泉市', '庆阳市',
              '定西市', '陇南市', '临夏', '甘南']},
    {'province': '青海', 'city': ['西宁市', '海东市', '海北', '黄南', '海南', '果洛', '玉树', '海西']},
    {'province': '宁夏回族自治区', 'city': ['银川市', '石嘴山市', '吴忠市', '固原市', '中卫市']},
    {'province': '新疆维吾尔自治区',
     'city': ['乌鲁木齐市', '克拉玛依市', '吐鲁番地区', '哈密地区', '昌吉', '博尔塔拉', '巴音郭楞', '阿克苏地区',
              '克孜勒苏柯尔克孜自治州', '喀什地区', '和田地区', '伊犁',
              '塔城地区', '阿勒泰地区', '石河子市', '阿拉尔市', '图木舒克市', '五家渠市']},
    {'province': '台湾',
     'city': ['台北市', '高雄市', '台南市', '台中市', '金门县', '南投县', '基隆市', '新竹市', '嘉义市', '新北市',
              '宜兰县', '新竹县', '桃园县', '苗栗县',
              '彰化县', '嘉义县', '云林县', '屏东县', '台东县', '花莲县', '澎湖县', '连江县']},
    {'province': '香港特别行政区', 'city': ['香港岛', '香港岛', '新界']},
    {'province': '澳门特别行政区', 'city': ['澳门', '离岛']}
]


def getUserHisotryData(username):
    user = querys('select * from user where user_name = %s', [username], 'select')[0]
    hisotryList = querys('select * from history where user_id = %s', [int(user[0])], 'select')
    maxPrice = 0
    cityLenDic = {}
    cityPriceDic = {}
    for h in hisotryList:
        if maxPrice < float(h[2]): maxPrice = float(h[2])
        if cityLenDic.get(h[1], -1) == -1:
            cityLenDic[h[1]] = 1
        else:
            cityLenDic[h[1]] += 1
        if cityPriceDic.get(h[1], -1) == -1:
            cityPriceDic[h[1]] = float(h[2])
        else:
            cityPriceDic[h[1]] += float(h[2])
    cityPriceList = []
    for key, value in cityPriceDic.items():
        cityPriceList.append({
            'name': key,
            'value': value
        })
    sorteCityLen = list(sorted(cityLenDic.items(), key=lambda x: x[1], reverse=True))
    if sorteCityLen:
        return hisotryList, len(hisotryList), maxPrice, sorteCityLen[0][0], cityPriceList
    else:
        return hisotryList, len(hisotryList), maxPrice, 0, cityPriceList


def getCitiesList():
    hourseList = list(set([x.city for x in Hourse_info.query.all()]))
    return hourseList


def getAllHourse_infoMap(city=''):
    if city != '':
        hourseList = Hourse_info.query.filter_by(city=city).all()
    else:
        hourseList = Hourse_info.query.all()

    def map_fn(item):
        item.rooms_desc = json.loads(item.rooms_desc)
        item.area_range = json.loads(item.area_range)
        item.tags = json.loads(item.tags)
        item.totalPrice_range = json.loads(item.totalPrice_range)
        return item

    hourseListMap = list(map(map_fn, hourseList))

    return hourseListMap


def getHourseInfoById(id):
    hourseInfo = Hourse_info.query.filter_by(id=id).first()
    hourseInfo.rooms_desc = json.loads(hourseInfo.rooms_desc)
    hourseInfo.tags = json.loads(hourseInfo.tags)
    hourseInfo.area_range = json.loads(hourseInfo.area_range)
    hourseInfo.totalPrice_range = json.loads(hourseInfo.totalPrice_range)
    return hourseInfo


def addHisotry(city, price, username):
    user = User.query.filter_by(user_name=username).first()
    newHistory = History(city=city, price=price, user=user)
    database.session.add(newHistory)
    database.session.commit()


def addHourseInfo(hourseInfo):
    hourseInfo['rooms_desc'] = json.dumps(hourseInfo['rooms_desc'].split('，'))
    hourseInfo['area_range'] = json.dumps(hourseInfo['area_range'].split('-'))
    hourseInfo['tags'] = json.dumps(hourseInfo['tags'].split('，'))
    hourseInfo['all_ready'] = '1'
    hourseInfo['on_time'] = '0000-00-00 00:00:00'
    hourseInfo['totalPrice_range'] = json.dumps([0])
    hourseInfo['sale_status'] = '1'
    hourseInfo['detail_url'] = '0'
    now = datetime.now()
    hourseInfo['open_date'] = f"{now.year}-{now.month:02d}-{now.day:02d}"
    hourse = Hourse_info(title=hourseInfo['title'], city=hourseInfo['city'], region=hourseInfo['region'],
                         address=hourseInfo['address'], rooms_desc=hourseInfo['rooms_desc'],
                         area_range=hourseInfo['area_range'],
                         price=hourseInfo['price'], hourseDecoration=hourseInfo['hourseDecoration'],
                         company=hourseInfo['company'], hourseType=hourseInfo['hourseType'], tags=hourseInfo['tags'],
                         cover=hourseInfo['cover'],
                         all_ready=hourseInfo['all_ready'], on_time=hourseInfo['on_time'],
                         totalPrice_range=hourseInfo['totalPrice_range'], sale_status=hourseInfo['sale_status'],
                         detail_url=hourseInfo['detail_url'], open_date=hourseInfo['open_date']
                         )

    database.session.add(hourse)
    database.session.commit()


def editHourseInfo(hourseInfo, id):
    hourseInfo['rooms_desc'] = json.dumps(hourseInfo['rooms_desc'].split('，'))
    hourseInfo['area_range'] = json.dumps(hourseInfo['area_range'].split('-'))
    hourseInfo['tags'] = json.dumps(hourseInfo['tags'].split('，'))
    hourse = getHourseInfoById(id)
    hourse.title = hourseInfo['title']
    hourse.totalPrice_range = json.dumps(hourse.totalPrice_range)
    hourse.city = hourseInfo['city']
    hourse.region = hourseInfo['region']
    hourse.address = hourseInfo['address']
    hourse.rooms_desc = hourseInfo['rooms_desc']
    hourse.area_range = hourseInfo['area_range']
    hourse.price = hourseInfo['price']
    hourse.hourseDecoration = hourseInfo['hourseDecoration']
    hourse.company = hourseInfo['company']
    hourse.hourseType = hourseInfo['hourseType']
    hourse.tags = hourseInfo['tags']
    if hourseInfo['cover'] != '0':
        hourse.cover = hourseInfo['cover']
    database.session.commit()


def deleteHourseInfo(id):
    hourseInfo = getHourseInfoById(id)
    database.session.delete(hourseInfo)
    database.session.commit()
