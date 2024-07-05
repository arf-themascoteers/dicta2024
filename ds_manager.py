import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale


class DSManager:
    def __init__(self, name, remove_bg=False):
        self.name = name
        dataset_path = f"data/{name}.csv"
        df = pd.read_csv(dataset_path)
        df.iloc[:, :-1] = minmax_scale(df.iloc[:, :-1])
        self.data = df.to_numpy()
        print(f"{self.name}: Total samples", len(self.data))
        self.foreground_data = self.data[self.data[:, -1] != 0]
        if remove_bg:
            self.foreground_data[:, -1] = self.foreground_data[:, -1] - 1
            self.data = self.foreground_data
        self.bs_train = self.data
        print(f"{self.name}: After background processing, Total samples", len(self.data))

    def get_name(self):
        return self.name

    def get_train_data(self):
        return self.bs_train

    def get_train_x_y(self):
        return self.get_train_x(), self.get_train_y()

    def get_train_x(self):
        return self.bs_train[:,0:-1]

    def get_train_y(self):
        return self.bs_train[:, -1]

    def get_foreground_data(self):
        return self.foreground_data

    def get_k_folds(self):
        for i in range(1):
            seed = 40 + i
            yield self.get_a_fold(seed)

    def get_a_fold(self, seed=50):
        return train_test_split(self.foreground_data[:,0:-1], self.foreground_data[:,-1], test_size=0.95, random_state=seed,
                         stratify=self.foreground_data[:, -1])

    def __repr__(self):
        return self.get_name()

    @staticmethod
    def get_dataset_names():
        return [
            "indian_pines",
            "paviaU",
            "salinas"
        ]

