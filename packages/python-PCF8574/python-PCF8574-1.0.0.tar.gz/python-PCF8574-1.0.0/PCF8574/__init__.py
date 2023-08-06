from PCF8574 import driver

class PCF8574:
    def __init__(self, busNum=None, slaveAddress=None) -> None:
        """
        The constructor for PCF8574 class.

        Args:
            busNum (integer , optional): SMBus/I2C bus number. Defaults to bus 0.
            slaveAddress (integer, optional): Slave address of SMBus/I2C device. \
                Defaults to address 0x20.
                    
        """
        if busNum is None:
            self.busNum = 0
        else:
            self.busNum = busNum
        if slaveAddress is None:
            self.slaveAddress = 0x20
        else:
            self.slaveAddress = slaveAddress
        self.__pinModeFlag = 0x00
        self.__isReady = False

    def begin(self, initialValue=None):
        """
        Intiates communication with slave.

        Args:
            initialValue (integer, optional): 8-bit integer. For each pin, configure bits <P7-P0>, \
                Set 0b1 for input and 0b0 for output. Defaults to power-on value 0xff i.e., all pins \
                as input.                

        Returns:
            bool: True on successful read/write operation. Otherwise false.
        """
        if initialValue is None:
            value = 0xff
        else:
            value = initialValue
        if driver.begin(self.busNum, self.slaveAddress, value):
            self.__isReady = True
        else:
            self.__isReady = False    
        return self.__isReady
    
    def pinMode(self, pinName, mode):
        """
        Sets pin as input or output. 

        Args:
            pinName (string): P0, P1, P2, P3, P4, P5, P6, P7
            mode (string): INPUT or OUTPUT

        Returns:
            integer: represents input/output configuration of pins

        Remarks:
            Since, no data direction register(DDR) available in PCF8574, this is \
            handled through software so that you don't set/reset any input pins. \
            Input pins become read-only.
        """
        self.__pinModeFlag = driver.pin_mode(pinName, mode, self.__pinModeFlag)
        return self.__pinModeFlag

    def digitalRead(self, pinName):
        """
        Reads value of a pin.

        Args:
            pinName (string): P0, P1, P2, P3, P4, P5, P6, P7

        Raises:
            Exception: if initialsation method <begin> fails or not called.

        Returns:
            bool: True if pin is set. Otherwise false.
        """
        if self.__isReady:
            return driver.digital_read(pinName, self.busNum, self.slaveAddress)
        else:
            raise Exception("Driver failed/ or not initialised")

    def digitalWrite(self, pinName, value):
        """
        Writes value to a pin.

        Args:
            pinName (string): P0, P1, P2, P3, P4, P5, P6, P7
            value (bool): True to set.

        Raises:
            Exception: if initialsation method <begin> fails or not called.

        Remarks:
            Applicable only to output pins.
        """
        if self.__isReady:
            driver.digital_write(pinName, value, self.busNum, self.slaveAddress, self.__pinModeFlag)
        else:
            raise Exception("Driver failed/ or not initialised")