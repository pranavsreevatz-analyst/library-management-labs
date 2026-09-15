import asyncio
import time
from concurrent.futures import ThreadPoolExecutor


def waiting_task(number):
    # Simulates a task waiting for a network response.
    time.sleep(1)
    return number


async def async_waiting_task(number):
    await asyncio.sleep(1)
    return number


async def run_async():
    return await asyncio.gather(
        *(async_waiting_task(i) for i in range(4))
    )


def main():
    start = time.perf_counter()
    sequential = [waiting_task(i) for i in range(4)]
    print("Sequential:", sequential, time.perf_counter() - start)

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        threaded = list(pool.map(waiting_task, range(4)))
    print("Threaded:", threaded, time.perf_counter() - start)

    start = time.perf_counter()
    asynchronous = asyncio.run(run_async())
    print("Async:", asynchronous, time.perf_counter() - start)


if __name__ == "__main__":
    main()