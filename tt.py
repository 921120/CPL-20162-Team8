#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:

$ ./record_measurments.py out.txt'''
import sys
import time 
from rplidar import RPLidar
from rplidar import RPLidarException
from Phidget22.Devices.Stepper import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *

PORT_NAME = '/dev/ttyUSB0'

def StepperAttached(e):
    try:
        attached = e
        print("\nAttach Event Detected (Information Below)")
        print("===========================================")
        print("Library Version: %s" % attached.getLibraryVersion())
        print("Serial Number: %d" % attached.getDeviceSerialNumber())
        print("Channel: %d" % attached.getChannel())
        print("Channel Class: %s" % attached.getChannelClass())
        print("Channel Name: %s" % attached.getChannelName())
        print("Device ID: %d" % attached.getDeviceID())
        print("Device Version: %d" % attached.getDeviceVersion())
        print("Device Name: %s" % attached.getDeviceName())
        print("Device Class: %d" % attached.getDeviceClass())
        print("\n")

    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   
    
def StepperDetached(e):
    detached = e
    try:
        print("\nDetach event on Port %d Channel %d" % (detached.getHubPort(), detached.getChannel()))
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Press Enter to Exit...\n")
        readin = sys.stdin.read(1)
        exit(1)   

def ErrorEvent(e, eCode, description):
    print("Error %i : %s" % (eCode, description))

def PositionChangeHandler(e, position):
    print("Position: %f" % position)
    return position



def run(pwm):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    lidar.set_pwm(int(pwm))
    outfile = open(str(pwm) + '.txt', 'w')
    cnt = 0
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measurments():
            line = '\t'.join(str(v) for v in measurment)
            outfile.write(line +'\t' + str(ch.getPosition()) + '\n')
            cnt += 1
            if lidar.motor:
                ln = 'Spinning %d'
            else:
                ln = 'Stopped %d'
            print(ln % cnt)
            if cnt > 85000:
                break
    except KeyboardInterrupt:
        print('Stopping.')
    except RPLidarException as e:
        print(e)

    print("complete")
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    outfile.close()
    print(lidar.motor)


try:
    ch = Stepper()
except RuntimeError as e:
    print("Runtime Exception %s" % e.details)
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)
    
try:
    ch.setOnAttachHandler(StepperAttached)
    ch.setOnDetachHandler(StepperDetached)
    ch.setOnErrorHandler(ErrorEvent)

    ch.setOnPositionChangeHandler(PositionChangeHandler)

    # Please review the Phidget22 channel matching documentation for details on the device
    # and class architecture of Phidget22, and how channels are matched to device features.

    # Specifies the serial number of the device to attach to.
    # For VINT devices, this is the hub serial number.
    #
    # The default is any device.
    #
    # ch.setDeviceSerialNumber(<YOUR DEVICE SERIAL NUMBER>) 

    # For VINT devices, this specifies the port the VINT device must be plugged into.
    #
    # The default is any port.
    #
    # ch.setHubPort(0)

    # Specifies which channel to attach to.  It is important that the channel of
    # the device is the same class as the channel that is being opened.
    #
    # The default is any channel.
    #
    # ch.setChannel(0)

    # In order to attach to a network Phidget, the program must connect to a Phidget22 Network Server.
    # In a normal environment this can be done automatically by enabling server discovery, which
    # will cause the client to discovery and connect to available servers.
    #
    # To force the channel to only match a network Phidget, set remote to 1.
    #
    # Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICE);
    # ch.setIsRemote(1)

    print("Waiting for the Phidget Stepper Object to be attached...")
    ch.openWaitForAttachment(5000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1)

print("Engaging the motor\n")
ch.setEngaged(1)


'''for i in range(-10000, -500001, -10000) :'''
ch.setTargetPosition(-500000)
run(sys.argv[1])
time.sleep(60)

print("Setting Position to -500000 for 5 seconds...\n")
'''ch.setTargetPosition(500000)
run(sys.argv[1])
time.sleep(45)'''
'''run(sys.argv[1])'''

'''print("Setting Position to -15000 for 5 seconds...\n")
ch.setTargetPosition(-300000)
time.sleep(50)'''

print("Setting Position to 0 for 5 seconds...\n")
ch.setTargetPosition(0)
time.sleep(30)

try:
    ch.close()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Press Enter to Exit...\n")
    readin = sys.stdin.read(1)
    exit(1) 
print("Closed Stepper device")
exit(0)