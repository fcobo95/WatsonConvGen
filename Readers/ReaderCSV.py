import pandas


class Reader:
    """
    :returns: a reader
    """

    def __init__(self):
        with open('../Data Files/data.csv') as CSVData:
            self.theFinalCSVData = pandas.read_csv(CSVData, delimiter=',', skipinitialspace=True)
