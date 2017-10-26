from sweeppy import Sweep

device_name = '/dev/ttyUSB0'

print('with scoping')

with Sweep(device_name) as sweep:
    sweep.start_scanning()

    i = 0
    for scan in sweep.get_scans():
        print('i={} {}\n'.format(i, scan))
        i += 1
        if i >= 3:
            break


print('no scoping')

sweep = Sweep(device_name)

sweep.open()
sweep.start_scanning()

i = 0
for scan in sweep.get_scans():
    print('i={} {}\n'.format(i, scan))
    i += 1
    if i >= 3:
        break

sweep.close()

