import sys
import subprocess
import re

class Adb_Handler:
    def adbExists(self):
        cmd = subprocess.run(['which', 'adb'], stdout=subprocess.PIPE)
        result = cmd.stdout.decode('utf-8') 
        return (len(result) > 0 and result.splitlines()[0] != 'adb not found')

    def getDeviceList(self):
        if not self.adbExists(self):
            return []

        cmd = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
        result = cmd.stdout.decode('utf-8').splitlines()
        result = result[1:len(result) - 1]
        devices = []

        for device in result:            
            devices.append(re.split(r'\t+', device.rstrip('\t'))[0])

        return devices

    def sendSms(self, deviceId, receiver, msg):
        cmd = subprocess.run(['adb', '-s', deviceId, 'shell', 'getprop ro.build.version.release'], stdout=subprocess.PIPE)
        androidVersion = int(cmd.stdout.decode('utf-8')[0])

        if androidVersion == 5:
            #adb shell service call isms 9 s16 "com.android.mms" s16 "123456789" s16 "null" s16 "MESSAGEBODY" s16 "null" s16 "null"
            cmd = subprocess.run(
                [
                    'adb', 
                    '-s', 
                    deviceId, 
                    'shell', 
                    'service call isms 9 s16 "com.android.mms" s16 "' + receiver + '" s16 "null" s16 "' + msg + '" s16 "null" s16 "null"'
                ], 
                stdout=subprocess.PIPE
            )
        elif androidVersion == 6 or androidVersion == 7:
            #adb shell service call isms 7 i32 1 s16 "com.android.mms" s16 "123456789" s16 "null" s16 "MESSAGEBODY" s16 "null" s16 "null"
            cmd = subprocess.run(
                [
                    'adb', 
                    '-s', 
                    deviceId, 
                    'shell', 
                    'service call isms 7 i32 1 s16 "com.android.mms" s16 "' + receiver + '" s16 "null" s16 "' + msg + '" s16 "null" s16 "null"'
                ], 
                stdout=subprocess.PIPE
            )
        elif androidVersion >= 8:
            #adb shell service call isms 7 i32 0 s16 "com.android.mms.service" s16 "123456789" s16 "null" s16 "MESSAGEBODY" s16 "null" s16 "null"
            cmd = subprocess.run(
                [
                    'adb', 
                    '-s', 
                    deviceId, 
                    'shell', 
                    'service call isms 7 i32 0 s16 "com.android.mms.service" s16 "' + receiver + '" s16 "null" s16 "' + msg + '" s16 "null" s16 "null"'
                ], 
                stdout=subprocess.PIPE
            )
        
        else:
            #adb shell service call isms 5 s16 "com.android.mms" s16 "+01234567890" s16 "null" s16 "MESSAGEBODY" i32 0 i32 0
            cmd = subprocess.run(
                [
                    'adb', 
                    '-s', 
                    deviceId, 
                    'shell', 
                    'service call isms 5 s16 "com.android.mms" s16 "' + receiver + '" s16 "null" s16 "' + msg + '" i32 0 i32 0'
                ], 
                stdout=subprocess.PIPE
            )

        return (cmd.stdout.decode('utf-8').splitlines()[0] == 'Result: Parcel(00000000    \'....\')')
