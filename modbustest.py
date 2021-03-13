import minimalmodbus

slaveaddr = 1
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddr, debug=False, mode=minimalmodbus.MODE_RTU)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1.50          # seconds

## Read registers
try:
    voltage = instrument.read_float(0, functioncode=4)  # Registernumber, number of decimals
    current = instrument.read_float(6, functioncode=4)
    power = instrument.read_float(12, functioncode=4)
    apparentpower = instrument.read_float(18, functioncode=4)
    reactivepower = instrument.read_float(24, functioncode=4)
    print("Voltage:          {:0.4f} V".format(voltage))
    print("Current:          {:0.4f} A".format(current))
    print("Power:            {:0.4f} W".format(power))
    print("Apparent power:   {:0.4f} VA".format(apparentpower))
    print("Reactive power:   {:0.4f} VAr".format(reactivepower))
except IOError:
    print("Failed to read from instrument")