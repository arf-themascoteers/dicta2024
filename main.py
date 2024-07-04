from task_runner import TaskRunner

if __name__ == '__main__':
    tag = "hello"
    tasks = {
        #"algorithms" : ["pcal","mcuve","bsnet","v0","v1","v2","v3","v4"],
        "algorithms" : ["bsnet","v0","v1","v2","v3","v4"],
        # "datasets" : ["indian_pines","paviaU","salinas"],
        "datasets": ["indian_pines"],
        "target_sizes" : [30, 29, 28]
        #"target_sizes" : list(range(30,4,-1))
    }
    ev = TaskRunner(tasks,tag,skip_all_bands=True, verbose=True)
    summary, details = ev.evaluate()
