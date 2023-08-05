from configobj import ConfigObj

class Ini:
    @staticmethod
    def Write(section:str,word:str,writeValue,pathDefault:str="./config.ini"):
        iniobj = ConfigObj(pathDefault,encoding="UTF8",list_values=False)
        if section in iniobj.sections:
            pass
        else:
            iniobj[section]={}
        iniobj[section][word]=writeValue
        iniobj.write()
    @staticmethod
    def Read(section:str,word:str,DefaultValue="",pathDefault="./config.ini"):
        iniobj = ConfigObj(pathDefault,encoding="UTF8",list_values=False)
        if section in iniobj.sections:
            if word in iniobj[section]:
                if "_bool" in word:
                    print("{},{},{}".format(section,word,iniobj[section][word]))
                    return bool(iniobj[section][word])
                if "_int" in word:
                    return int(iniobj[section][word])
                if "_float" in word:
                    return float(iniobj[section][word])
                return iniobj[section][word]
            else:
                iniobj[section][word]=DefaultValue
                iniobj.write()
                return DefaultValue
        else:
            iniobj[section]={}
            iniobj[section][word]=DefaultValue
            iniobj.write()
            return DefaultValue
if __name__=="__main__":
    # path = ["cnblogs","com","hardfood"]
    # Ini.Write(path[0],path[1],path[2])
    # print("{}.{}/{}".format(path[0],path[1],Ini.Read(path[0],path[1])))
    data= Ini.Read("Instr","B{}-BW".format(1),"10")
    print(data)
    print(int(data[1]))