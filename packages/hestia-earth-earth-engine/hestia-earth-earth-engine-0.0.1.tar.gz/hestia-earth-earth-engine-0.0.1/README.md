# Hestia Earth Engine

[![Pipeline Status](https://gitlab.com/hestia-earth/hestia-earth-engine/badges/master/pipeline.svg)](https://gitlab.com/hestia-earth/hestia-earth-engine/commits/master)
[![Coverage Report](https://gitlab.com/hestia-earth/hestia-earth-engine/badges/master/coverage.svg)](https://gitlab.com/hestia-earth/hestia-earth-engine/commits/master)

Hestia's utilities to make queries to Earth Engine.

## Getting Started

1. Sign up for a [Google Cloud Account](https://cloud.google.com)
2. Enable the [Earth Engine API](https://developers.google.com/earth-engine)
3. Create a [Service Account with Earth Engine access](https://developers.google.com/earth-engine/guides/service_account)
4. Set the following environment variable:
```
EARTH_ENGINE_ACCOUNT_ID=<service account ID with access to Earth Engine API on Google Cloud Platform>
```
5. Set the service account JSON credentials in the following file: `ee-credentials.json`

## Install

1. Install Python `3` (we recommend using Python `3.6` minimum)
2. Install the module:
```bash
pip install hestia_earth.earth_engine
```

### Usage

```python
from hestia_earth.earth_engine import run

# fetch sand content for a specific location
run('coordinates', {
  "collection": "users/hestiaplatform/T_SAND",
  "ee_type": "raster",
  "latitude": -11.77,
  "longitude": -45.7689
})
```
