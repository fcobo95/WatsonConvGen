import pandas


class CSVReader:
    """
    :returns: a reader
    """

    def __init__(self):
        with open('data.csv') as CSVData:
            self.theFinalCSVData = pandas.read_csv(CSVData, delimiter=',', skipinitialspace=True)
