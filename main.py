from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "zhangANDv1"
    tasks = {
        "algorithms" : ["zhang","v1"],
        "datasets" : ["indian_pines"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,2,tag,skip_all_bands=True)
    summary, details = ev.evaluate()
