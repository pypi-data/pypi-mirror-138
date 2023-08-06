"""
Author 凌风 QQ:418155641
Email 418155641@qq.com
Date 2021-11-05
"""

#工具类
class utils(object):

    #列表转字符串
    @staticmethod
    def listTostr(list, cut=' '):
        sqlList = filter(None, list)
        return cut.join(sqlList)

    #字典转列表
    @staticmethod
    def dictToList(dict):
        res = ['(']
        for k, v in dict.items():
            res += [k, '=', utils.filterParam(v), 'and']
        res[-1] = ')'
        return res

    #列表转列表
    @staticmethod
    def listToList(list):
        res = ['(']
        for v in list:
            res += [v[0], v[1], utils.filterParam(v[2]), 'and']
        res[-1] = ')'
        return res

    #过滤参数
    @staticmethod
    def filterParam(param):
        if (isinstance(param, str)):
            return "'{}'".format(str(param).replace("'", "\\'"))
        else:
            return str(param)

    #日期转时间戳
    @staticmethod
    def strtotime(str):
        stra = str.split(' ')
        if (len(stra) == 1):
            str = stra[0] + ' 00:00:00'
        else:
            strb = stra[1].split(':')
            strblen = len(strb)
            if (strblen == 1):
                str += ':00:00'
            elif (strblen == 2):
                str += ':00'
        array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
        return int(time.mktime(array))

    #获取某年的第一天和最后一天
    @staticmethod
    def format_year_time(year):
        start = str(datetime.datetime(year, 1, 1))
        end = str(datetime.datetime(year + 1, 1, 1).date() - timedelta(days = 1)) + ' 23:59:59'
        return [utils.strtotime(start), utils.strtotime(end)]

    #获取某年某月的第一天和最后一天
    @staticmethod
    def format_month_time(year, month):
        start = str(datetime.datetime(year, month, 1))
        end = str(datetime.datetime(year, month, calendar.monthrange(year, month)[1]).date()) + ' 23:59:59'
        return [utils.strtotime(start), utils.strtotime(end)]

    #获取本周或上周的第一天和最后一天
    @staticmethod
    def format_week_time(type):
        now = datetime.datetime.now()
        if (type == 'this week'):
            start = str(now.date() - timedelta(days=now.weekday()))
            end = str(now.date() + timedelta(days = 6 - now.weekday())) + ' 23:59:59'
        else:
            start = str(now.date() - timedelta(days=now.weekday() + 7))
            end = str(now.date() - timedelta(days=now.weekday() + 1)) + ' 23:59:59'
        return [utils.strtotime(start), utils.strtotime(end)]

    #获取某天开始的一周的第一天和最后一天
    @staticmethod
    def format_weekday_time(year, month, day):
        start = str(datetime.datetime(year, month, day))
        end = str(datetime.datetime(year, month, day).date() + timedelta(days = 6)) + ' 23:59:59'
        return [utils.strtotime(start), utils.strtotime(end)]

    #获取某天的开始和结束
    @staticmethod
    def format_day_time(date):
        start = date
        end = date + ' 23:59:59'
        return [utils.strtotime(start), utils.strtotime(end)]

    #格式化条件
    @staticmethod
    def formatWhere(where):
        if (where):
            rwhere = []
            for w in where:
                w = list(filter(None, w))
                wlen = len(w)
                wlist = [w[0]]
                if (wlen == 2):
                    if (isinstance(w[1], dict)):
                        wlist += utils.dictToList(w[1])
                    elif (isinstance(w[1], list)):
                        wlist += utils.listToList(w[1])
                    else:
                        wlist += ['(', w[1], ')']
                elif (wlen == 3):
                    wlist += ['(', w[1], '=', utils.filterParam(w[2]), ')']
                else:
                    if ('like' in w[2]):
                        if (isinstance(w[3], list)):
                            wlist.append('(')
                            for v in w[3]:
                                wlist += [w[1], w[2], utils.filterParam(v), 'and']
                            wlist[-1] = ')'
                        else:
                            wlist += [w[1], w[2], utils.filterParam(w[3])]
                    elif ('between' in w[2]):
                        wlist += [w[1], w[2], utils.filterParam(w[3][0]), 'and', utils.filterParam(w[3][1])]
                    elif ('in' in w[2]):
                        if (len(w[3]) == 1):
                            wlist += [w[1], '=', utils.filterParam(w[3][0])]
                        else:
                            wlist += [w[1], w[2], str(tuple(w[3]))]
                    else:
                        wlist += [w[1], w[2], utils.filterParam(w[3])]
                rwhere += wlist
            rwhere[0] = 'where'
            return utils.listTostr(rwhere)
        else:
            return ''

    #格式化新增数据字段
    @staticmethod
    def formatDataField(data):
        fields = list(data[0].keys())
        marks = ['%s' for x in range(0, len(fields))]
        fields = utils.listTostr(fields, ', ')
        marks = utils.listTostr(marks, ', ')
        return '({0}) values ({1})'.format(fields, marks)

    #格式化更新数据
    @staticmethod
    def formatData(data, incOrDec):
        if (incOrDec):
            return '{0} = {1}'.format(data[0], data[1])
        else:
            data = ['{0} = {1}'.format(field, utils.filterParam(value)) for field, value in data.items()]
            return utils.listTostr(data, ', ')

    #异常处理
    @staticmethod
    def error(e):
        if (isinstance(e, str)):
            msg = e
        elif (len(e.args) == 1):
            msg = e.args[0]
        else:
            msg = e.args[1]
        print('error:', msg)
        exit()