#!/usr/bin/python
#encoding:utf-8
import os
import sys
import json
import time


server = sys.argv[1]
sensor = sys.argv[2]
request_type = sys.argv[3]
cache_file = '/var/tmp/ipmi_sensor_' + server
user = 'ipmi_user'
pwd = 'ipmi_pwd'


def is_float(s):
    try:
        float(s)
        return True
    except:
        return False


def not_contain(s1,s2):
    if s1 in s2:
        return False
    return True


def create_ipmi_file():
    ipmi_cmd = 'ipmi-sensors -D LAN2_0 -h {} -u {} -p {} -l USER -W discretereading --no-header-output --quiet-cache --sdr-cache-recreate --comma-separated-output --entity-sensor-names 2>/dev/null'
    ipmi_cmd = ipmi_cmd.format(server, user, pwd)
    ipmi_list = os.popen(ipmi_cmd).readlines()
    count = 0
    while len(ipmi_list) == 0 and count < 5:
        ipmi_list = os.popen(ipmi_cmd).readlines()
        count += 1
    if (os.path.exists(cache_file)) and os.path.getsize(cache_file) > 100:
        return
    if os.path.exists(cache_file):
        return
    open(cache_file + '.lock', 'a').close()
    with open(cache_file, 'w') as f:
        f.write(str(time.time())+'\n')
        for ipmi in ipmi_list:
            f.write(ipmi)
    os.remove(cache_file + '.lock')


def ipmi_discovery():
    data_json = {"data": []}
    with open(cache_file, 'r') as f:
        for data_txt in f:
            try:
                num, key, section, value, measure, status = data_txt.split(',')
            except:
                continue
            if sensor.lower() == section.lower():
                if 'number' in request_type and is_float(value) and float(value) != 0:
                    d = { 
                        "{#CLASS}": "sensor",
                        "{#KEY}": key,
                        "{#SECTION}": section,
                        "{#TYPE}": "number",
                        "{#MEASURE}":measure
                    }
                    data_json["data"].append(d)
                elif 'status' in request_type and not_contain('N/A',status) and status != '':
                    d = {
                        "{#CLASS}": "sensor",
                        "{#KEY}": key,
                        "{#SECTION}": section,
                        "{#TYPE}": "status"
                    }
                    data_json["data"].append(d)
    result = json.dumps(data_json, indent=4)
    print(result)


create_ipmi_file()
ipmi_discovery()
