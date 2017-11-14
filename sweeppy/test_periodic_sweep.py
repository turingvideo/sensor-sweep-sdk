import os
import sys
import time
from sweeppy import Sweep
import pylab
pylab.ion()

def write_scan_to_file(f, ts, samples):
    for sample in samples:
        f.write('{},{},{},{}\n'.format(ts, sample.angle/1000., sample.distance, sample.signal_strength))
        ts = -1

device_name = '/dev/ttyUSB0'

output_folder = 'scan_samples'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with Sweep(device_name) as sweep:

    sweep.set_motor_speed(0)
    print('Reset sweep motor to stop')
    time.sleep(2)
    period = 30
    cooldown_period = 10

    scan_logs = []

    while True:
        start_time = time.time()
        print('Start scanning: {}'.format(start_time))
        sweep.set_motor_speed(5)
        print('sweep set speed = 5')

        sweep.start_scanning()
        print('sweep started')

        ready_time = time.time()
        print('Device ready: {}, elapsed {}s'.format(ready_time, ready_time - start_time))

        output_file = os.path.join(output_folder, 'scan_{:d}.csv'.format(int(start_time*1000)))
        with open(output_file, 'w') as f:
            f.write("TIMESTAMP,AZIMUTH,DISTANCE,SIGNAL_STRENGTH\n")
            i = 0
            while True:
                for scan in sweep.get_scans():
                    ts = int(time.time() * 1000)
                    print('{} i = {} read {} scan samples'.format(ts, i, len(scan.samples)))
                    scan_logs.append((ts, len(scan.samples)))
                    write_scan_to_file(f, ts, scan.samples)
                    break
                if time.time() - ready_time > period:
                    break
                i += 1

        stop_time = time.time()
        sweep.stop_scanning()
        print('sweep stoped')
        sweep.set_motor_speed(1)
        print('sweep set speed = 1')
        print('Stop scanning: {}, elapsed {}s'.format(stop_time, stop_time - ready_time))

        pylab.plot([s[0] for s in scan_logs], [s[1] for s in scan_logs])
        pylab.show(block=False)
        pylab.pause(0.01)
        # import pdb; pdb.set_trace()

        time.sleep(cooldown_period)
        cooldown_time = time.time()
        print('finish cool down: {}, elapsed {}s'.format(cooldown_time, cooldown_time - stop_time))


