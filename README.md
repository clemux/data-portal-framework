# DPF

## Configuration

`export DPF_DATABASE_URL=sqlite:///./dpf.db`

## Covid module

`dpf covid update-db`

## Elections module

You can retrieve elections.csv on
[data.gouv.fr](https://www.data.gouv.fr/fr/datasets/r/056c3d1e-87ef-42b2-ae9c-57ad9d81b563)

`dpf elections update-db elections.csv`

### Build database

## Run API

`uvicorn dpf.api:app`

## Container deployment

### Build

`podman build -t dpf:latest -f Dockerfile .`

### Build database

 - `mkdir ~/dpf-data`
 - `cp elections.csv ~/dpf-data`
 - `podman run --rm -v ~/dpf-data:/data:z -e DPF_DATABASE_URL=sqlite:////data/dpf.db dpf:latest dpf elections update-db /data/elections.csv`
 - `podman run --rm -v ~/dpf-data:/data:z -e DPF_DATABASE_URL=sqlite:////data/dpf.db dpf:latest dpf covid update-db`

### Run server

 - `podman run -p 8000:8000 --rm -v ~/dpf-data:/data -e DPF_DATABASE_URL=sqlite:////data/dpf.db   dpf:latest uvicorn --host 0.0.0.0 dpf.api:app`
