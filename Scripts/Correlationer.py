from os import name
import numpy
from scipy.stats import pearsonr
from tkinter.filedialog import askopenfile, askdirectory

class Correlationer:

    def __init__(self):
        print('Starting correlationer')
        data, names = self.OpenFile()
        print('Names Loaded')
        print(names)
        print('Data Loaded')
        print(data)
        data, names = self.FeaturesRemover(data, names)
        print('Names Filtered')
        print(names)
        print('Data Filtered')
        print(data)
        correlations, target = self.Correlation(data, names)
        print('Correlations')
        print(correlations)
        dataFiltered, namesFiltered, correlationsFiltered = self.FeaturesFilter(data, target, names, correlations)
        print('Summary: ')
        print('-----------------------------------')
        print('Features')
        print(namesFiltered)
        print('Correlations')
        print(correlationsFiltered)
        print('------------------------------------')

    def OpenFile(self):
        file = askopenfile()
        delimit = input('Define the csv delimiter: ')
        data = numpy.genfromtxt(file, delimiter = delimit, dtype = str)
        names = data[0,:]
        data = numpy.delete(data, 0, axis = 0)
        data = numpy.asarray(data, dtype= numpy.float64)
        return data, names

    def FeaturesRemover(self, data, names):
        sw = bool(input('Do you want to exclude some columns? '))
        while sw:
            print(names)
            column = int(input('Input the column index: '))
            sw_input = bool(input('Do you want to exclude ' + names[column]))
            if sw_input:
                data = numpy.delete(data, column, axis=1)
                names = numpy.delete(names, column)
            sw = bool(input('Continue? '))
        return data, names
    
    def Correlation(self, data, names):
        print(names)
        sw = False
        while not sw:
            target = int(input('Input the index of the target variable: '))
            sw = bool(input('Selected Value: ' + names[target]))
        correlations = numpy.zeros(numpy.size(data,1) - 1)
        z = 0
        for i in range(0,numpy.size(data,1)):
            if i!=target:
                correlations[z] = pearsonr(data[:,i],data[:,target])[0]
                z = z + 1
        correlations = abs(correlations)
        return correlations, target
    
    def FeaturesFilter(self, data, target, names, correlations):
        number = int(input('Input the number of features to take into account: '))
        indexes = correlations.argsort()[::-1][:number]
        correlationsFiltered = numpy.zeros(number)
        dataFiltered = numpy.zeros([numpy.size(data,0),number + 1])
        namesFiltered = numpy.empty(number + 1, dtype= numpy.dtype('U100'))
        z = 0
        for index in indexes:
            dataFiltered[:,z] = data[:,index]
            namesFiltered[z] = names[index]
            correlationsFiltered[z] = correlations[index]
            z = z + 1
        dataFiltered[:, z] = data[:, target]
        namesFiltered[z] = names[target]
        return dataFiltered,namesFiltered,correlationsFiltered
    
    def ExportData(self, data, names):
        path = askdirectory()
        name = input("Input the name of the file: ")
        pathData = path + "/" + name + ".csv"
        pathNames = path + "/" + name + "_names.csv"
        numpy.savetxt(pathData, data, delimiter = ";")
        numpy.savetxt(pathNames, names, delimiter = ";", fmt = "%s")

if __name__ == '__main__':
    Correlationer()