from rplidar import RPLidar
rp = RPLidar('/dev/ttyUSB0')
rp.stop()
rp.stop_motor()
rp.disconnect()
del rp
