# osdata-utils

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

# OS Data Downloader
**OS Data Downloader** is a Python package designed to interact with the Ordnance Survey API, enabling users to query and download geospatial datasets such as urban areas, buildings, roads, and more. The package supports both open and premium products and provides tools for transforming CRS, querying specific features, and overlaying data on raster maps.

A python package to query and process Ordnance Survey data via the OSDataHub API

## Features
* Query and download geospatial data from the Ordnance Survey API.
* Supports both open and premium datasets.
* Seamlessly integrates with GeoTIFF files to extract metadata and transform bounding boxes.
* Provides pre-defined product dictionaries for quick access to datasets.
* Includes helper functions for CRS transformations and bounding box operations.

## Installation

```bash
python -m pip install osdata_utils
```

From source:
```bash
git clone https://github.com/DGalexander/osdata-utils
cd osdata-utils
python -m pip install .
```

## Usage

#### Workflow Options
OS Data Downloader integrates seamlessly with both MapReader workflows and independent TIFF-based workflows:

1. MapReader Integration:

* Extract bounding boxes directly from the maps.parents object.
* Leverages metadata from MapReader for spatial queries.

2. TIFF-Based Workflow:

* Use Rasterio to extract bounding box and CRS from TIFF files.
* Works independently of MapReader.

See [tests/test_osdata_mapreader_integration.ipynb](tests/test_osdata_mapreader_integration.ipynb) for example workflows.


### Supported Datasets

The package includes access to the following datasets:

#### Open Products:
* Urban Areas
* Local and District Buildings
* Foreshore
* Greenspace
* National Parks
* Railways and Roads
* Surface Water
* Woodland

#### Premium Products:
* Topographic Areas, Points, and Lines
* Detailed Path and Water Networks
* Functional Sites
* Greenspace Areas

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).


<!-- prettier-ignore-start -->
[actions-badge]:            https://github.com/DGalexander/osdata-utils/workflows/CI/badge.svg
[actions-link]:             https://github.com/DGalexander/osdata-utils/actions
[pypi-link]:                https://pypi.org/project/osdata-utils/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/osdata-utils
[pypi-version]:             https://img.shields.io/pypi/v/osdata-utils
<!-- prettier-ignore-end -->
