from PCF8574 import PCF8574

bus = 6
chip_addr = 0x20

def main():
    pcf = PCF8574(bus, chip_addr)

    if not pcf.begin():
        print("No communication is established. Exiting...")
        return

    pcf.pinMode('P0', 'INPUT')
    pcf.pinMode('P1', 'OUTPUT')

    # read input
    val = pcf.digitalRead('P0')
    print('P0: ', val)

    # read output
    val = pcf.digitalRead('P1')
    print('P1: ', val)

    # write output
    pcf.digitalWrite('P1', 1)

    # verify
    val = pcf.digitalRead('P1')
    print('P1: ', val)


if __name__ == '__main__':
    main()