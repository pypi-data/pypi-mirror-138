import pyvisa
import serial
import time
import subprocess
import json
# import sys
# sys.path.append("D:\pppython\python")
# from All_pack import DlxTestClassV3


class InThreadTime(): 
    @staticmethod
    def GetTimeStr():
        '''
        返回日期字符串 如211103_161722
        '''
        return time.strftime("%y%m%d_%H%M%S", time.localtime())
    @staticmethod
    def GetTimefloat():
        '''
        返回当前时间(s)
        '''
        return time.time()
    @staticmethod
    def FloatTimeToStr(time_sum:float):
        return time.strftime("%M-%S",time.localtime(time_sum))
    @staticmethod
    def Sleep(time_s:float,key:list=[False]):
        '''
        key为真退出
        返回True 为失败退出
        
        '''
        for idx in range(0,int(time_s)):
            time.sleep(1)
            if(key[0]):
                return True
            print("[InThreadTime-Sleep]:{}".format(idx))
        time.sleep(time_s-int(time_s))
        return False
    @staticmethod
    def cmd_deal_real_time_show(cmd:str,logprint=print):
        '''
        Log打印回调接口 参数str，命令执行成功返回0，执行失败返回1
        '''
        xe = subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
        while True:
            rt_data = xe.stdout.readline().decode("GBK")
            if rt_data!="":
                if logprint==print:
                    logprint(rt_data,end="")

                else:
                    logprint(rt_data)
            else:
                break
        return xe.wait()#执行成功返回0，执行失败返回1
    @staticmethod
    def cmd_deal_not_real_time_show(cmd:str):
        '''
        返回(0,str)执行成功，返回(1,str)执行失败
        '''
        xe = subprocess.run(cmd,stdout=subprocess.PIPE)
        return (xe.returncode,xe.stdout.decode("gbk"))
    @staticmethod
    def iperf3_json_get_bandwitdh(data:str):
        data_obj = json.loads(data)
        return data_obj["end"]["sum_received"]["bits_per_second"]
#-----------------------------------------------------
class scpi_communication_pack:
    """
    SCPI 的通信包
    需先进行连接才能进行后续的数据通信操作
    """
    def _connect(self,scpi_addr:str):
        """
        VISA 字符串格式:
        GPIB0::{}::INSTR
        TCPIP0::{}::inst0::INSTR
        """
        self.visoure = pyvisa.ResourceManager()
        self.__inst = self.visoure.open_resource(scpi_addr)
        self.__inst.timeout = 20000  
       
    def _send(self,send_data:str,confir_key:bool=True):

        if confir_key:
            self.__inst.write(send_data)
            x = self.__inst.query('*OPC?')
            print(x)
            if '1' in x:
                return True
            return False
        else:
            self.__inst.write(send_data)
            return True

    def _query(self,send_data:str,confirm_answer:str=''):
        '''
        返回data或者返回[bool,data]
        '''
        if confirm_answer=='':
            data = self.__inst.query(send_data)
            print(data)
            return data
        else:
            data = self.__inst.query(send_data)
            print(data)
            if confirm_answer in data:
                return [True,data]
            else:
                return [False,data]
    def _query_while_key_time(self,cmd:str,confirm_key:str,time_s:int=40):
        '''
        命令|确认结果|时间
        '''
        start_time = InThreadTime.GetTimefloat()
        while InThreadTime.GetTimefloat()-start_time<time_s:
            get_data = self._query(cmd)
            if confirm_key in get_data:
                return get_data
            time.sleep(2)
        raise Exception("超时",time_s,get_data)
    def _close(self):
        try:
            self.__inst.close()
        except:
            pass

