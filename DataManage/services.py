import csv
import os

import openpyxl
import pandas as pd
from sqlalchemy.exc import DataError, IntegrityError, OperationalError

from app.database import engine
from .schemes import TableIn


def upload_data_background(file_path: str, table_name: TableIn, chunk_size: int):
    try:
        if file_path.endswith("xlsx"):
            file_path = convert_to_csv(file_path)
        reader = pd.read_csv(file_path, chunksize=chunk_size, encoding="utf-8")
        for chunk in reader:
            try:
                chunk = data_filter(table_name, chunk)
                chunk.to_sql(table_name.value, con=engine, if_exists='append', chunksize=chunk_size, index=False)
            except Exception as e:
                print(e)
                for _, row in chunk.iterrows():
                    try:
                        row.to_frame().T.to_sql(table_name.value, con=engine, if_exists='append', index=False)
                    except DataError as e:
                        print(e.params)
                    except IntegrityError as e:
                        print(e.params)
                    except OperationalError as e:
                        print(e.params)
    except Exception as e:
        print(e)
        raise
    finally:
        os.remove(file_path)


# 数据清洗
def data_filter(table_name: TableIn, chunk):
    if table_name == TableIn.tbCell:
        chunk = chunk.drop(['SSS', 'PSS'], axis=1)
        condition = (chunk['LONGITUDE'] >= -180.0) & (chunk['LONGITUDE'] <= 180.0)  # 经度

        condition = condition & (chunk['LATITUDE'] >= -90) & (chunk['LATITUDE'] <= 90)  # 纬度
        condition = condition & (chunk['PCI'] >= 0) & (chunk['PCI'] <= 503)  # 物理小区标识介于0到503之间
        filtered = chunk[~condition]
        print(filtered)  # todo 在导入日志文件（txt 文件）中记录改行数据编号
        chunk = chunk[condition]
    # elif table_name == table_name.tbKPI:  # 没有什么好检查的

    # elif table_name == table_name.tbPRB:  # 没有什么好检查的

    else:  # table_name == table_name.tbMROData
        condition = (chunk['LteNcPci'] >= 0) & (chunk['LteNcPci'] <= 503)
        filtered = chunk[~condition]
        print(filtered)  # 在导入日志文件（txt 文件）中记录改行数据编号
        chunk = chunk[condition]

    return chunk


def convert_to_csv(path: str):
    workbook = openpyxl.load_workbook(path)
    worksheet = workbook.active

    output_file = path.replace(".xlsx", ".csv")
    with open(output_file, 'w', newline='', encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in worksheet.iter_rows(values_only=True):
            csvwriter.writerow(row)
    os.remove(path)
    return output_file

