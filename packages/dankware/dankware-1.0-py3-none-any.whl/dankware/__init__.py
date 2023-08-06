from concurrent.futures import ThreadPoolExecutor, as_completed
from alive_progress import alive_bar

def multithread(function, list, threads, progress_bar):

    futures = []
    executor = ThreadPoolExecutor(max_workers=threads)
    for item in list:futures.append(executor.submit(function, item))
    
    if progress_bar:
        with alive_bar(int(len(futures))) as bar:
            for future in as_completed(futures):
                try:future.result();bar()
                except:bar()
    else:
        for future in as_completed(futures):
            try:future.result()
            except:pass