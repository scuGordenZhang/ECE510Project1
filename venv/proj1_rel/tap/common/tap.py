##########################################################
# PSU ECE510 Post-silicon Validation Project 1
# --------------------------------------------------------
# Filename: tap.py
# --------------------------------------------------------
# Purpose: TAP Controller Class
# Github:  https://github.com/tarcheen/ECE510Project1.git
##########################################################

from tap.common.tap_gpio import *
from tap.log.logging_setup import *
import time

class Tap(Tap_GPIO):
    """ Class for JTAG TAP Controller"""

    def __init__(self,log_level=logging.INFO):
        """ initialize TAP """
        self.logger = get_logger(__file__,log_level)
        self.max_length = 1000

        #set up the RPi TAP pins
        Tap_GPIO.__init__(self)

    def toggle_tck(self, tms, tdi):
        """ toggle TCK for state transition 

        :param tms: data for TMS pin
        :type tms: int (0/1)
        :param tdi: data for TDI pin
        :type tdi: int (0/1)

        """
        #make clock one
        #initially it is 0
        #as it is rising edge
        Tap_GPIO.set_io_data(self,tms,tdi,1)
        Tap_GPIO.delay(0.1)
        #make it zero again
        Tap_GPIO.set_io_data(self,tms,tdi,0)
        Tap_GPIO.delay(0.1)
        pass
       
    def reset(self):
        """ set TAP state to Test_Logic_Reset """
        # assert TMS for 5 TCKs in a row
        self.toggle_tck(1,0)
        self.toggle_tck(1,0)
        self.toggle_tck(1,0)
        self.toggle_tck(1,0)
        self.toggle_tck(1,0)
        pass

    def reset2ShiftIR(self):
        """ shift TAP state from reset to shiftIR """
        #from the state machine
        #reset to run test/idle
        self.toggle_tck(0,0)
        #select DR
        self.toggle_tck(1,0)
        #select IR
        self.toggle_tck(1,0)
        #capture IR
        self.toggle_tck(0,0)
        #shift IR
        self.toggle_tck(0,0)
        pass 

    def exit1IR2ShiftDR(self):
        """ shift TAP state from exit1IR to shiftDR """
        #update IR
        self.toggle_tck(1,0)
		#select DR
        self.toggle_tck(1,0)
		#capture DR
        self.toggle_tck(0,0)
		#shift DR
        self.toggle_tck(0,0)
        pass

    def exit1DR2ShiftIR(self):
        """ shift TAP state from exit1DR to shiftIR """
        #update DR
        self.toggle_tck(1,0)
        #select DR
        self.toggle_tck(1,0)
        #select IR
        self.toggle_tck(1,0)
        #capture IR
        self.toggle_tck(0,0)
        #shift IR
        self.toggle_tck(0,0)
        pass

    def shiftInData(self, tdi_str):    
        """ shift in IR/DR data

        :param tdi_str: TDI data to shift in
        :type tdo_str: str

        """
		#here we should break the string and send 1 bit at a time ex. 001001
		#but LSB first so user will pass 100100
		#so send the string character 1 by 1 till last TMS should be 0
        for i in range(len(tdi_str)-1):
            self.toggle_tck(0,int(tdi_str[i]))
		#for last bit TMS should be 1
        if(len(tdi_str) != 0):
            self.toggle_tck(1,int(tdi_str[-1]))
        pass

    def shiftOutData(self, length):
        """ get IR/DR data

        :param length: chain length        
        :type length: int
        :returns: int - TDO data

        """
        ret = []
		#first bit will be here
		#just read it
        ret.append(Tap_GPIO.read_tdo_data(self))
        for i in range(length-1):
            #give clock
            self.toggle_tck(0,0)
            #read the bit
            ret.append(Tap_GPIO.read_tdo_data(self))
        print(ret)
        reVal = 0
        for i in range(len(ret)):
            #print(len(ret)-i-1)
            reVal |=(ret[len(ret)-i-1] << (len(ret)-i-1))
        #retVal = 0
        return reVal

    def getChainLength(self):
        """ get chain length

        :returns: int -- chain length	

        """

        return 0