class at_communication_pack():
    """
    AT 通信包
    需先进行连接才能进行后续的数据通信操作
    """
    def _connect(self,com_num:str,bps:int=115200,time=0.1):
        '''
        输入参数(3,[115200,[0.1]])
        '''
        self.c_at = serial.Serial("COM{}".format(com_num))
        self.c_at.baudrate=bps
        self.c_at.timeout=time

    def _send(self,data:str):
        '''
        返回发送字节数
        '''
        count=self.c_at.write("{}\r".format(data).encode("gbk"))
        return count
    def _send_and_recv_confirm_single_key(self,at_send:str,at_recv:str):
        '''
        返回[bool,data]
        '''
        self.c_at.write("{}\r".format(at_send).encode("gbk"))
        get_data = self.c_at.readall()#.decode("gbk")
        # print(str(get_data))
        if at_recv.encode("GBK") in get_data:
            return [True,get_data]
        else:
            return [False,get_data]
    def _send_and_recv_confirm_single_key_split_while(self,at_send:str,at_recv:str,time_s:int=10):
        '''
        返回 data
        '''
        start_time = InThreadTime.GetTimefloat()
        while InThreadTime.GetTimefloat()-start_time<time_s:
            self.c_at.write("{}\r".format(at_send).encode("gbk"))
            get_data = self.c_at.readall().decode("gbk")
            print(str(get_data))
            if at_recv in get_data.split(","):
                return get_data
            time.sleep(1)
        raise Exception("超时",time_s)
    def _send_and_recv_confirm_single_key_while(self,at_send:str,at_recv:str,time_s:int=10):
        '''
        返回 data
        '''
        start_time = InThreadTime.GetTimefloat()
        while InThreadTime.GetTimefloat()-start_time<time_s:
            self.c_at.write("{}\r".format(at_send).encode("gbk"))
            get_data = self.c_at.readall().decode("gbk")
            print(str(get_data))
            if at_recv in get_data:
                return get_data
            time.sleep(1)
        raise Exception("超时",time_s,get_data)
    def _send_and_recv_confirm_multiple_key(self,at_send:str,at_key_list:list):
        '''
        输入(at_command,at_key_list)
        '''
        send_num=self.c_at.write("{}\r".format(at_send).encode("gbk"))
        print("send_num{}".format(send_num))
        get_data = self.c_at.readall()#.decode("gbk")
        # print(str(get_data))
        for idx in at_key_list:
            if idx.encode("GBK") in get_data:
                pass
            else:
                return False
        return True
    def _readall(self):
        try:   
            data = self.c_at.readall()
            if data!=b'':
                return [True,data.decode()]
            elif data!="":
                return [True,data]
            else:
                return [False,"NONE"]
        except:
            return [False,"ERROR"]

    def _readline(self):
        try:
            data = self.c_at.readline()
            if data!=b'':
                return [True,data.decode()]
            else:
                return [False,"NONE"]
        except:
            return [False,"ERROR"]

                
    def _close(self):
        try:
            self.c_at.close()
        except:
            pass

    
if __name__=="__main__":
    # comK = [3,5,8]
    # vss = [at_communication_pack() for idx in range(len(comK))]
    # [vss[idx]._connect(str(idx)) for idx in range(len(comK))]
    # vss[0]._send("AT")
    # vss = at_communication_pack()
    # vss._connect(3)
    # vss._send_and_recv_confirm_single_key("AT+SIMCOMATI","OK")
    # vss._send_and_recv_confirm_multiple_key("AT+SIMCOMATI",["A011B02A7670M6","OK"])
    # InThreadTime.Sleep(10)
    xe = scpi_cmw500_test_cmd()
    # xe._connect("GPIB0::20::INSTR")
    # xe.Mes2GInit()
    # xe.Mes2GOn()
    # print(xe.TxPower2GGet())
    # xe = scpi_SP9500_test_cmd()
    xe._connect("TCPIP0::192.168.1.9::inst0::INSTR")
    # xe.Init_Instr()
    # xe.HandOver_regist_Init_Catm()
    # xe.Instr_SIGN_ON()
    xe.HandOver_to_other_Band_Catm("2")
    time.sleep(2)
    xe.HandOver_Init_Catm()
    data=xe.HandOver_QueryTxPowerAVERage()
    print(data)

    # xe._connect("TCPIP0::192.168.1.80::inst0::INSTR")
    # xe.MesureInitV2()
    # print(xe.Query_Power())
    # print(xe.GetChannel())
    # print(xe._query_while_key_time("CONFigure:CELL1:NR:SIGN:STATe?","CellConnected"))
    # print(xe.Query_Power())
    # print(xe.IFConnected())
    # xe = scpi_66391D_test_cmd()
    # xe._connect("GPIB0::12::INSTR")
    # xe.PowerOnOff(2,False)
    # xe.SetVolt(2,0)
    # time.sleep(1)
    # xe.SetVolt(2,3.8)
    # xe.PowerOnOff(2,True)
