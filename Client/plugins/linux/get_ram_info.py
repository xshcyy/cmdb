#!/usr/bin/env python3
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -- coding:utf-8 --

import subprocess
def get_ram_info():
    '''
    获取内存信息
    :return:
    '''
    raw_data = subprocess.Popen("sudo dmidecode -t memory", stdout=subprocess.PIPE, shell=True)
    raw_list = raw_data.stdout.read().split('\n')
    raw_ram_list = []
    item_list = []

    for line in raw_list:
        if line.startswith("Memory Device"):
            raw_ram_list.append(item_list)
            item_list = []
        else:
            item_list.append(line.strip())

    ram_list = []
    for item in raw_ram_list:
        item_ram_size = 0
        ram_item_to_dic = {}
        for i in item:
            data = i.split(":")
            if len(data) == 2:
                key, v = data
                if key == 'Size':
                    if v.strip() != "No Module Installed":
                        ram_item_to_dic['capacity'] = v.split()[0].strip()
                        #print(v.split()[0])
                        item_ram_size = round(int(v.split()[0]))
                    else:
                        ram_item_to_dic['capacity'] = 0
                if key == 'Type':
                    ram_item_to_dic['model'] = v.strip()
                if key == 'Manufacturer':
                    ram_item_to_dic['manufacturer'] = v.strip()
                if key == 'Serial Number':
                    ram_item_to_dic['sn'] = v.strip()
                if key == 'Asset Tag':
                    ram_item_to_dic['asset_tag'] = v.strip()
                if key == 'Locator':
                    ram_item_to_dic['slot'] = v.strip()
        if item_ram_size == 0:
            pass
        else:
            ram_list.append(ram_item_to_dic)

    raw_total_size = subprocess.Popen("cat /proc/meminfo|grep MemTotal", stdout=subprocess.PIPE, shell=True)
    raw_total_size = raw_total_size.stdout.read().split(":")
    ram_data = {'ram': ram_list}
    if len(raw_total_size) == 2:
        total_gb_size = int(int((raw_total_size[1].split()[0])) / 1024**2)
        ram_data['ram_size'] = total_gb_size
    return ram_data
if __name__ == "__main__":
    ram_data = get_ram_info()
    print(ram_data)
