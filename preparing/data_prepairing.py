import codecs
from re import findall
from re import sub
import pandas as pd

with codecs.open('preparing\\unprepaired_data.txt', 'r', encoding='utf-8-sig') as file:
    file.seek(0, 0)
    level1 = file.read().replace('\r', '').split('\n')

level2 = {}
for index, elem in enumerate(level1):
    rec = elem.split('; ')
    for i in rec:
        if i == '':
            rec.pop(rec.index(i))
    level2.update({index + 1: rec})

for key in level2:
    district_streets = {}
    for elem in level2[key]:
        if ':' in elem:
            nums = [sub(r'[а-я]', '', string) for string in findall(r'\d+\w?-?\d+|\d+', elem)]
            street_nums = []
            for num in nums:
                if '-' in num:
                    low, high = map(int, num.split('-'))
                    num = list(range(low, high+1, 2))
                    street_nums += num
                else:
                    num = int(num)
                    street_nums.append(num)
            street_nums.sort()
            elem = elem.split(':')[0]
            district_streets.update({elem: street_nums})
        elif elem not in district_streets.keys():
            district_streets.update({elem: list(range(1, 200))})
    level2[key] = district_streets

dataFrame = pd.concat({k: pd.Series(v) for k, v in level2.items()}).reset_index()
dataFrame.columns = ['d_index', 'street', 'number']

dataFrame.to_csv('preparing\\dist_data.csv', encoding='utf-8')
