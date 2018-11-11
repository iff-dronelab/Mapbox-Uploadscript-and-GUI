import mapbox
import os
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')
account = config['Accountdata']
upload = config['Uploaddata']

username=account['username']
access_token=account['accesstoken']

path=upload['path']
UAV=upload['UAVname']
datatype=upload['datatype']
start=int(upload['startingtileset'])

while True:
    if os.path.isfile(path  + '/' + UAV + str(start) + '.' + datatype) == True:
        print('Data ' + UAV + str(start) + ' found! Preparing to upload:\n')

        res = mapbox.Uploader(access_token=access_token)._get_credentials()
        with open(path  + '/' + UAV + str(start) + '.' + datatype, 'rb') as src:
            stage_url = mapbox.Uploader(access_token=access_token).stage(src)

        print('Data ' + UAV + str(start) + ' successfully staged. Start upload:\n')

        def print_cb(num_bytes):
            print("{0} bytes uploaded".format(num_bytes))

        with open(path  + '/' + UAV + str(start) + '.' + datatype, 'rb') as src:
            res = mapbox.Uploader(access_token=access_token).upload(src, UAV + str(start), callback=print_cb)
            print('Data ' + UAV + str(start) + ' successfully uploaded. Search for next:\n')
            start += 1
            time.sleep(3)

    else:
        print('Data ' + UAV + str(start) + ' not found. Sleep 3 seconds and try again.\n')
        time.sleep(3)

