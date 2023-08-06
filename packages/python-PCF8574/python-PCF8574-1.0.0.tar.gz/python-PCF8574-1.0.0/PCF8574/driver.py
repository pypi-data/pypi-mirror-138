from smbus2 import SMBus

def begin(smBus, address, value):
    with SMBus(smBus) as bus:
        bus.write_byte(address, value)
    with SMBus(smBus) as bus:
        response = bus.read_byte(address)
    if response == value:
        return True
    return False

def pin_mode(pinName, mode, pinModeFlag):
    pinNumber = __pinNameToNumber(pinName)
    if mode == 'INPUT':
        pinModeFlag |= (1<<pinNumber)
    elif mode == 'OUTPUT':
        pinModeFlag &= ~(1<<pinNumber)
    else:
        raise ValueError("Invalid mode %s" % mode)
    return pinModeFlag

def digital_read(pinName, smBus, address):
    pinNumber = __pinNameToNumber(pinName)
    with SMBus(smBus) as bus:
        response = bus.read_byte(address)
    return __isNthBitSet(pinNumber, response)

def digital_write(pinName, value, smBus, address, pinModeFlag):
    pinNumber = __pinNameToNumber(pinName)
    # if requested pin is output
    if not __isNthBitSet(pinNumber, pinModeFlag):
        with SMBus(smBus) as bus:
            response = bus.read_byte(address)
        if value:
            response |= (1<<pinNumber) 
        else:
            response &= ~(1<<pinNumber)
        with SMBus(smBus) as bus:
            bus.write_byte(address, response)
    else:
        raise Exception("Can't write to input pin %s" % pinName)


def __pinNameToNumber(pinName):
    if not isinstance(pinName, str):
        raise TypeError("pinName should be str")

    if len(pinName) == 2 and pinName[0] == 'P':
        pinNumber = int(pinName[1])
        if pinNumber in range(8):
            return pinNumber
        else:
            raise IndexError("Out of index pin %s" % pinName)
    else:
        raise ValueError("Invalid pin name. Didn't you mean 'P0, P1, ... , P7'? ")

def __isNthBitSet(bit, data):
    if data & (1<<bit):
        return True
    return False