from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "v3"
    tasks = {
        "algorithms" : ["v3"],
        "datasets": ["salinas"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False, test=True)
    summary, details = ev.evaluate()
