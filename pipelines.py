# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import MySQLdb.cursors


class ShanbayPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # 保存方法3 mysql保存
    # 说明: 解析速度大于入库速度 同步可能会造成堵塞
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'root', 'article', charset="utf8", use_unicode=True)
        # 主机名 用户名 密码 数据库
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into shanbay(user_name, listen_num, reading_num, word_num, training_num,sentence_num,course_num,speaking_num, voc_all, study_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["user_name"], item["listen_num"], item["reading_num"], item["word_num"], item["training_num"],item["sentence_num"],item["course_num"],item["speaking_num"],item["voc_all"],item["study_time"]))
        self.conn.commit()