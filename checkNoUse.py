import json, os
from pprint import pprint

if __name__ == '__main__':
    with open('cron.json', 'r') as f:
        对象 = json.load(f)
    for files in os.listdir('./'):
        if os.path.isfile(files):
            if files in 对象:
                pass
            else:
                if '.js' in files or '.ts' in files:
                    print(files)