from datetime import datetime,timedelta
import os
import json
def convert_datetime_to_str(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, list):
                data[key] = [convert_datetime_to_str(item) for item in value]
            elif isinstance(value, dict):
                data[key] = convert_datetime_to_str(value)
    return data

def entry(results,keywords=[]):
    nowtime = datetime.now().date()
    nowtime = str(nowtime)
    s = "_"
    for key in keywords:
        s += key + "_"
    cwd = os.getcwd()
    filepath = os.path.join(cwd,"output")
    os.makedirs(filepath, exist_ok=True)
    results_str = [convert_datetime_to_str(result) for result in results]
    if os.path.isfile(os.path.join(filepath,nowtime+s)):
        print(f"already updated today")
    else:
        with open(os.path.join(filepath,nowtime+s), 'w', encoding='utf-8') as file:
            json.dump(results_str, file, ensure_ascii=False, indent=4)
        print(f"successfully updated today")
    
