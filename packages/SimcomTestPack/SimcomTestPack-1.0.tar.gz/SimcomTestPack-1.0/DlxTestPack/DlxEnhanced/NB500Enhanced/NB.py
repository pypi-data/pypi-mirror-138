import time
from ..CMW500 import NB
class NB1(NB):
    def __init__(self):
        super().__init__()
    def NB1_NPDCCH_conf(self):
        print("配置NB1的NPDCCH")
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:NPDCch:MXNRep 8")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:NPDCch:NREP RMAX8")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:NPDCch:STSF 2")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:NPDCch:OFFSt 2")
        if count==4:
            return True
        else:
            return False
    def NB_RATE_CONF_15k_s_d(self):
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:CELL:SCSPacing S15K")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UDPattern DL") #DL|UL|DLUL
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:DL KEEP, KEEP, MI12, NSF03, NR1")
        if count==3:
            return True
        else:
            return False
    def NB_RATE_CONF_15k_12_u(self):
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:CELL:SCSPacing S15K")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UDPattern UL") #DL|UL|DLUL
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UL SC12, 0, MI12, NRU04, NR1")
        if count==3:
            return True
        else:
            return False
    def NB_RATE_CONF_15k_s_u(self):
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:CELL:SCSPacing S15K")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UDPattern UL") #DL|UL|DLUL
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UL SC1, 0, MI10, NRU06, NR1")
        if count==3:
            return True
        else:
            return False
    def NB_RATE_CONF_3k75_s_u(self):
        count = 0
        count+=self._send("CONFigure:NIOT:SIGN:CELL:SCSPacing S3K75")
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UDPattern UL") #DL|UL|DLUL
        count+=self._send("CONFigure:NIOT:SIGN:CONNection:UDEFined:UL SC1, 0, MI10, NRU06, NR1")
        if count==3:
            return True
        else:
            return False
    def NB_BAND_set(self,band_num:str):
        return self._send("CONFigure:NIOT:SIGN:BAND OB{}".format(band_num))
    def NB_POWER_set(self,value:float):
        return self._send("CONFigure:NIOT:SIGN:DL:NRSepre:LEVel {}".format())
    
    def NB_RATE_UL_get(self):
        '''
        返回两个参数的列表
        第一个参数为真则获得有效数据
        第二个参数为float (Kbit)速率
        '''
        self._send("INITiate:NIOT:SIGN:BLER")#
        state = 1
        while state:
            state =not self._query("FETCh:NIOT:SIGN:BLER:STATe?","RDY")
            time.sleep(1)
        result_data:str = self._query("FETCh:NIOT:SIGN:BLER:UL:ABSolute?")
        deal_data_list = result_data.split(",")
        if int(deal_data_list[1])>=1000:
            return [True,float(deal_data_list[3])/1000]
        else:
            return [False,0]
    def NB_RATE_DL_get(self):
        '''
        返回两个参数的列表
        第一个参数为真则获得有效数据
        第二个参数为float (Kbit)速率
        '''
        self._send("INITiate:NIOT:SIGN:BLER")#
        state = 1
        while state:
            state =not self._query("FETCh:NIOT:SIGN:BLER:STATe?","RDY")
            time.sleep(1)
        result_data:str = self._query("FETCh:NIOT:SIGN:BLER:ABSolute?")
        deal_data_list = result_data.split(",")
        if int(deal_data_list[3])>=1000:
            return [True,float(deal_data_list[4])/1000]
        else:
            return [False,0]

class NB2(NB):
    def __init__(self):
        super().__init__()