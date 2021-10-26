import pandas as pd
from tkinter.filedialog import askopenfile
import matplotlib.pyplot as plt
import seaborn as sns
import neurolab as nl

class ANN:

    def __init__(self):
        data = self.OpenFile()
        data_2 = self.DropData(data, ['Year', 'ReactivePower', 'GlobalVoltage', 'GlobalCurrent'])
        self.ScatterPlot(data_2)
        self.BoxPlot(data_2)
        self.Correlations(data_2)
        net = self.TrainNeuralNetwork(data_2)
        self.EvaluateNet(data)
  
    def OpenFile(self):
        file = askopenfile()
        data = pd.read_csv(file,sep=";")
        return data

    def DropData(self, data, columns):
        data = data.drop(columns, axis = 1)
        return data

    def ScatterPlot(self, data):
        for column in data.head():
            if column != 'Day' and column != 'Time':
                ax = sns.scatterplot(data = data, x = 'Time', y = column)
                plt.show()

    def BoxPlot(self, data):
        for column in data.head():
            if column != 'Day' and column != 'Time':
                ax = sns.boxplot(data = data, x = 'Time', y = column)
                plt.show()

    def Correlations(self, data):
        corr = data.corr()
        ax = sns.heatmap(corr, annot = True)
        plt.show()
    
    def TrainNeuralNetwork(self, data):
        net = nl.net.newff([[0,365],[0,23]],[30,1])

        inputs = [[0,0] for size in range(data['Time'].size)]
        index = 0
        for input in inputs:
            input[0] = data['Day'][index]
            input[1] = data['Time'][index]
            index = index + 1

        targets = [[0] for size in range(data['Time'].size)]
        index = 0
        for target in targets:
            target[0] = data['ActivePower'][index]
            index = index + 1
        
        error = net.train(inputs, targets, epochs = 30)
        net.save("Net")
        plt.plot(error)
        plt.show()

        return net
    
    def EvaluateNet(self, data):
        net = nl.load("Net")
        print(data.head())

        Year = input("Input the target Year: ")
        Day = input("Input the target Day: ")
        
        data = data.loc[(data['Year'] == int(Year))&(data['Day'] == int(Day))]
        print(data)

        inputs = [[0,0] for size in range(data['Time'].size)]
        index = data.index[0]
        for inpu in inputs:
            inpu[0] = data['Day'][index]
            inpu[1] = data['Time'][index]
            index = index + 1

        targets = [[0] for size in range(data['Time'].size)]
        index = data.index[0]
        for target in targets:
            target[0] = data['ActivePower'][index]
            index = index + 1
        
        predictions = net.sim(inputs)
        print(predictions.reshape(len(predictions)))

        inputs = [item[1] for item in inputs]
        targets = [item[0] for item in targets]

        plt.plot(inputs,targets,predictions)
        plt.show()

        
        
        
        


if __name__ == "__main__":
    ANN()        