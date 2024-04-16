# Serverless Sentinel Mosaic

This repo demonstrates how to build a Zarr-based data cube from [Sentinel 2 L2A Data](https://registry.opendata.aws/sentinel-2-l2a-cogs/)
in the AWS Open Data Program.

**Note**: This repo is for demonstration purposes only. It does not aspire to be a maintained package.
If you want to build on top of it, fork this repo and modify it to your needs.

**License:** Apache 2.0

**Supported Serverless Backends**

- [Coiled Functions](https://docs.coiled.io/user_guide/usage/functions/index.html)
- [Modal](https://modal.com)
- [LithOps](https://lithops-cloud.github.io/) (AWS Lambda Executor)

**Supported Storage Locations**

- [Arraylake](https://docs.earthmover.io/) - Earthmover's data lake platform for Zarr data
- Any [fsspec](https://filesystem-spec.readthedocs.io/en/latest/)-compatible cloud storage location (e.g. S3)

## Example Usage

Vermont Datacube (monthly for 4 years), store in Arraylake

```
python src/main.py --start-date 2020-01-01 --end-date 2023-12-31 --bbox -73.43 42.72 -71.47 45.02 \
--arraylake-repo-name "earthmover-demos/sentinel-datacube-Vermont" --arraylake-bucket-nickname earthmover-demo-bucket \
--storage-backend arraylake --serverless-backend lithops
```

All of South America, one single month, store in Arraylake

```
python src/main.py --start-date 2020-01-01 --end-date 2020-01-31 --bbox -82 -56 -34 13 --chunk-size 1800 \
--arraylake-repo-name "earthmover-demos/sentinel-datacube-South-America" --arraylake-bucket-nickname earthmover-demo-bucket
--storage-backend arraylake --serverless-backend lithops 
```

All of South America, 12 months, store in plain S3 bucket

```
 python src/main.py --start-date 2020-01-01 --end-date 2020-12-31 --bbox -82 -56 -34 13 \
 --storage-backend fsspec --fsspec-uri s3://earthmover-sample-data/zarr-datacubes/South-America\
  --serverless-backend modal
```


## Lithops Setup


```
lithops runtime build -f PipDockerfile -b aws_lambda serverless-datacube
```

