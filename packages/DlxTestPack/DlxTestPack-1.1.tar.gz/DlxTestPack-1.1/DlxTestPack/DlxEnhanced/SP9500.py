import time
from ..DlxTestClassV5 import scpi_communication_pack
Nr_FDD = [1,3,5,7,8,12,20,28]
Nr_FreM = {1:1980,2:1910,3:1785,5:849,7:2570,8:915,12:716,20:862,25:1915,26:849,28:748,30:2315,
            34:2025,38:2620,39:1920,40:2400,41:2690,66:1780,71:698,77:4200,78:3800,79:4999}
class scpi_SP9500_test_cmd(scpi_communication_pack):
    def __init__(self):
        pass
    def Band_set(self,band_num:str):
        self._send("CONFigure:CELL1:NR:SIGN:COMMon:FBANd:INDCator {}".format(band_num))
        self._send("CONFigure:CELL1:NR:SIGN:COMMon:FBANd:INDCator:UL {}".format(band_num))
        self._send("CONFigure:CELL1:NR:SIGN:COMMon:FBANd:INDCator:DL {}".format(band_num))
    def BandWidth_set(self,band_width:int):
        self._send("CONFigure:CELL1:NR:SIGN:BWidth BW{}".format(band_width))
    def Channel_set(self,channel:str='High'):
        '''
        参数 str : High Mid Low
        '''
        self._send("CONFigure:CELL1:NR:CONFig:RANGe {}".format(channel))
    def Query_Connected(self,time_s:int=120):
        return self._query_while_key_time("CONFigure:CELL:NR:SIGN:STATe?","CellConnected",time_s)
        
    def Query_Power(self):
        # data = self._query("FETCh:SENSe:NR:ABSolute:PTOLerance?")
        data = self._query("FETCh:SENSe:NR:MEValuation:TXP:AVG?")
        return data
    def IFConnected(self,time_s:int=120):
        '''
        连接上return [True,data]
        '''
        time_start = InThreadTime.GetTimefloat()
        while InThreadTime.GetTimefloat()-time_start<time_s:
            rt_data:str = self.Query_Power()
            data = rt_data.split(",")[-1]
            if float(data)>10:
                return data
            time.sleep(0.5)
        raise Exception("连接已断开",data)
    def MesureInit(self):
        # self._send("CONFigure:NR:ULMimo:MEValuation:RESult ON,OFF,OFF,OFF,OFF")
        # self._send("CONFigure:NR:ULMimo:MEValuation:RESult:TXP ON")
        # self._send("ABORt:NR:MEValuation")
        self._send("CONFigure:NR:MEValuation:TOUT 10")
        self._send("CONFigure:NR:MEValuation:REPetition CONTinuous")
        self._send("INITiate:NR:MEValuation")
        time.sleep(1)
        # self._send("CONFigure:CELL1:NR:SIGN:SLOT8:UL:CTYPe NSCH")
        # self._send("CONFigure:CELL1:NR:SIGN:SLOT:APPLy")
        # self._send("CONFigure:NR:MEValuation:RESult ON,OFF,OFF,OFF,OFF")

        # self._send("CONFigure:CELL1:NR:SIGN:RLEVel 30")
        # self._send("CONFigure:CELL1:NR:SIGN:SLOT:TPC 3,255")
    def MesureInitV2(self,bandNum:int=1):
        '''
        1 or '1'
        '''
        if int(bandNum) in Nr_FDD:
            for idx in range(10):
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:DL:CTYPe NSCH".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:CTYPe NSCH".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:CTYPe PUSCh".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:NUMBer 1".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:SYMBol 0,14".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:MCS1 0".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:RB 1,1".format(idx))
            self._send("CONFigure:CELL1:NR:SIGN:SLOT:APPLy")
            self._send("CONFigure:CELL1:NR:SIGN:SLOT:TPC 3,255")
            self._send("CONFigure:CELL1:NR:SIGN:RLEVel 30.00")
            
            self._send("CONFigure:NR:MEValuation:RESult ON,OFF,OFF,OFF,OFF")
            self._send("CONFigure:NR:MEValuation:REPetition CONTinuous")
            self._send("INITiate:NR:MEValuation")
        else:
            for idx in range(20):
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:DL:CTYPe NSCH".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:CTYPe NSCH".format(idx))
            for idx in [8,9,18,19]:
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:CTYPe PUSCh".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:NUMBer 1".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:SYMBol 0,14".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:MCS1 0".format(idx))
                self._send("CONFigure:CELL1:NR:SIGN:SLOT{}:UL:RB 1,1".format(idx))
            self._send("CONFigure:CELL1:NR:SIGN:SLOT:APPLy")
            self._send("CONFigure:CELL1:NR:SIGN:SLOT:TPC 3,255")
            self._send("CONFigure:CELL1:NR:SIGN:RLEVel 30.00")

            self._send("CONFigure:NR:MEValuation:RESult ON,OFF,OFF,OFF,OFF")
            self._send("CONFigure:NR:MEValuation:REPetition CONTinuous")
            self._send('INITiate:NR:MEValuation')
    def OnOffSignal(self,Key:bool=True):
        '''
        ON|OFF
        '''
        if Key:
            self._send("CALL:CELL1 ON")
            self._query_while_key_time("QUERy:CELL1:NR:SIGN:ON:ERRor?","No_err",20)
        else:
            self._send("CALL:CELL1 OFF")
            time.sleep(8)
    def RegistState(self):
        return self._query_while_key_time("CONFigure:CELL1:NR:SIGN:STATe?","CellConnected")
    # def Query_power(self):
    #     return self._query("CONFigure:CELL1:NR:SIGN:POWer?")
    def PuschRB(self,RbStart:int=1,RbCnt:int=1):
        self._send("CONFigure:CELL1:NR:SIGN:SLOT8:UL:RB {},{}".format(RbStart,RbCnt))
    def GetChannel(self):
        # return self._query("CONFigure:CELL1:NR:SIGN:AFPA:CHANnel:UL?")
        return self._query("CONFigure:CELL1:NR:SIGN:COMMon:FBANd:UL:CARCentre:ARFCn?")
        
    def SetLoss(self,loss_f:float=0.5):
        self._send("CONFigure:BASE:FDCorrection:CTABle:CREate TLoss,100000000,{},6000000000,{}".format(loss_f,loss_f))
        self._send("CONFigure:BASE:FDCorrection:SAVE")
        self._send("CONFigure:FDCorrection:ACTivate TLoss,0,IO,RXTX")
        self._send("CONFigure:FDCorrection:ACTivate TLoss,0,OUT,TX")
    def SetSubcarrierSpacing(self,bandNum:int=1):
        '''
        FDD 15,TDD 30
        '''
        if bandNum in Nr_FDD:
            scs =15
        else:
            scs =30
        self._send("CONFigure:CELL1:NR:SIGN:COMMon:FBANd:DL:SCSList:SCSPacing kHz{}".format(scs))
