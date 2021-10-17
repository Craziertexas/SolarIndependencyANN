from numpy import NaN
import pandas as pd
from tkinter.filedialog import askopenfile

class Formater:

    def __init__(self):
        print("Formating Household Energy Consumption")
        Data = self.OpenFile()
        print('Data:')
        print(Data)
        self.Format(Data)
    
    def OpenFile(self):
        file = askopenfile()
        data = pd.read_csv(file,sep=";")
        return data
    
    def Format(self, Data):
        Data = self.GroupByHours(Data)
        self.BackUp(Data)
        Data = self.GetDayOfYear(Data)
        self.BackUp(Data)
        Data = self.DeleteNanRows(Data)
        self.BackUp(Data)
        print(Data)
        
        
    def GroupByHours(self, Data):
        DF = pd.DataFrame(columns=['Year','Day','Time','ActivePower','ReactivePower','GlobalVoltage','GlobalCurrent','SubMetering1','SubMetering2','SubMetering3'])
        LastHourSW = True
        LastHour = 0
        index = 0

        for Time in Data['Time']:
            Hour = Time.split(':')[0]

            if LastHourSW:

                LastHour = Hour
                LastHourSW = False
                counter = 0

                ActivePower = 0
                ReactivePower = 0
                GlobalVoltage = 0
                GlobalCurrent = 0
                SubMetering1 = 0
                SubMetering2 = 0
                SubMetering3 = 0


            if (Hour == LastHour):
                try:
                    ActivePower = ActivePower + float(Data['Global_active_power'][index])
                    ReactivePower = ReactivePower + float(Data['Global_reactive_power'][index])
                    GlobalVoltage = GlobalVoltage + float(Data['Voltage'][index])
                    GlobalCurrent = GlobalCurrent + float(Data['Global_intensity'][index])
                    SubMetering1 = SubMetering1 + float(Data['Sub_metering_1'][index])
                    SubMetering2 = SubMetering2 + float(Data['Sub_metering_2'][index])
                    SubMetering3 = SubMetering3 + float(Data['Sub_metering_3'][index])
                    counter = counter + 1
                except:
                    None
            else:
                try:
                    ActivePower = ActivePower/counter
                    ReactivePower = ReactivePower/counter
                    GlobalVoltage = GlobalVoltage/counter
                    GlobalCurrent = GlobalCurrent/counter
                    SubMetering1 = SubMetering1/counter
                    SubMetering2 = SubMetering2/counter
                    SubMetering3 = SubMetering3/counter
                except:
                    ActivePower = NaN
                    ReactivePower = NaN
                    GlobalVoltage = NaN
                    GlobalCurrent = NaN
                    SubMetering1 = NaN
                    SubMetering2 = NaN
                    SubMetering3 = NaN
                Date = Data['Date'][index-1]
                DF = DF.append({'Day':Date,'Time':LastHour,'ActivePower':ActivePower,'ReactivePower':ReactivePower,'GlobalVoltage':GlobalVoltage,'GlobalCurrent':GlobalCurrent,'SubMetering1':SubMetering1,'SubMetering2':SubMetering2,'SubMetering3':SubMetering3}, ignore_index = True)
                LastHourSW = True

            print((index/2075259)*100)
            index = index + 1
        return DF
    
    def GetDayOfYear(self, Data):
        Data['Year'] = pd.to_datetime(Data['Day'],format = '%d/%m/%Y').dt.year
        Data['Day'] = pd.to_datetime(Data['Day'],format ='%d/%m/%Y').dt.dayofyear
        return Data 

    def DeleteNanRows(self, Data):
        Data = Data.dropna()
        return Data 

    def BackUp(self, Data):
        Data.to_csv('BackUp.csv',sep=";")

if __name__ == "__main__":
    Formater()