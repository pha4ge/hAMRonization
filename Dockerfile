# base image
FROM docker.io/library/python:3.14.4-alpine3.23

# metadata
LABEL org.opencontainers.image.version=1.2.0
LABEL org.opencontainers.image.base.name="docker.io/library/python:3.14.4-alpine3.23"
LABEL org.opencontainers.image.base.digest="sha256:105efb1f600e4e5d216985f6eeda0ed853ff9b38e65877039781f448ed677a0f"
LABEL org.opencontainers.image.title="hAMRronization"
LABEL org.opencontainers.image.title="Parse multiple Antimicrobial Resistance Analysis Reports into a common data structure"
LABEL org.opencontainers.image.source="https://github.com/pha4ge/hAMRonization"
LABEL org.opencontainers.image.documentation="https://github.com/pha4ge/hAMRonization/blob/master/README.md"
LABEL org.opencontainers.image.licenses="LGPL-3.0-only"
LABEL org.opencontainers.image.authors="Finlay Maguire <finlaymaguire@gmail.com>, Marco van Zwetselaar <io@zwets.it>"
LABEL tags="Genomics"

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
