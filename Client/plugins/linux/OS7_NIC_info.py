#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import subprocess


def get_NIC_info():
    '''
    获取redhat7的网卡信息
    :return:
    '''

    raw_data = subprocess.Popen("ifconfig -a", stdout=subprocess.PIPE, shell=True)
    raw_data = [ i for i in raw_data.stdout.read().decode().split("\n") if i]

    parsed_data = []
    new_line = ''
    for line in raw_data:
        if line[0].strip():
            parsed_data.append(new_line)
            new_line = line + '\n'
        else:
            new_line += line + '\n'
    parsed_data.append(new_line)
    parsed_data = [i for i in parsed_data if i]
    parsed_data = [i for i in parsed_data if 'lo' not in i]

    nic_dic = dict()
    for lines in parsed_data:
        if 'inet' in lines:
            line_list = lines.split('\n')
            nic_name = line_list[0].split(':')[0]
            mac_addr = line_list[3].split()[1]
            ip_addr = line_list[1].split()[1]
            netmask = line_list[1].split()[3]
            network = line_list[1].split()[5]
            nic_dic[mac_addr] = {
                'name': nic_name,
                'mac': mac_addr,
                'net_mask': netmask,
                'network': network,
                'bonding': [],
                'model': 'unknown',
                'ip_address': ip_addr,
            }
    for lines in parsed_data:
        if 'inet' not in lines:
            line_list = lines.split('\n')
            nic_name = line_list[0].split(':')[0]
            mac_addr = line_list[1].split()[1]
            nic_dic[mac_addr]['bonding'].append(nic_name)
    nic_list = []
    for v in nic_dic.values():
        nic_list.append(v)

    return {'nic': nic_list}
    print({'nic': nic_list})

if __name__ == '__main__':
    get_NIC_info()



