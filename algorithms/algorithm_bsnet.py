from algorithm import Algorithm
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from data_splits import DataSplits
import train_test_evaluator


class BSNetFC(nn.Module):
    def __init__(self, bands):
        super().__init__()
        torch.manual_seed(3)
        self.bands = bands
        self.weighter = nn.Sequential(
            nn.BatchNorm1d(self.bands),
            nn.Linear(self.bands, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU()
        )
        self.channel_weight_layer = nn.Sequential(
            nn.Linear(128, self.bands),
            nn.Sigmoid()
        )
        self.encoder = nn.Sequential(
            nn.Linear(self.bands, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Linear(256, self.bands),
            nn.BatchNorm1d(self.bands),
            nn.Sigmoid()
        )

        num_params = sum(p.numel() for p in self.parameters() if p.requires_grad)
        print("Number of learnable parameters:", num_params)

    def forward(self, X):
        channel_weights = self.weighter(X)
        channel_weights = self.channel_weight_layer(channel_weights)
        reweight_out = X * channel_weights
        output = self.encoder(reweight_out)
        return channel_weights, output


class Algorithm_bsnet(Algorithm):
    def __init__(self, target_size:int, splits:DataSplits, tag, reporter, verbose, fold):
        super().__init__(target_size, splits, tag, reporter, verbose, fold)
        self.criterion = torch.nn.MSELoss(reduction='sum')
        self.epoch = -1
        self.bsnet = BSNetFC(self.splits.train_x.shape[1]).to(self.device)
        self.X_train = torch.tensor(self.splits.train_x, dtype=torch.float32).to(self.device)
        self.y_train = torch.tensor(self.splits.train_x, dtype=torch.int32).to(self.device)
        self.X_val = torch.tensor(self.splits.validation_x, dtype=torch.float32).to(self.device)
        self.y_val = torch.tensor(self.splits.validation_x, dtype=torch.int32).to(self.device)

    def get_selected_indices(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        optimizer = torch.optim.Adam(self.bsnet.parameters(), lr=0.00002)
        X_train = torch.tensor(self.splits.train_x, dtype=torch.float32).to(device)
        dataset = TensorDataset(X_train, X_train)
        dataloader = DataLoader(dataset, batch_size=64, shuffle=True)
        channel_weights = None
        loss = 0
        l1_loss = 0
        mse_loss = 0
        for epoch in range(100):
            self.epoch = epoch
            for batch_idx, (X, y) in enumerate(dataloader):
                if X.shape[0] == 1:
                    continue
                optimizer.zero_grad()
                channel_weights, y_hat = self.bsnet(X)
                deciding_weights = channel_weights
                mean_weight, all_bands, selected_bands = self.get_indices(deciding_weights)
                self.set_all_indices(all_bands)
                self.set_selected_indices(selected_bands)
                self.set_weights(mean_weight)

                mse_loss = self.criterion(y_hat, y)
                norms_for_all_batches = torch.norm(channel_weights, p=1, dim=1)
                l1_loss = torch.mean(norms_for_all_batches)
                loss = mse_loss + l1_loss * 0.01
                if batch_idx == 0 and self.epoch%10 == 0:
                    self.report_stats(channel_weights, channel_weights, epoch, mse_loss, l1_loss.item(), 0.01,0, 0,loss)
                loss.backward()
                optimizer.step()
            print(f"Epoch={epoch} MSE={round(mse_loss.item(), 5)}, L1={round(l1_loss.item(), 5)}, LOSS={round(loss.item(), 5)}")

        print(self.get_name(),"selected bands and weights:")
        print("".join([str(i).ljust(10) for i in self.selected_indices]))
        return self.bsnet, self.selected_indices

    def report_stats(self, channel_weights, sparse_weights, epoch, mse_loss, l1_loss, lambda1, l2_loss, lambda2, loss):
        cw,y_hat = self.bsnet(self.X_train)
        yp = torch.argmax(y_hat, dim=1)
        yt = self.y_train.cpu().detach().numpy()
        yh = yp.cpu().detach().numpy()
        t_oa, t_aa, t_k = 0,0,0#train_test_evaluator.calculate_metrics(yt, yh)

        cw,y_hat = self.bsnet(self.X_val)
        yp = torch.argmax(y_hat, dim=1)
        yt = self.y_val.cpu().detach().numpy()
        yh = yp.cpu().detach().numpy()
        v_oa, v_aa, v_k = 0,0,0#train_test_evaluator.calculate_metrics(yt, yh)

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