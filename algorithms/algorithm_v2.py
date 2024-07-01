from algorithm import Algorithm
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import numpy as np
import math
from data_splits import DataSplits
import train_test_evaluator


class Sparse(nn.Module):
    def __init__(self):
        super().__init__()
        self.k = 0.1

    def forward(self, X):
        X = torch.where(X < self.k, 0, X)
        return X


class ZhangNet(nn.Module):
    def __init__(self, bands, number_of_classes, last_layer_input):
        super().__init__()
        
        self.bands = bands
        self.number_of_classes = number_of_classes
        self.last_layer_input = last_layer_input
        self.weighter = nn.Sequential(
            nn.Linear(self.bands, 512),
            nn.ReLU(),
            nn.Linear(512, self.bands),
            nn.Sigmoid()
        )
        self.classnet = nn.Sequential(
            nn.Conv1d(1,16,kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(16),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=0),
            nn.Conv1d(16, 8, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(8),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=0),
            nn.Conv1d(8, 4, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(4),
            nn.MaxPool1d(kernel_size=2, stride=2, padding=0),
            nn.Flatten(start_dim=1),
            nn.Linear(last_layer_input,self.number_of_classes)
        )
        self.sparse = Sparse()
        num_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print("Number of learnable parameters:", num_params)

    def forward(self, X):
        channel_weights = self.weighter(X)
        channel_weights = torch.mean(channel_weights, dim=0)
        sparse_weights = self.sparse(channel_weights)
        reweight_out = X * sparse_weights
        reweight_out = reweight_out.reshape(reweight_out.shape[0],1,reweight_out.shape[1])
        output = self.classnet(reweight_out)
        return channel_weights, sparse_weights, output


class Algorithm_v2(Algorithm):
    def __init__(self, target_size:int, splits:DataSplits, tag, reporter, verbose, fold):
        super().__init__(target_size, splits, tag, reporter, verbose, fold)
        self.criterion = torch.nn.CrossEntropyLoss()
        self.class_size = len(np.unique(self.splits.train_y))
        self.last_layer_input = 100
        self.zhangnet = ZhangNet(self.splits.train_x.shape[1], self.class_size, self.last_layer_input).to(self.device)
        self.total_epoch = 500
        self.epoch = -1
        self.X_train = torch.tensor(self.splits.train_x, dtype=torch.float32).to(self.device)
        self.y_train = torch.tensor(self.splits.train_y, dtype=torch.int32).to(self.device)
        self.X_val = torch.tensor(self.splits.validation_x, dtype=torch.float32).to(self.device)
        self.y_val = torch.tensor(self.splits.validation_y, dtype=torch.int32).to(self.device)

    def get_selected_indices(self):
        optimizer = torch.optim.Adam(self.zhangnet.parameters(), lr=0.001, betas=(0.9,0.999))
        dataset = TensorDataset(self.X_train, self.y_train)
        dataloader = DataLoader(dataset, batch_size=128000, shuffle=True)
        channel_weights = None
        loss = 0
        l1_loss = 0
        mse_loss = 0

        for epoch in range(self.total_epoch):
            self.epoch = epoch
            for batch_idx, (X, y) in enumerate(dataloader):
                optimizer.zero_grad()
                channel_weights, sparse_weights, y_hat = self.zhangnet(X)
                deciding_weights = channel_weights
                mean_weight, all_bands, selected_bands = self.get_indices(deciding_weights)
                self.set_all_indices(all_bands)
                self.set_selected_indices(selected_bands)
                self.set_weights(mean_weight)

                y = y.type(torch.LongTensor).to(self.device)
                mse_loss = self.criterion(y_hat, y)
                l1_loss = self.l1_loss(channel_weights)
                lambda_value = self.get_lambda(epoch+1)
                loss = mse_loss + lambda_value*l1_loss
                if batch_idx == 0 and self.epoch%10 == 0:
                    self.report_stats(channel_weights, sparse_weights, epoch, mse_loss, l1_loss.item(), lambda_value,0, 0,loss)
                loss.backward()
                optimizer.step()

        print(self.get_name(),"selected bands and weights:")
        print("".join([str(i).ljust(10) for i in self.selected_indices]))
        return self.zhangnet, self.selected_indices

    def report_stats(self, channel_weights, sparse_weights, epoch, mse_loss, l1_loss, lambda1, l2_loss, lambda2, loss):
        # _, _,y_hat = self.zhangnet(self.X_train)
        # yp = torch.argmax(y_hat, dim=1)
        # yt = self.y_train.cpu().detach().numpy()
        # yh = yp.cpu().detach().numpy()
        # t_oa, t_aa, t_k = train_test_evaluator.calculate_metrics(yt, yh)
        t_oa, t_aa, t_k = 0,0,0

        # _, _,y_hat = self.zhangnet(self.X_val)
        # yp = torch.argmax(y_hat, dim=1)
        # yt = self.y_val.cpu().detach().numpy()
        # yh = yp.cpu().detach().numpy()
        # v_oa, v_aa, v_k = train_test_evaluator.calculate_metrics(yt, yh)
        v_oa, v_aa, v_k = 0,0,0

        mean_weight = channel_weights
        means_sparse = sparse_weights

        if len(mean_weight.shape) > 1:
            mean_weight = torch.mean(mean_weight, dim=0)
            means_sparse = torch.mean(means_sparse, dim=0)


        min_cw = torch.min(mean_weight).item()
        min_s = torch.min(means_sparse).item()
        max_cw = torch.max(mean_weight).item()
        max_s = torch.max(means_sparse).item()
        avg_cw = torch.mean(mean_weight).item()
        avg_s = torch.mean(means_sparse).item()

        l0_cw = torch.norm(mean_weight, p=0).item()
        l0_s = torch.norm(means_sparse, p=0).item()

        mean_weight, all_bands, selected_bands = self.get_indices(channel_weights)

        oa, aa, k = train_test_evaluator.evaluate_split(self.splits, self)
        self.reporter.report_epoch(epoch, mse_loss, l1_loss, lambda1, l2_loss,lambda2,loss,
                                   t_oa, t_aa, t_k,
                                   v_oa, v_aa, v_k,
                                   oa, aa, k,
                                   min_cw, max_cw, avg_cw,
                                   min_s, max_s, avg_s,
                                   l0_cw, l0_s,
                                   selected_bands, means_sparse)

    def get_indices(self, deciding_weights):
        mean_weights = deciding_weights
        if len(mean_weights.shape) > 1:
            mean_weights = torch.mean(mean_weights, dim=0)

        corrected_weights = mean_weights
        if torch.any(corrected_weights < 0):
            corrected_weights = torch.abs(corrected_weights)

        band_indx = (torch.argsort(corrected_weights, descending=True)).tolist()
        return mean_weights, band_indx, band_indx[: self.target_size]

    def l1_loss(self, channel_weights):
        channel_weights = torch.abs(channel_weights)
        return torch.mean(channel_weights)

    def get_lambda(self, epoch):
        return 0.0001 * math.exp(-epoch/self.total_epoch)



