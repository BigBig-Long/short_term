import pandas as pd
import numpy as np
import re


INPUT_FILE = "../spider/hourse_info.csv"
OUTPUT_FILE = "../spider/hourse_info_cleaned.csv"
PRICE_COL = 'price'
DATE_COL = 'open_date'
CITY_COL = 'city'  # 假设数据中存在城市字段
DECORATION_COL = 'hourseDecoration'


# ====================== 核心函数 ======================
def fill_price_zeros(df):
    """填充价格为0的记录：优先用城市非零均价，无城市数据则用全局均值"""
    # 计算城市级非零均价
    city_avg = df.groupby(CITY_COL)[PRICE_COL].transform(lambda x: int(x[x > 0].mean()))
    # 计算全局非零均价
    global_avg = df[PRICE_COL][df[PRICE_COL] > 0].mean().round()
    # 填充逻辑：城市均值优先，否则用全局均值
    df[PRICE_COL] = np.where(
        df[PRICE_COL] == 0,
        city_avg.fillna(global_avg),
        df[PRICE_COL]
    )
    return df


def fix_invalid_dates(df):
    """修正日期异常：99→当月第一天，空值→N/A，其他日期仅保留日期部分"""

    def process_date(date_str):
        if pd.isna(date_str) or date_str.strip() == "":
            return np.nan

        # 处理含"99"的异常日期（如"2023-09-99"→2023-09-01）
        if isinstance(date_str, str) and re.search(r'\b99\b', date_str):
            match = re.match(r'^(\d{4})[-/]?(\d{1,2})', date_str)
            if match:
                year, month = map(int, match.groups())
                month = max(1, min(12, month))
                return f"{year}-{month:02d}-01"  # 仅保留日期
            return np.nan

        # 标准化日期格式（去除时间部分）
        try:
            dt = pd.to_datetime(date_str, errors='coerce')
            if pd.isna(dt):
                return np.nan
            return dt.strftime('%Y-%m-%d')  # 强制输出日期格式
        except:
            return np.nan

    df[DATE_COL] = df[DATE_COL].apply(process_date)
    return df


# ====================== 主流程 ======================
if __name__ == "__main__":
    df = pd.read_csv(INPUT_FILE, encoding='utf-8')
    df = fill_price_zeros(df)
    df = fix_invalid_dates(df)
    df[DATE_COL] = df[DATE_COL].fillna('N/A')  # 空值统一为字符串"N/A"

    df = df[df[DECORATION_COL].notna()]
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
    print(f"清洗完成，结果已保存至 {OUTPUT_FILE}")
