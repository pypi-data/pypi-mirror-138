from ..DlxTestClassV5 import scpi_communication_pack
POWER_66391D = {"100.us/div":"SENS:SWE:TINT 1.56E-005;POIN 38;OFFS:POIN 0",
                "200.us/div":"SENS:SWE:TINT 1.56E-005;POIN 76;OFFS:POIN 0",
                "500.us/div":"SENS:SWE:TINT 1.56E-005;POIN 192;OFFS:POIN 0",
                "1.ms/div":"SENS:SWE:TINT 1.56E-005;POIN 384;OFFS:POIN 0",
                "2.ms/div":"SENS:SWE:TINT 1.56E-005;POIN 769;OFFS:POIN 0",
                "5.ms/div":"SENS:SWE:TINT 1.56E-005;POIN 1923;OFFS:POIN 0",
                "10.ms/div":"SENS:SWE:TINT 1.56E-005;POIN 3846;OFFS:POIN 0",
                "20.ms/div":"SENS:SWE:TINT 3.12E-005;POIN 3846;OFFS:POIN 0",
                "50.ms/div":"SENS:SWE:TINT 7.8E-005;POIN 3846;OFFS:POIN 0",
                "100.ms/div":"SENS:SWE:TINT 0.000156;POIN 3846;OFFS:POIN 0",
                "200.ms/div":"SENS:SWE:TINT 0.0002964;POIN 4048;OFFS:POIN 0",
                "500.ms/div":"SENS:SWE:TINT 0.0007332;POIN 4091;OFFS:POIN 0",
                "1.s/div":"SENS:SWE:TINT 0.0014664;POIN 4091;OFFS:POIN 0",
                "2.s/div":"SENS:SWE:TINT 0.0029328;POIN 4091;OFFS:POIN 0",
                "4.s/div":"SENS:SWE:TINT 0.0058656;POIN 4091;OFFS:POIN 0"
                }
class scpi_66391D_test_cmd(scpi_communication_pack):
    def __init__(self):
        pass
    def ReadESRstate(self):
        while True:
            if self._query("*ESR?","+0"):
                break
    def Query_data(self,Accur:str):
        '''
        获取电流 {'CurrentDc':0,'CurrentMax':0,'CurrentHigh':0,'CurrentLow':0}
        '''
        return_data = {'CurrentDc':0,'CurrentMax':0,'CurrentHigh':0,'CurrentLow':0}
        self._send(POWER_66391D[Accur])
        self.ReadESRstate()
        self._query("MEAS:ARR:CURR?")
        self.ReadESRstate()
        return_data["CurrentDc"]=self._query("FETC:CURR?")
        self.ReadESRstate()
        return_data["CurrentHigh"]=self._query("FETC:CURR:HIGH?")
        self.ReadESRstate()
        return_data["CurrentMax"]=self._query("FETC:CURR:MAX?")
        self.ReadESRstate()
        return_data["CurrentLow"]=self._query("FETC:CURR:LOW?")
        
        return return_data
    def SetVolt(self,Channel:int=1,Volt:float=0):
        '''
        Channel 1|2
        '''
        # self._send("SOUR{}:VOLT {}".format(Channel,"1.000"))
        self._send("SOUR:VOLT{} {}".format(Channel,Volt))
    def PowerOnOff(self,Channel:int=1,OnOff:bool=True):
        '''
        Channel 1|2 
        '''
        if OnOff:
            self._send("OUTP{} ON".format(Channel))
        else:
            self._send("OUTP{} OFF".format(Channel))
