import csv
import logging
import os

import pandas as pd
from sqlalchemy.orm import Session
from itertools import islice
from typing import Iterator

from . import models, schemes

upload_dict = dict()


def convert_excel_to_csv(input_path, output_path):
    df = pd.read_excel(input_path)
    # 将数据写入 CSV 文件
    df.to_csv(output_path, index=False)

def batch(it: Iterator, size):
    return iter(lambda: tuple(islice(it, size)), ())


def str2schemas(table_name: str, **kwargs):
    try:
        return schemes.__dict__[table_name](**kwargs)
    except Exception:
        raise


def str2models(table_name: str, **kwargs):
    try:
        return models.__dict__[table_name](**kwargs)
    except Exception:
        raise


def upload_data_background(csvfile: str, task_id: str, table_name: str, db: Session):
    try:
        cur = 1
        with open(csvfile, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for fifty_rows in batch(iter(reader), 50):
                to_update = list()
                for i in fifty_rows:
                    try:
                        cur += 1
                        # time.sleep(0.1)
                        # 数据清洗：从要插入的记录中删除不满足约束条件的项,主要靠validator实现
                        t = str2schemas(table_name=table_name, **i)
                        to_update.append(t.dict())
                    except Exception as e:
                        upload_dict[task_id].failed += 1
                        upload_dict[task_id].failed_msg.append(
                            {
                                "line": cur,
                                "msg": e
                            }
                        )
                    finally:
                        upload_dict[task_id].processed += 1
                try:
                    create_table_by_batch(db=db, table_name=table_name, values_batch=to_update)
                except Exception as e:
                    raise e
    except Exception as e:
        raise e
    finally:
        f.close()
        # 删除临时文件
        os.remove(csvfile)
        upload_dict[task_id].done = True


def create_table_by_batch(db: Session, values_batch: list, table_name: str):
    for item in values_batch:
        try:
            record = str2models(table_name=table_name, **item)
            db.merge(record)
        except Exception as e:
            db.rollback()
            print(e)
            raise e
    db.commit()
    logging.info("插入成功")

# todo
# 批量导入数据
# def create_table_by_file(db: Session, values_dict_list: list, table_name: str):
#     try:
#         table = get_table_by_name(table_name)
#         stmt = insert(table).values(values_dict_list)
#         db.execute(stmt)
#     except Exception as e:
#         db.rollback()
#         raise e
#     else:
#         db.commit()  # 提交到数据库


# todo
# def create_table_by_line(db: Session, values_dict: dict, table_name: str):
#     try:
#         table = get_table_by_name(table_name)
#         stmt = insert(table).values(values_dict)
#         db.execute(stmt)
#     except Exception as e:
#         db.rollback()
#         raise e
#     else:
#         db.commit()  # 提交到数据库
