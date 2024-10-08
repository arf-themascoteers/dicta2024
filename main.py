from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "iv00"
    tasks = {
        "algorithms" : ["v0"],
        "datasets": ["indian_pines"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False)
    summary, details = ev.evaluate()
