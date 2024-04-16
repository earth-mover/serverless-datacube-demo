import random
import time

# from .lib import generate_jobs, process_monthly_chunk
import lithops


def process(n):
    time.sleep(random.choice([1, 20]))
    return n


if __name__ == "__main__":
    fexec = lithops.FunctionExecutor(runtime_timeout=10)

    retry_fexec = lithops.RetryingFunctionExecutor(fexec)
    # futures = retry_fexec.map(process, list(range(10)), retries=5)
    futures = [
        lithops.retries.RetryingFuture(
            fexec.call_async(process, i), process, i, retries=5
        )
        for i in range(10)
    ]
    # retrying only works with throw_except=False
    retrying_done, retrying_pending = retry_fexec.wait(futures, throw_except=False)
    # result = fexec.get_result(throw_except=False)
    assert len(retrying_pending) == 0

    response_done = [f.response_future for f in retrying_done]
    # response_pending = [f.response_future for f in retrying_pending]
    result = [r.result(throw_except=False) for r in response_done]

    print(result)
