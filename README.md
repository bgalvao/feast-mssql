# feast-mssql

An offline store plugin in development.

## Set up dev environment

The dev dependencies are in the two `environment.*.yml` files.

- `dev` is meant to install the feast-mssql dependencies to run Feast.
- `mssql-cli` installs the mssql client to a python 3.7 environment, without Feast.

thus, run

```
conda create -f environment.dev.yml -c conda-forge -n feast-mssql
conda create -f environment.mssql-cli.yml -c conda-forge -n mssql-cli
```

and then activate and deactivate the environments (`feast-mssql` and `mssql-cli`) as you need them.

(In the future, if justifiable, I am switching this over to PDM...)


## Set up to develop against an Offline Store

You want to have sample data in the (dummy) database that is standing as a Data Warehouse / Offline Store. Then you can run feast apply to check whether the implementation is working as intended.

```shell
# spin up a dummy database, specified in docker-compose.yml
docker compose up -d

# create the database namespace to put the sample data into
conda activate mssql-cli
mssql-cli -U sa -P Dck3r_pa55 -S localhost \
-Q "IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'feast_offline_store') BEGIN CREATE DATABASE feast_offline_store END;"

# put the driver sample table from Feast into the above created database
conda activate feast-mssql
python feast_mssql/templates/mssql/bootstrap.py

# install this package in editable mode
pip install -e .

# cd into the *feature repo* named witty_lioness
cd witty_lioness

# run the example driver_repo.py and fix bugs against that
feast apply
```
