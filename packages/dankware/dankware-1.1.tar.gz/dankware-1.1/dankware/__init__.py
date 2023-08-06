from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar

def multithread(function, list_one: list = [], list_two: list = [], threads: int = 1, progress_bar: bool = True):

    futures = []
    executor = ThreadPoolExecutor(max_workers=threads)
    
    if len(list_one) == 0:
        for i in range(threads):futures.append(executor.submit(function))
    
    elif len(list_two) == 0:
        for item in list_one:futures.append(executor.submit(function, item))
        
    elif len(list_one) == len(list_two):
        for index in range(len(list_one)):futures.append(executor.submit(function, list_one[index], list_two[index]))
        
    else:
        print("\n  > MULTITHREAD ERROR! list_one and list_two do not have the same length!")
        return
    
    if progress_bar:
        with alive_bar(int(len(futures))) as bar:
            for future in as_completed(futures):
                try:future.result();bar()
                except:bar()
    else:
        for future in as_completed(futures):
            try:future.result()
            except:pass