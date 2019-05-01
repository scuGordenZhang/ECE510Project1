##########################################################
# PSU ECE510 Post-silicon Validation Project 1
# --------------------------------------------------------
# Filename: tap.py
# --------------------------------------------------------
# Purpose: TAP Controller Class
##########################################################

from tap.common.tap_gpio import *
from tap.log.logging_setup import *
import time


class Tap(Tap_GPIO):
    """ Class for JTAG TAP Controller"""

    def __init__(self, log_level=logging.INFO):
        """ initialize TAP """
        self.logger = get_logger(__file__, log_level)
        self.max_length = 1000

        # set up the RPi TAP pins
        Tap_GPIO.__init__(self)

    def toggle_tck(self, tms, tdi):  # use set_io_data method to toggle
        """ toggle TCK for state transition 

        :param tms: data for TMS pin
        :type tms: int (0/1)
        :param tdi: data for TDI pin
        :type tdi: int (0/1)

        """

        Tap_GPIO.set_io_data(self, tms, tdi, 0)
        Tap_GPIO.set_io_data(self, tms, tdi, 1)

        pass

    def reset(self):
        """ set TAP state to Test_Logic_Reset """
        # assert TMS for 5 TCKs in a row
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)

        pass

    def reset2ShiftIR(self):
        """ shift TAP state from reset to shiftIR """  # write state transition from Test-Logic_Reset to Shift-IR

        self.toggle_tck(0, x)
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(0, x)
        self.toggle_tck(0, x)

        pass

    def exit1IR2ShiftDR(self):
        """ shift TAP state from exit1IR to shiftDR """

        self.toggle_tck(1, x)
        self.toggle_tck(0, x)
        self.toggle_tck(1, x)
        self.toggle_tck(0, x)
        self.toggle_tck(0, x)

        pass

    def exit1DR2ShiftIR(self):
        """ shift TAP state from exit1DR to shiftIR """

        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(1, x)
        self.toggle_tck(0, x)
        self.toggle_tck(0, x)

        pass

    def shiftInData(self, tdi_str):  # when you are in SHIFT-IR or Shift-DR state you can call below methods
        """ shift in IR/DR data                             # when you are done here, you should leave IR state

        :param tdi_str: TDI data to shift in
        :type tdo_str: str

        """

        bits = str(tdi_str[::-1])  # reverse the bit order

        for bit in bits[:-1]:  # shift in all bits
            self.toggle_tck(0, bit)   # issue TMS 0 to stay in the SHIFT-IR or SHIFT-DR state
        self.toggle_tck(1, bits[-1])  # issue TMS 1 to go Update-IR and send the last bit

        pass

    def shiftOutData(self, length):  # in this case the length is 31
        """ get IR/DR data

        :param length: chain length        
        :type length: int
        :returns: int - TDO data

        """

        strBits = []
        count = 0

        while (count < length):

            self.toggle_tck(0, x)   # Issue TMS 0 to stay in Shift-IR or Shift-DR state
            bit = Tap_GPIO.read_tdo_data()
            strBits = [bit] + strBits  # append newly read bit from TDO in FRONT
            count += 1

        # return 0
        return strBits

    def getChainLength(self):  # dont worry about this one
        """ get chain length

        :returns: int -- chain length	

        """

        return 0
