from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "v35"
    tasks = {
        # "algorithms" : ["pcal","mcuve","bsnet","v0","v1","v2","v3","v4"],
        # "datasets" : ["indian_pines","paviaU","salinas"],
        "algorithms": ["bsnet","v0","v2","v3","v4"],
        "datasets": ["indian_pines"],
        "target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,1,tag,skip_all_bands=False)
    summary, details = ev.evaluate()
