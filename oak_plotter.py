import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

ALGS = {
    "zhang" : "BS-Net-Classifier",
    "lw_relu" : "Proposed Algorithm"
}

DSS = {
    "indian_pines" : "Indian Pines"
}


def plot_oak(source, exclude=None):
    if exclude is None:
        exclude = []
    os.makedirs("saved_figs", exist_ok=True)
    dest = os.path.join("saved_figs","out.png")
    if isinstance(source,str):
        df = pd.read_csv(source)
    else:
        df = [pd.read_csv(loc) for loc in source]
        df = pd.concat(df, axis=0, ignore_index=True)

    df.to_csv(os.path.join("saved_figs","source.split.csv"), index=False)
    colors = ['#909c86', '#e389b9', '#269658', '#5c1ad6', '#f20a21', '#000000']
    markers = ['s', 'P', 'D', '^', 'o', '*', '.']
    labels = ["Overall Accuracy (OA)", "Average Accuracy (AA)", "Cohen's kappa ($\kappa$)"]

    min_lim = min(df["oa"].min(),df["aa"].min(),df["k"].min())-0.1
    max_lim = max(df["oa"].max(),df["aa"].max(),df["k"].max())+0.1

    algorithms = df["algorithm"].unique()
    datasets = df["dataset"].unique()

    fig, axes = plt.subplots(nrows=3, ncols=len(datasets), figsize=(15, 15))
    axes = np.reshape(axes, (3, -1))

    for metric_index,metric in enumerate(["oa", "aa", "k"]):
        for ds_index, dataset in enumerate(datasets):
            dataset_label = dataset
            if dataset in DSS:
                dataset_label = DSS[dataset]
            dataset_df = df[df["dataset"] == dataset].copy()
            algorithm_counter = 0
            for algorithm_index, algorithm in enumerate(algorithms):
                if algorithm in exclude:
                    continue
                algorithm_counter = algorithm_counter + 1
                algorithm_label = algorithm
                if algorithm in ALGS:
                    algorithm_label = ALGS[algorithm]
                alg_df = dataset_df[dataset_df["algorithm"] == algorithm]
                alg_df = alg_df.sort_values(by='target_size')
                axes[metric_index, ds_index].plot(alg_df['target_size'], alg_df[metric],
                        label=algorithm_label, marker=markers[algorithm_counter], color=colors[algorithm_counter],
                        fillstyle='none', markersize=10, linewidth=2
                        )

            axes[metric_index, ds_index].set_xlabel('Target size', fontsize=18)
            axes[metric_index, ds_index].set_ylabel(labels[metric_index], fontsize=18)
            axes[metric_index, ds_index].set_ylim(min_lim, max_lim)
            axes[metric_index, ds_index].tick_params(axis='both', which='major', labelsize=14)
            if ds_index == len(datasets)-1 and metric_index == 0:
                legend = axes[metric_index, ds_index].legend(title="Algorithms", loc='upper left', fontsize=18,
                                                             bbox_to_anchor=(0, 1.6), ncols=2)
                legend.get_title().set_fontsize('18')
                legend.get_title().set_fontweight('bold')

            axes[metric_index, ds_index].grid(True, linestyle='--', alpha=0.6)
            if metric_index == 0:
                axes[metric_index, ds_index].set_title(f"{dataset_label}", fontsize=22, pad=20)

    plt.tight_layout()
    fig.subplots_adjust(wspace=0.5)
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


if __name__ == "__main__":
    #plot_saved()
    plot_oak([
        "results/v0_summary.csv",
        "results/v9_summary.csv"
    ])


