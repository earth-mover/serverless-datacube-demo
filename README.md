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

## Usage

```
% python src/main.py --help
Usage: main.py [OPTIONS]

Options:
  --start-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  Start date for the data cube. Everything but
                                  year and month will be ignored.  [required]
  --end-date [%Y-%m-%d|%Y-%m-%dT%H:%M:%S|%Y-%m-%d %H:%M:%S]
                                  Start date for the data cube. Everything but
                                  year and month will be ignored.  [required]
  --bbox <FLOAT FLOAT FLOAT FLOAT>...
                                  Bounding box for the data cube in lat/lon.
                                  (min_lon, min_lat, max_lon, max_lat)
                                  [required]
  --time-frequency-months INTEGER RANGE
                                  Temporal sampling frequency in months.
                                  [1<=x<=24]
  --resolution FLOAT              Spatial resolution in degrees.  [default:
                                  0.0002777777777777778]
  --chunk-size INTEGER            Zarr chunk size for the data cube.
                                  [default: 1200]
  --bands TEXT                    Bands to include in the data cube. Must
                                  match band names from odc.stac.load
                                  [default: red, green, blue]
  --varname TEXT                  The name of the variable to use in the Zarr
                                  data cube.  [default: rgb_median]
  --epsg [4326]                   EPSG for the data cube. Only 4326 is
                                  supported at the moment.  [default: 4326]
  --serverless-backend [coiled|modal|lithops]
                                  [required]
  --storage-backend [arraylake|fsspec]
                                  [default: arraylake; required]
  --arraylake-repo-name TEXT
  --arraylake-bucket-nickname TEXT
  --fsspec-uri TEXT
  --limit INTEGER
  --debug
  --initialize / --no-initialize  Initialize the Zarr store before processing.
  --help                          Show this message and exit.
```

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

