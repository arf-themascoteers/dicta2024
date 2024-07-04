class DataSplits:
    def __init__(self, name, bs_train_x, bs_train_y, train_x, train_y, test_x, test_y):
        self.name = name
        self.bs_train_x = bs_train_x
        self.bs_train_y = bs_train_y
        self.train_x = train_x
        self.train_y = train_y
        self.test_x = test_x
        self.test_y = test_y

    def get_name(self):
        return self.name

    def splits_description(self, short=True):
        desc = f"train={len(self.train_y)}; test={len(self.test_y)};\n"
        if not short:
            desc = f"{desc}bs_train_x={self.bs_train_x[0:3,0]}; bs_train_y={self.bs_train_y[0:3]};\n"
            desc = f"{desc}train_x={self.train_x[0:3,0]}; train_y={self.train_y[0:3]};\n"
            desc = f"{desc}test_x={self.test_x[0:3,0]}; test_y={self.test_y[0:3]};\n"
        return desc