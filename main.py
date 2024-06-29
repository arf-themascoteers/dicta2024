from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "ps"
    tasks = {
        "algorithms" : [],
        "datasets" : ["paviaU","salinas"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,10,tag,skip_all_bands=False)
    summary, details = ev.evaluate()
