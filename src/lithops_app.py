import lithops
import zarr
from lib import ChunkProcessingJob, ChunkProcessingResult


def process_chunk(
    job: ChunkProcessingJob, array: zarr.Array, debug: bool
) -> ChunkProcessingResult:
    # arraylake.config.set({"chunkstore.uri": "s3://arraylake-test"})
    return job.process(array, debug=debug)


def spawn_lithops_jobs(
    jobs: list[ChunkProcessingJob], array: zarr.Array, debug: bool
) -> list[ChunkProcessingResult | None]:
    base_fexec = lithops.FunctionExecutor(
        runtime="serverless-datacube", runtime_memory=16 * 256
    )
    retry_fexec = lithops.RetryingFunctionExecutor(base_fexec)
    futures = [
        lithops.retries.RetryingFuture(
            base_fexec.call_async(process_chunk, (job, array, debug)),
            process_chunk,
            (job, array, debug),
            retries=5,
        )
        for job in jobs
    ]

    # use longer wait period for large number of futures
    wait_dur_sec = 10 if len(futures) > 3000 else 1

    retrying_done, retrying_pending = retry_fexec.wait(
        futures, throw_except=False, wait_dur_sec=wait_dur_sec
    )
    assert len(retrying_pending) == 0

    result = [r.response_future.result(throw_except=False) for r in retrying_done]
    return result
