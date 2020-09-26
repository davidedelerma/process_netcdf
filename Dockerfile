FROM jupyter/base-notebook:612aa5710bf9

RUN conda config --add channels conda-forge

COPY requirements.txt /tmp/

RUN conda install --yes --file /tmp/requirements.txt iris && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

ENV S3_URL=http://s3-uk-1.sa-catapult.co.uk
ENV S3_BUCKET=csvs-netcdf
ENV S3_ID=testID
ENV S3_KEY=test_key

COPY ./src ./work/src
COPY ./notebooks ./work/notebooks


