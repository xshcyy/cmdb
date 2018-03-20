#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess


def get_disk_info():
    '''
    获取主机磁盘信息。
    只获取磁盘个数和各磁盘大小
    :return:
    '''
    raw_data = subprocess.Popen("lsblk -d -n", stdout=subprocess.PIPE, shell=True)
    raw_data = raw_data.stdout.read().decode()
    raw_list = [ i for i in raw_data.split('\n') if i != '']
    result = {'physical_disk_driver':[]}
    disk_dict = dict()
    for line in raw_list:
        if 'disk' not in line:
            continue
        line = line.split()
        disk_dict['name'] = line[0]
        disk_dict['size'] = line[3]
        result['physical_disk_driver'].append(disk_dict)

    return result

if __name__ == '__main__':
    disk_inf = get_disk_info()
    print(disk_inf)




