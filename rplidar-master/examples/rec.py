#!/usr/bin/env python3
'''Records measurments to a given file. Usage example:

$ ./record_measurments.py out.txt'''
import sys
from rplidar import RPLidar
from rplidar import RPLidarException



PORT_NAME = '/dev/ttyUSB0'


def run(pwm):
    '''Main function'''
    lidar = RPLidar(PORT_NAME)
    lidar.set_pwm(int(pwm))
    outfile = open(pwm + '.txt', 'w')
    cnt = 0
    try:
        print('Recording measurments... Press Crl+C to stop.')
        for measurment in lidar.iter_measurments():
            line = '\t'.join(str(v) for v in measurment)
            outfile.write(line + '\n')
            cnt += 1
            if lidar.motor:
                ln = 'Spinning %d'
            else:
                ln = 'Stopped %d'
            print(ln % cnt)
            if cnt > 10000:
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

if __name__ == '__main__':
    run(sys.argv[1])
