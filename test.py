import json


data = []
data_dict = {}
data.append(data_dict)
data_dict['people'] = []
data_dict['people'].append({
    'name': 'Scott',
    'website': 'pythonist.ru',
    'from': 'Nebraska'
})
data_dict['people'].append({
    'name': 'Larry',
    'website': 'pythonist.ru',
    'from': 'Michigan'
})
data_dict['people'].append({
    'name': 'Tim',
    'website': 'pythonist.ru',
    'from': 'Alabama'
})


try:
    json_data = json.load(open("db.json"))
    json_data.append(data)
except:
    json_data = data
with open('db.json', 'w') as outfile:
    json.dump(json_data, outfile)