from algorithm import Algorithm
from auswahl import MCUVE
from data_splits import DataSplits
import numpy as np


class Algorithm_mcuve(Algorithm):
    def __init__(self, target_size:int, dataset, tag, reporter, verbose, fold):
        super().__init__(target_size, dataset, tag, reporter, verbose, fold)


    def get_selected_indices(self):
        selector = MCUVE(n_features_to_select=self.target_size)
        selector.fit(self.splits.train_x, self.splits.train_y)
        support = selector.get_support(indices=True)
        self.set_all_indices(support)
        self.set_selected_indices(support)
        self.set_weights(np.zeros(self.splits.train_x.shape[1]))
        return selector, support

    def is_cacheable(self):
        return False