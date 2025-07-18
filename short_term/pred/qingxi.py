import pandas as pd
import re
from datetime import datetime

# ====================== 配置参数 ======================
# 假设数据文件路径（根据实际路径调整）
INPUT_FILE = "../spider/hourseInfoData.csv"  # 或 .xlsx
OUTPUT_FILE = "../spider/cleaned_house_data1.csv"


# 目标列名（根据实际数据调整，假设open_date列名为'open_date'）
OPEN_DATE_COL = 'open_date'

# 允许的时间格式（可根据实际数据补充）
ALLOWED_TIME_PATTERNS = [
    r'^\d{4}-\d{1,2}-\d{1,2}$',  # YYYY-MM-DD（如2021-05-14）
    r'^\d{4}/\d{1,2}/\d{1,2}$',  # YYYY/MM/DD（如2021/5/14）
    r'^\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{2}(:\d{2})?$'  # YYYY-MM-DD HH:mm[:ss]（如2021-05-14 10:48）
]

# 非法日期阈值（月份1-12，日期根据月份动态判断）
MAX_DAYS_PER_MONTH = {
    1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
    7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
}


# ====================== 核心函数 ======================
def is_valid_time(time_str):
    if time_str == "N/A":
        return True
    """判断时间字符串是否合法（格式+日期有效性）"""
    # 步骤1：过滤含非法字符（中文、方括号、编码符号等）
    if re.search(r'[\u4e00-\u9fa5]', str(time_str)):  # 包含中文字符
        return False
    if re.search(r'\[.*?\]', str(time_str)):  # 包含方括号内的编码（如\u4f4e）
        return False
    if re.search(r'[^\w\-/:.]', str(time_str)):  # 包含其他非法符号（如^、$、空格等）
        return False

    # 步骤2：匹配允许的时间格式
    matched = False
    for pattern in ALLOWED_TIME_PATTERNS:
        if re.match(pattern, str(time_str)):
            matched = True
            break
    if not matched:
        return False

    # 步骤3：验证日期有效性（月份1-12，日期不超过当月最大天数）
    try:
        # 提取日期部分（忽略时间）
        date_part = str(time_str).split()[0]
        year, month, day = map(int, date_part.split('-')) if '-' in date_part else \
            map(int, date_part.split('/'))

        # 验证月份
        if month < 1 or month > 12:
            return False

        # 验证日期（考虑闰年2月）
        max_day = MAX_DAYS_PER_MONTH[month]
        if month == 2 and (year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)):
            max_day = 29  # 闰年2月有29天
        if day < 1 or day > max_day:
            return False

        # 验证时间部分（如果有）
        if ' ' in time_str:
            time_part = time_str.split()[1]
            hh, mm = map(int, time_part.split(':')[:2])
            if hh < 0 or hh > 23 or mm < 0 or mm > 59:
                return False

        return True
    except (ValueError, IndexError):
        return False


def clean_open_date_data(df):
    """清洗open_date列的异常时间和缺失值"""
    # 复制原始数据避免修改原数据
    df_clean = df.copy()

    # ---------------------- 步骤1：处理缺失值 ----------------------
    # 定义缺失值标记（包括空字符串、NaN、"缺失值"文本等）
    missing_mask = (
            df_clean[OPEN_DATE_COL].isna() |
            (df_clean[OPEN_DATE_COL] == '') |
            (df_clean[OPEN_DATE_COL].astype(str).str.strip().str.lower() == '缺失值')
    )

    # 将所有缺失值替换为N/A
    df_clean.loc[missing_mask, OPEN_DATE_COL] = "N/A"

    # ---------------------- 步骤2：过滤异常时间 ----------------------
    # 应用时间合法性检测函数
    valid_time_mask = df_clean[OPEN_DATE_COL].apply(is_valid_time)
    df_clean = df_clean[valid_time_mask]

    # ---------------------- 步骤3：输出清洗结果 ----------------------
    print(f"原始数据量: {len(df)}")
    print(f"清洗后数据量: {len(df_clean)}")
    print(f"删除原因分布:")
    print(f"  - 缺失值: {len(df[missing_mask])}")
    print(f"  - 异常时间: {len(df[~missing_mask]) - len(df_clean)}")

    return df_clean


# ====================== 主流程 ======================
if __name__ == "__main__":
    # 读取数据（假设为CSV，若为Excel使用pd.read_excel）
    try:
        df = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"读取数据失败: {e}")
        exit(1)

    # 检查目标列是否存在
    if OPEN_DATE_COL not in df.columns:
        print(f"错误：数据中不存在列 '{OPEN_DATE_COL}'")
        exit(1)

    # 清洗数据
    df_clean = clean_open_date_data(df)

    # 保存清洗后数据
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print(f"清洗后数据已保存至: {OUTPUT_FILE}")