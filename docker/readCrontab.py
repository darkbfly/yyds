from itsdangerous import json
import pyperclip
from croniter import croniter_range
from datetime import datetime, timedelta
import json

触发器字符串 = "\n        - name: {name}\n          type: timer\n          config:    \n            payload: '{name}'    \n            cronExpression: '{cron}'    \n            enable: true"


def 解析crontab(strCrontab):
    listData = []
    tomorrow = datetime.strptime(
        (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S'),
        "%Y-%m-%d %H:%M:%S")
    for run_time in croniter_range(datetime.now(), tomorrow, strCrontab):
        print(run_time)
        date = datetime.strptime(str(run_time), '%Y-%m-%d %H:%M:%S')
        listData.append(date.hour)
    return list(set(listData))


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


if __name__ == '__main__':
    触发器数据 = {}
    分钟脚本 = []
    with open("crontab_list.sh", 'r', encoding='utf8') as f:
        数据 = f.readlines()
    for item in 数据:
        if item.__contains__("#"):
            continue
        elif item.__contains__("node") == False:
            continue
        else:
            x = item.split(' ')
            crontabstr = x[0] + ' ' + x[1] + ' ' + x[2] + ' ' + x[3] + ' ' + x[
                4]
            if is_number(x[0]) == False:
                print(x[6].replace('/scripts/', '').replace('.js', '') +
                      '不是小时计数')
                分钟脚本.append(x[6].replace('/scripts/', '').replace('.js', ''))
                continue
            # print(crontabstr)

            # 触发器数据 += 触发器字符串.format(name=,
            #                        cron=crontabstr)
            触发器数据[x[6].replace('/scripts/',
                               '').replace('.js', '')] = 解析crontab(crontabstr)
    print(触发器数据)
    print(分钟脚本)
    pyperclip.copy(json.dumps(触发器数据))