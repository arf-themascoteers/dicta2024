from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "v5"
    tasks = {
        "algorithms" : ["v5"],
        "datasets" : ["indian_pines"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,10,tag,skip_all_bands=True)
    summary, details = ev.evaluate()
