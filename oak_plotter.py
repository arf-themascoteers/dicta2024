import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

ALGS = {
    "v0": "BS-Net-Classifier [6]",
    "v4": "Proposed Algorithm",
    "all": "All Bands",
    "mcuve": "MCUVE [10]",
    "bsnet": "BS-Net-FC [5]",
    "pcal": "PCA-loading [11]",
    "v3": "Proposed Algorithm excluding FC",
    "v2": "Proposed Algorithm excluding FC, Sigmoid",
    "v1": "Proposed Algorithm excluding FC, Sigmoid, Full-batch"
}

DSS = {
    "indian_pines" : "Indian Pines",
    "paviaU" : "paviaU",
    "salinas" : "salinas",
}

COLORS = {
    "v0": "#1f77b4",
    "v4": "#ff7f0e",
    "all": "#2ca02c",
    "mcuve": "#d62728",
    "bsnet": "#9467bd",
    "pcal": "#8c564b",
    "v1": "#e377c2",
    "v2": "#bcbd22",
    "v3": "#17becf"
}


def sanitize_df(df):
    if "algorithm" not in df.columns:
        df['target_size'] = 0
        df['algorithm'] = 'all'
        df['time'] = 0
        df['selected_features'] = ''
    return df


def plot_oak(source, exclude=None, include=None, out_file="baseline.png"):
    if exclude is None:
        exclude = []
    os.makedirs("saved_figs", exist_ok=True)
    dest = os.path.join("saved_figs",out_file)
    if isinstance(source,str):
        df = sanitize_df(pd.read_csv(source))
    else:
        df = [sanitize_df(pd.read_csv(loc)) for loc in source]
        df = pd.concat(df, axis=0, ignore_index=True)

    df.to_csv(os.path.join("saved_figs","source.split.csv"), index=False)
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    markers = ['s', 'P', 'D', '^', 'o', '*', '.']
    labels = ["Overall Accuracy (OA)", "Average Accuracy (AA)", r"Cohen's kappa ($\kappa$)"]

    min_lim = min(df["oa"].min(),df["aa"].min(),df["k"].min())-0.1
    max_lim = max(df["oa"].max(),df["aa"].max(),df["k"].max())+0.1

    min_lim = 0.3
    max_lim = 1

    order = ["all","pcal","mcuve","bsnet","v0","v1","v2","v3","v4"]
    df["algorithm"] = pd.Categorical(df["algorithm"], categories=order, ordered=True)
    df = df.sort_values("algorithm")

    algorithms = df["algorithm"].unique()
    datasets = df["dataset"].unique()

    if include is None:
        include = algorithms

    include = [x for x in include if x not in exclude]

    fig, axes = plt.subplots(nrows=3, ncols=len(datasets), figsize=(15, 15))
    axes = np.reshape(axes, (3, -1))

    for metric_index,metric in enumerate(["oa", "aa", "k"]):
        for ds_index, dataset in enumerate(datasets):
            dataset_label = dataset
            if dataset in DSS:
                dataset_label = DSS[dataset]
            dataset_df = df[df["dataset"] == dataset].copy()
            algorithm_counter = 0
            for algorithm_index, algorithm in enumerate(include):
                algorithm_label = algorithm
                if algorithm in ALGS:
                    algorithm_label = ALGS[algorithm]
                alg_df = dataset_df[dataset_df["algorithm"] == algorithm]
                alg_df = alg_df.sort_values(by='target_size')
                linestyle = "-"
                if algorithm in COLORS:
                    color = COLORS[algorithm]
                else:
                    color = colors[algorithm_counter]

                marker = markers[algorithm_counter]
                if algorithm == "all":
                    oa = alg_df.iloc[0]["oa"]
                    aa = alg_df.iloc[0]["aa"]
                    k = alg_df.iloc[0]["k"]
                    alg_df = pd.DataFrame({'target_size': range(5, 31), 'oa': [oa] * 26, 'aa': [aa] * 26, 'k': [k] * 26})
                    linestyle = "--"
                    color = "#000000"
                    marker = None
                else:
                    algorithm_counter = algorithm_counter + 1

                axes[metric_index, ds_index].plot(alg_df['target_size'], alg_df[metric],
                        label=algorithm_label, marker=marker, color=color,
                        fillstyle='none', markersize=10, linewidth=2, linestyle=linestyle
                        )

            axes[metric_index, ds_index].set_xlabel('Target size', fontsize=18)
            axes[metric_index, ds_index].set_ylabel(labels[metric_index], fontsize=18)
            axes[metric_index, ds_index].set_ylim(min_lim, max_lim)
            axes[metric_index, ds_index].tick_params(axis='both', which='major', labelsize=14)
            if ds_index == len(datasets)-1 and metric_index == 0:
                legend = axes[metric_index, ds_index].legend(title="Algorithms", loc='upper left', fontsize=18,
                                                             bbox_to_anchor=(0, 1.6), ncols=3)
                legend.get_title().set_fontsize('18')
                legend.get_title().set_fontweight('bold')

            axes[metric_index, ds_index].grid(True, linestyle='--', alpha=0.6)
            if metric_index == 0:
                axes[metric_index, ds_index].set_title(f"{dataset_label}", fontsize=22, pad=20)

    plt.tight_layout()
    fig.subplots_adjust(wspace=0.4)
    plt.savefig(dest)
    plt.close(fig)



def plot_saved(exclude=None):
    files = []
    for d in os.listdir("saved_results"):
        dpath = os.path.join("saved_results",d)
        for f in os.listdir(dpath):
            if f.endswith("_summary.csv") and not f.startswith("all_"):
                fpath = os.path.join("saved_results",d,f)
                files.append(fpath)
    plot_oak(files, exclude)


def plot_baseline():
    plot_oak(["saved_results/all/all_summary.csv"],
         exclude=["v1""v2","v3"],
         out_file = "baseline.png"
    )

def plot_ablation():
    plot_oak(["saved_results/all/all_summary.csv"],
         include=["v0","v1"],
         out_file = "ablation_1.png"
    )

    plot_oak(["saved_results/all/all_summary.csv"],
         include=["v0","v1","v2"],
         out_file = "ablation_2.png"
    )

    plot_oak(["saved_results/all/all_summary.csv"],
         include=["v2","v3"],
         out_file = "ablation_3.png"
    )

    plot_oak(["saved_results/all/all_summary.csv"],
         include=["v3","v4"],
         out_file = "ablation_3.png"
    )



if __name__ == "__main__":
    plot_baseline()
    plot_ablation()


