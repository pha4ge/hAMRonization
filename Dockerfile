# base image
FROM python:3.9-alpine

# metadata
LABEL base.image="python:3.9"
LABEL software="hAMRonization"
ARG SOFTWARE_VERSION=unspecified
LABEL software_version=$SOFTWARE_VERSION
LABEL description="Tool to identify resistance genes using the CARD database"
LABEL website="https://github.com/pha4ge/hAMRonization"
LABEL documentation="https://github.com/pha4ge/hAMRonization/blob/master/README.md"
LABEL license="https://github.com/pha4ge/hAMRonization/blob/master/LICENSE.txt"
LABEL tags="Genomics"

# maintainer
MAINTAINER Finlay Maguire <finlaymaguire@gmail.com>

# add bash so Nextflow can run the container
RUN apk add --no-cache bash && rm -rf /var/cache/apk/*

# set the working directory in the container
WORKDIR /hAMRonization

# copy the sources into the container
COPY . /hAMRonization/src

# install dependencies and clean all up
RUN python -m pip --no-cache-dir install ./src && rm -rf ./src

# command to run on container start without args
CMD ["hamronize", "--help"]
