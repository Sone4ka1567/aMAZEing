import settings as const

class Map:
    def __init__(self, file):  # подгружать карту будем из текстового файла
        self.data = []
        with open(file, 'rt') as f:
            for line in f:
                self.data.append(line.strip())  # срезать перенос строки!

        self.cell_width = len(self.data[0])
        self.cell_height = len(self.data)
        self.width = self.cell_width * const.CELL_SIZE
        self.height = self.cell_height * const.CELL_SIZE



