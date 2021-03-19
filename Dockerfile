# base image
FROM python:3.9

# metadata
LABEL base.image="pathon:3.9"
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

# set the working directory in the container
WORKDIR /hAMRonization

# copy the dependencies file to the working directory
COPY . /hAMRonization

# install dependencies
RUN python -m pip install hAMRonization

# command to run on container start
ENTRYPOINT ["hamronize"] 
CMD ["--help"]
