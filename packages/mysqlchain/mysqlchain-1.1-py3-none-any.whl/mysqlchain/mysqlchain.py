"""
Author 凌风 QQ:418155641
Email 418155641@qq.com
Date 2021-11-05
"""

import pymysql
from .utils import utils

#链式操作mysql
class chain(object):

    #初始化类
    def __init__(self, config={}):
        default = {
            'host': 'localhost',
            'port': 3306,
            'user': '',
            'password': '',
            'database': '',
            'charset': 'utf8'
        }
        self.connect(dict(default, **config))

    #初始化参数
    def initParams(self):
        self.params = {
            'type': 'select',
            'distinct': '',
            'field': '',
            'from': 'from',
            'name': '',
            'alias': '',
            'force': '',
            'join': [],
            'union': [],
            'where': [],
            'group': '',
            'having': '',
            'order': '',
            'limit': '',
            'lock': '',
            'comment': ''
        }
        self.data = []
        self.ignoreStr = ''
        self.lastId = False
        self.incOrDec = False

    #连接数据库
    def connect(self, config):
        try:
            self.db = pymysql.connect(host=config['host'], port=config['port'], user=config['user'], password=config['password'], database=config['database'], charset=config['charset'])
            self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            utils.error(e)

    #格式化SQL语句
    def formatSql(self, type):
        if (type == 'select'):
            self.params['field'] = self.params['field'] if self.params['field'] else '*'
            self.params['join'] = utils.listTostr(self.params['join'])
            self.params['union'] = utils.listTostr(self.params['union'])
            self.params['where'] = utils.formatWhere(self.params['where'])
            sqlList = list(self.params.values())
            sql = utils.listTostr(sqlList)
        elif (type == 'insert'):
            dataField = utils.formatDataField(self.data)
            sql = utils.listTostr(['insert', self.ignoreStr, 'into', self.params['name'], dataField])
        elif (type == 'update'):
            data = utils.formatData(self.data, self.incOrDec)
            where = utils.formatWhere(self.params['where'])
            sql = utils.listTostr(['update', self.params['name'], 'set', data, where])
        elif (type == 'delete'):
            where = utils.formatWhere(self.params['where'])
            sql = utils.listTostr(['delete', 'from', self.params['name'], where])
        return sql

    #执行查询sql
    def query(self, sql='', mode='fetchall'):
        try:
            self.db.ping(reconnect=True)
            self.cursor.execute(sql)
        except Exception as e:
            utils.error(e)
        else:
            if (mode == 'fetchone'):
                result = self.cursor.fetchone()
                if (result):
                    return result
                else:
                    return {}
            elif (mode == 'fetchall'):
                result = self.cursor.fetchall()
                if (result):
                    return result
                else:
                    return []
            else:
                return True

    #执行新增和更新sql
    def execute(self, sql, mode=None):
        if (mode == 'insert'):
            data = []
            for val in self.data:
                data.append(tuple(val.values()))
            try:
                self.db.ping(reconnect=True)
                total = self.cursor.executemany(sql, data)
                self.db.commit()
                if (self.lastId):
                    total = self.cursor.lastrowid
            except Exception as e:
                self.db.rollback()
                utils.error(e)
            else:
                return total
        else:
            try:
                self.db.ping(reconnect=True)
                result = self.cursor.execute(sql)
                self.db.commit()
            except Exception as e:
                self.db.rollback()
                utils.error(e)
            else:
                return result

    #指定DISTINCT查询
    def distinct(self, distinct=True):
        if (distinct):
            self.params['distinct'] = 'distinct'
        else:
            self.params['distinct'] = ''
        return self

    #指定查询字段
    def field(self, field='*'):
        if (isinstance(field, list)):
            self.params['field'] = ','.join(field)
        else:
            self.params['field'] = field
        return self

    #指定排除的查询字段
    def withoutField(self, field):
        columns = self.columnsInfo()
        fields = []
        for column in columns:
            fields.append(column['Field'])
        if (isinstance(field, str)):
            dfields = field.replace(' ','').split(',')
        else:
            dfields = field
        fields = list(filter(lambda v: v not in dfields, fields))
        if (fields):
            self.params['field'] = ','.join(fields)
        return self

    #指定数据表名
    def name(self, name):
        self.initParams()
        self.params['name'] = name
        return self

    #指定数据表别名
    def alias(self, alias):
        self.params['alias'] = alias
        return self

    #指定强制索引
    def force(self, force):
        self.params['force'] = 'force index ({})'.format(force)
        return self

    #指定INNER JOIN查询
    def join(self, join, where):
        self.params['join'].append('inner join {0} on {1}'.format(join, where))
        return self

    #指定LEFT JOIN查询
    def leftJoin(self, join, where):
        self.params['join'].append('left join {0} on {1}'.format(join, where))
        return self

    #指定RIGHT JOIN查询
    def rightJoin(self, join, where):
        self.params['join'].append('right join {0} on {1}'.format(join, where))
        return self

    #指定UNION查询
    def union(self, union):
        if isinstance(union, list):
            for val in union:
                self.params['union'].append('union ({})'.format(val))
        else:
            self.params['union'].append('union ({})'.format(union))
        return self

    #指定UNION ALL查询
    def unionAll(self, union):
        if isinstance(union, list):
            for val in union:
                self.params['union'].append('union all ({})'.format(val))
        else:
            self.params['union'].append('union all ({})'.format(union))
        return self

    #指定AND查询条件
    def where(self, field='', operator=None, value=None):
        self.params['where'].append(['and', field, operator, value])
        return self

    #指定OR查询条件
    def whereOr(self, field='', operator=None, value=None):
        self.params['where'].append(['or', field, operator, value])
        return self

    #指定查询日期或时间
    def whereTime(self, field, operator, range):
        if (isinstance(range, str)):
            self.params['where'].append(['and', field, operator, utils.strtotime(range)])
        else:
            self.params['where'].append(['and', field, operator, [utils.strtotime(range[0]), utils.strtotime(range[1])]])
        return self

    #指定查询日期或时间在范围内
    def whereBetweenTime(self, field, startTime, endTime):
        self.params['where'].append(['and', field, 'between', [utils.strtotime(startTime), utils.strtotime(endTime)]])
        return self

    #指定查询日期或时间不在范围内
    def whereNotBetweenTime(self, field, startTime, endTime):
        self.params['where'].append(['and', field, 'not between', [utils.strtotime(startTime), utils.strtotime(endTime)]])
        return self

    #指定查询当前时间在两个时间字段范围内
    def whereBetweenTimeField(self, startField, endField):
        nowtime = str(int(time.time()))
        self.params['where'].append(['and', startField, '<=', nowtime])
        self.params['where'].append(['and', endField, '>=', nowtime])
        return self

    #指定查询当前时间不在两个时间字段范围内
    def whereNotBetweenTimeField(self, startField, endField):
        nowtime = str(int(time.time()))
        self.params['where'].append(['or', startField, '>', nowtime])
        self.params['where'].append(['or', endField, '<', nowtime])
        return self

    #指定查询年数据
    def whereYear(self, field, year='this year'):
        thisyear = datetime.datetime.now().year
        if (year == 'this year'):
            timeList = utils.format_year_time(thisyear)
        elif (year == 'last year'):
            timeList = utils.format_year_time(thisyear - 1)
        else:
            timeList = utils.format_year_time(year)
        self.params['where'].append(['and', field, 'between', timeList])
        return self

    #指定查询月数据
    def whereMonth(self, field, month='this month'):
        thisyear = datetime.datetime.now().year
        thismonth = datetime.datetime.now().month
        if (month == 'this month'):
            timeList = utils.format_month_time(thisyear, thismonth)
        elif (month == 'last month'):
            timeList = utils.format_month_time(thisyear, thismonth - 1)
        else:
            year, month = month.split('-')
            timeList = utils.format_month_time(int(year), int(month))
        self.params['where'].append(['and', field, 'between', timeList])
        return self

    #指定查询周数据
    def whereWeek(self, field, week='this week'):
        if (week == 'this week' or week == 'last week'):
            timeList = utils.format_week_time(week)
        else:
            year, month, day = week.split('-')
            timeList = utils.format_weekday_time(int(year), int(month), int(day))
        self.params['where'].append(['and', field, 'between', timeList])
        return self

    #指定查询天数据
    def whereDay(self, field, day='today'):
        if (day == 'today'):
            date = str(datetime.date.today())
        elif (day == 'yesterday'):
            date = str(datetime.datetime.now().date() - timedelta(days = 1))
        else:
            date = day
        timeList = utils.format_day_time(date)
        self.params['where'].append(['and', field, 'between', timeList])
        return self

    #指定group查询
    def group(self, group):
        self.params['group'] = 'group by {}'.format(group)
        return self

    #指定having查询
    def having(self, having):
        self.params['having'] = 'having {}'.format(having)
        return self

    #指定排序规则
    def order(self, order, sort=''):
        if (sort):
            self.params['order'] = 'order by {0} {1}'.format(order, sort)
        else:
            self.params['order'] = 'order by {}'.format(order)
        return self

    #指定随机排序
    def orderRand(self):
        self.params['order'] = 'order by rand()'
        return self

    #指定查询条数
    def limit(self, offset, length=0):
        if (length):
            self.params['limit'] = 'limit {0},{1}'.format(offset, length)
        else:
            self.params['limit'] = 'limit {}'.format(offset)
        return self

    #指定分页
    def page(self, page, listRows):
        offset = (page - 1) * listRows
        self.params['limit'] = 'limit {0},{1}'.format(offset, listRows)
        return self

    #指定LOCK锁定
    def lock(self, lock=True):
        if isinstance(lock, str):
            self.params['lock'] = lock
        else:
            self.params['lock'] = 'for update'
        return self

    #指定查询注释
    def comment(self, comment):
        self.params['comment'] = '/* {} */'.format(comment)
        return self

    #指定是否忽略已存在的数据
    def ignore(self, ignore=True):
        if (ignore):
            self.params['ignore'] = 'ignore'
        else:
            self.params['ignore'] = ''
        return self

    #指定字段自增更新
    def inc(self, field, step=1):
        self.data = [field, '{0} + {1}'.format(field, str(step))]
        self.incOrDec = True
        return self

    #指定字段自减更新
    def dec(self, field, step=1):
        self.data = [field, '{0} - {1}'.format(field, str(step))]
        self.incOrDec = True
        return self

    #查询一条数据
    def find(self):
        self.limit(1)
        sql = self.formatSql('select')
        return self.query(sql, 'fetchone')

    #查询多条数据
    def select(self):
        sql = self.formatSql('select')
        return self.query(sql)

    #查询某个字段的值
    def value(self, field):
        self.params['field'] = field
        data = self.find()
        if (data):
            return data[field]

    #查询某一列
    def column(self, field, index=''):
        if (isinstance(field, list)):
            self.params['field'] = ','.join(field)
        else:
            self.params['field'] = field.replace(' ','')
        data = self.select()
        if (data and index):
            ndata = {}
            for v in data:
                ndata[v[index]] = v
            return ndata
        else:
            return data

    #count查询
    def count(self, field='*'):
        self.params['field'] = 'count({}) as f_count'.format(field)
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_count']

    #max查询
    def max(self, field):
        self.params['field'] = 'max({}) as f_max'.format(field)
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_max']

    #min查询
    def min(self, field):
        self.params['field'] = 'min({}) as f_min'.format(field)
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_min']

    #avg查询
    def avg(self, field):
        self.params['field'] = 'avg({}) as f_avg'.format(field)
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_avg']

    #sum查询
    def sum(self, field):
        self.params['field'] = 'sum({}) as f_sum'.format(field)
        sql = self.formatSql('select')
        result = self.query(sql, 'fetchone')
        return result['f_sum']

    #新增单条数据
    def insert(self, data):
        if (isinstance(data, dict)):
            self.data = [data]
            sql = self.formatSql('insert')
            return self.execute(sql, 'insert')
        else:
            return 0

    #新增单条数据并获取ID
    def insertGetId(self, data):
        self.lastId = True
        return self.insert(data)

    #新增多条数据
    def insertAll(self, data):
        if (isinstance(data, list)):
            self.data = data
            sql = self.formatSql('insert')
            return self.execute(sql, 'insert')
        else:
            return 0

    #更新数据
    def update(self, data=None):
        if (not data is None and isinstance(data, dict)):
            self.data = data
        if (self.data):
            sql = self.formatSql('update')
            return self.execute(sql)
        else:
            return 0

    #删除数据
    def delete(self, data=None):
        if (not data is None):
            if (isinstance(data, bool) and data == True):
                sql = self.formatSql('delete')
                return self.execute(sql)
            else:
                columns = self.columnsInfo()
                for column in columns:
                    if ('auto_increment' in column.values()):
                        field = column['Field']
                        break
                if (field):
                    if (isinstance(data, list)):
                        self.params['where'].append(['and', field, 'in', data])
                    else:
                        self.params['where'].append(['and', field, '=', data])
                    sql = self.formatSql('delete')
                    return self.execute(sql)
                else:
                    return 0
        elif (self.params['where']):
            sql = self.formatSql('delete')
            return self.execute(sql)
        else:
            return 0

    #获取数据表的所有列信息
    def columnsInfo(self):
        sql = 'show full columns from {}'.format(self.params['name'])
        return self.query(sql)

    #清空数据表
    def truncate(self):
        sql = 'truncate table {}'.format(self.params['name'])
        return self.query(sql, 'truncate')

    #输出sql
    def fetchSql(self):
        return self.formatSql('select')