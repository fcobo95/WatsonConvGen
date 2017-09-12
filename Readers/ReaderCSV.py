import pandas


class reader:
    def __init__(self):
        with open('../Data Files/data.csv') as CSVData:
            self.theFinalCSVData = pandas.read_csv(CSVData, delimiter=',')
