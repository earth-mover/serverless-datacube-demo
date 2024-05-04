import coiled
import zarr
from lib import ChunkProcessingJob, ChunkProcessingResult
from tqdm import tqdm


@coiled.function(
    cpu=4, region="us-west-2", environ={"ZARR_V3_EXPERIMENTAL_API": "1"}, keepalive="5m"
)
def process_chunk(
    job: ChunkProcessingJob, array: zarr.Array, debug: bool
) -> ChunkProcessingResult | None:
    return job.process(array, debug=debug)


def spawn_coiled_jobs(
    jobs: list[ChunkProcessingJob], array: zarr.Array, debug: bool
) -> list[ChunkProcessingResult]:
    # futures = []
    # for job in jobs:
    #     future = process_chunk.submit(job, array, debug=debug)
    #     futures.append(future)
    # results = [f.result() for f in tqdm(futures)]

    # map does not return futures - hard to monitor progress
    jobs = list(jobs)
    results = list(
        tqdm(
            process_chunk.map(jobs, array=array, debug=debug, retries=5),
            total=len(jobs),
            desc="Jobs Completed",
        )
    )

    return results
