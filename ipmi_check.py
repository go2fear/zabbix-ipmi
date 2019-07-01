#!/usr/bin/python
# encoding:utf-8

import os
import sys
import time

server = sys.argv[1]
sensor = sys.argv[2]
request_type = sys.argv[3]
user = 'ipmi_user'
pwd = 'ipmi_pwd'
cache_file = '/var/tmp/ipmi_sensor_' + server


def fru_chassis():
    ipmi_cmd = '/usr/sbin/ipmi-{} -D LAN2_0 -h {} -u {} -p {} -l USER -W discretereading'
    if sensor == 'fru':
        ipmi_cmd += ' -e 0 2>/dev/null'
    else:
        ipmi_cmd += ' --get-status 2>/dev/null'
    ipmi_cmd = ipmi_cmd.format(sensor, server, user, pwd)
    ipmi_list = os.popen(ipmi_cmd).readlines()
    count = 0
    while len(ipmi_list) == 0 and count < 5:
        ipmi_list = os.popen(ipmi_cmd).readlines()
        count += 1
    for ipmi in ipmi_list:
        try:
            key, value = ipmi.split(':')
        except:
            continue
        if request_type.lower() == key.strip().lower():
            print(value.strip())
            break


def create_ipmi_file():
    ipmi_cmd = 'ipmi-sensors -D LAN2_0 -h {} -u {} -p {} -l USER -W discretereading --no-header-output --quiet-cache --sdr-cache-recreate --comma-separated-output --entity-sensor-names 2>/dev/null'
    ipmi_cmd = ipmi_cmd.format(server, user, pwd)
    ipmi_list = os.popen(ipmi_cmd).readlines()
    count = 0
    while len(ipmi_list) == 0 and count < 5:
        ipmi_list = os.popen(ipmi_cmd).readlines()
        count += 1
    if os.path.exists(cache_file + '.lock'):
        return
    else:
        open(cache_file + '.lock', 'a').close()
        with open(cache_file, 'w') as f:
            f.write(str(time.time()) + '\n')
            for sensor in ipmi_list:
                f.write(sensor)
        os.remove(cache_file + '.lock')


def rewrite_ipmi_file():
    with open(cache_file, 'r') as f:
        lines = f.readlines()
        ipmi_create_time = float(lines[0])
        if time.time() - ipmi_create_time > 120 or not (os.path.exists(cache_file)) or os.path.getsize(
                cache_file) < 100:
            create_ipmi_file()


def ipmi_check():
    with open(cache_file, 'r') as txt:
        for data_txt in txt:
            try:
                num, key, section, value, measure, status = data_txt.split(',')
            except:
                continue
            if sensor == key:
                if 'number' in request_type:
                    result = float(value)
                    print(result)
                    return
                elif 'status' in request_type:
                    result = status.strip().replace('\'', '')
                    print(result)
                    return


if sensor == 'fru' or sensor == 'chassis':
    fru_chassis()
else:
    rewrite_ipmi_file()
    ipmi_check()
