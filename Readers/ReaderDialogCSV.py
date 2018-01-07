import pandas


class DialogReader:
    """
    :returns: a reader
    """

    def __init__(self):
        with open('dialog.csv') as DialogData:
            self.theFinalCSVData = pandas.read_csv(DialogData, delimiter=',', skipinitialspace=True)
