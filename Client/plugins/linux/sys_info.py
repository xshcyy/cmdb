#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess


def get_cmd_info(cmd):
    '''
    获取命令是否存在，如不存在就安装
    :param cmd:
    :return:
    '''
    which_cmd = "which " + cmd
    cmd_return_code = subprocess.call(which_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cmd_return_code:
        install_cmd = "yum -y install " + "*" + cmd + "*"
        install_cmd_code = subprocess.call(install_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if install_cmd_code:
            #判断是否安装成功，不成功返回1，表示该命令不存在且未安装成功
            return 1
    else:
        #名令存在
        return 0


def collect():
    if get_cmd_info("dmidecode") == 0:
        filter_keys = ['Manufacturer', 'Serial Number', 'Product Name', 'UUID', 'Wake-up Type']
        raw_data = {}

        for key in filter_keys:
            try:
                res = subprocess.Popen("sudo dmidecode -t system|grep '%s'" % key,
                                       stdout=subprocess.PIPE, shell=True)
                result = res.stdout.read().decode()
                data_list = result.split(':')

                if len(data_list) > 1:
                    raw_data[key] =data_list[1].strip()
                else:
                    raw_data[key] = -1
            except Exception as e:
                print(e)
                raw_data[key] = -2

        data = dict()
        data['asset_type'] = 'server'
        data['manufacturer'] = raw_data['Manufacturer']
        data['sn'] = raw_data['Serial Number']
        data['model'] = raw_data['Product Name']
        data['uuid'] = raw_data['UUID']
        data['wake_up_type'] = raw_data['Wake-up Type']

        data.update(get_os_info())
        data.update(get_cpu_info())
        data.update(get_ram_info())
        data.update(get_nic_info())
        data.update(get_disk_info())
    else:
        data = dict()
    return data


def get_os_info():
    '''
    获取操作系统信息
    :return:
    '''
    if get_cmd_info("lsb_release") == 0:
        distributor = subprocess.Popen("lsb_release -a|grep 'Distributor ID'",
                                       stdout=subprocess.PIPE, shell=True)
        distributor = distributor.stdout.read().decode().split(":")

        release = subprocess.Popen("lsb_release -a|grep 'Description'",
                                   stdout=subprocess.PIPE, shell=True)
        release = release.stdout.read().decode().split(":")
        data_dict = {
            "os_distribution": distributor[1].strip() if len(distributor) > 1 else "",
            "os_release": release[1].strip() if len(release) > 1 else "",
            "os_type": "Linux"
        }
    else:
        data_dict = {}
    return data_dict

def get_cpu_info():
    '''
    获取cpu信息
    :return:
    '''
    base_cmd = 'cat /proc/cpuinfo'

    raw_data = {
        'cpu_model': "%s |grep 'model name' |head -1" % base_cmd,
        'cpu_count': "%s |grep 'processor' |wc -l" % base_cmd,
        'cpu_core_count': "%s |grep 'cpu cores'|awk -F: '{SUM +=$2} END {print SUM}'" % base_cmd,
    }

    for key, cmd in raw_data.items():
        try:
            cmd_res = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            raw_data[key] = cmd_res.stdout.read().decode().strip()
        except ValueError as e:
            print(e)
            raw_data[key] = ""

    data = {
        "cpu_count": raw_data["cpu_count"],
        "cpu_core_count": raw_data["cpu_core_count"]
    }
    cpu_model = raw_data["cpu_model"].split(":")

    if len(cpu_model) > 1:
        data["cpu_model"] = cpu_model[1].strip()
    else:
        data["cpu_model"] = -1

    return data

def get_ram_info():
    '''
    获取内存信息
    :return:
    '''
    raw_data = subprocess.Popen("dmidecode -t memory", stdout=subprocess.PIPE, shell=True)
    raw_list = raw_data.stdout.read().decode().split('\n')
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
    raw_total_size = raw_total_size.stdout.read().decode().split(":")
    ram_data = {'ram': ram_list}
    if len(raw_total_size) == 2:
        total_gb_size = int(int((raw_total_size[1].split()[0])) / 1024**2)
        ram_data['ram_size'] = total_gb_size
    return ram_data

def get_nic_info():
    '''
    获取网卡信息
    :return:
    '''
    os_version = subprocess.Popen('uname -r', stdout=subprocess.PIPE, shell=True)
    os_version = os_version.stdout.read().split('.')[-2]
    if os_version == 'el7':
        from . import OS7_NIC_info
        OS7_NIC_info.get_NIC_info()
    else:
        from . import OS_NIC_info
        OS_NIC_info.get_NIC_info()


def get_disk_info():
    '''
    获取存储信息。
    本脚本只针对
    :return:
    '''
    raw_data = subprocess.Popen("lsblk -d -n", stdout=subprocess.PIPE, shell=True)
    raw_data = raw_data.stdout.read().decode()
    raw_list = [i for i in raw_data.split('\n') if i != '']
    result = {'physical_disk_driver': []}
    for line in raw_list:
        disk_dict = dict()
        if 'disk' not in line:
            continue
        line = line.split()
        disk_dict['name'] = line[0]
        disk_dict['size'] = line[3]
    result['physical_disk_driver'].append(disk_dict)

    return result


if __name__ == '__main__':
    # 收集信息功能测试
    d = collect()
    print(d)
