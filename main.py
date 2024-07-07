from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "dummy"
    tasks = {
        "algorithms" : ["v0","v2"],
        "datasets": ["indian_pines"],
        "target_sizes" : [5]
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False)
    summary, details = ev.evaluate()
