import os

import modal
import zarr
from lib import ChunkProcessingJob, ChunkProcessingResult

stub = modal.Stub("serverless-datacube")

image = (
    modal.Image.micromamba(python_version="3.10")
    .micromamba_install(
        "arraylake",
        "pystac-client",
        "odc-stac",
        "odc-geo",
        "odc-algo",
        "rasterio",
        "cartopy",
        "zarr>=2.17.2",
        "s3fs",
        channels=["conda-forge"],
    )
    .pip_install("pydantic==2.5.3", "fastapi==0.109.0")
    .env({"ZARR_V3_EXPERIMENTAL_API": "1"})
)


@stub.function(
    image=image,
    secrets=[
        modal.Secret.from_name("ryan-aws-secret"),
        modal.Secret.from_name("arraylake-token"),
    ],
    mounts=[modal.Mount.from_local_python_packages("lib")],
)
def process_chunk(
    job: ChunkProcessingJob, array: zarr.Array, debug: bool
) -> ChunkProcessingResult | None:
    #  work around modal env bug with httpx
    os.environ.pop("SSL_CERT_DIR", None)
    return job.process(array, debug=debug)


def spawn_modal_jobs(
    jobs: list[ChunkProcessingJob], array: zarr.Array, debug: bool
) -> list[ChunkProcessingResult]:
    with stub.run():
        # need to iterate to trigger execution
        results = [
            r for r in process_chunk.map(jobs, kwargs={"array": array, "debug": debug})
        ]
    return results
