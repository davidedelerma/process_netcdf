# A repository containing code to handle ERA 5 data provided by UK MetOffice

## Docker image spins up a jupyter instance:

to run Jupyter notebook locally first build the image with:

`docker build -t <your docker repo>:<your tag> .`

e.g.: `docker build -t davidedelerma/nc_playground:0.0.6 .`

then run the docker container using:

`docker run -it 
-p 8888:8888 
-e S3_ID=<your aws access key> 
-e S3_KEY=<your aws secret access key> 
davidedelerma/netcdf_playground:0.0.6`

This docker file is based on the official jupyter notebook base image so full focumentation can be found at:
[Link to official jupyer docker documentation](https://jupyter-docker-stacks.readthedocs.io/en/latest/using/common.html)

### To persist the jupyter notebooks:  
```
docker run -it -p 8888:8888 
-e S3_ID=test 
-e S3_KEY=test 
-v <absolute path to project directory>/notebooks:/home/jovyan/work davidedelerma/nc_playground:0.0.19
```

### To run the 30 years average processor:

`docker run -it 
-e GRANT_SUDO=yes 
--user root 
-p 8888:8888 
-e S3_ID=<your aws access key> 
-e S3_KEY=<your aws secret access key>
-e PYTHONPATH=/home/jovyan/code/src/
-w /home/jovyan/code/src
davidedelerma/nc_playground:0.0.19 
python ./entrypoints/process_30ys_average.py`
