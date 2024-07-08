from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "1ps"
    tasks = {
        "algorithms" : ["v1"],
        "datasets": ["indian_pines","paviaU","salinas"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()
