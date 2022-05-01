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