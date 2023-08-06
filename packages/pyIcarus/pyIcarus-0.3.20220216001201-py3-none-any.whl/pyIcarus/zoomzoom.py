import threading
import time

from monty.inspect import caller_name

range_num = 100


def add_mult(x, y, z):
    time.sleep(0.01)
    return (z + y) * x


if __name__ == '__main__':
    r = range(range_num)
    pool_size = 20
    # pool = Pool(pool_size)
    # print(f"Running pool of {pool_size} processes")
    # partial_func = partial(add_mult, z=1, y=2)
    # start = time.time()
    # result = pool.map(partial_func, r, chunksize=10)
    # print(f"It took {time.time() - start} seconds")
    # pool.close()
    # pool.join()


async def async_add_mult(x, y, z):
    time.sleep(0.01)
    return (z + y) * x


if __name__ == '__main__':
    r = range(range_num)
    start = time.time()
    # for i in r:
    #     asyncio.run(async_add_mult(x=i, y=2, z=1))
    # print(f'finished in {time.time() - start} seconds')

if __name__ == '__main__':
    r = range(range_num)
    start = time.time()
    # partial_func = partial(add_mult, z=1, y=2)
    # imap_tqdm(20, partial_func, r)


def run_in_another_thread(func):
    def call_threaded(*args, **kwargs):
        t = threading.Thread(target=func, args=args, kwargs=kwargs, name=f'Thread-{caller_name()}')
        t.start()
        return t

    return call_threaded


@run_in_another_thread
def long_duration_function(*args, **kwargs):
    print(f"{threading.current_thread().name = !s}")
    for i in range(10):
        print(f'{i=}')
        time.sleep(1)


if __name__ == '__main__':
    t = long_duration_function('I am a function arg', test='I am a function kwarg')
    f = long_duration_function('testing')
    print(f"{threading.current_thread().name = !s}")
