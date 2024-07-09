from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "iv3"
    tasks = {
        "algorithms" : ["v3"],
        "datasets": ["indian_pines"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=False, test=True)
    summary, details = ev.evaluate()
