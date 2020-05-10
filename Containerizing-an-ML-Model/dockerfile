#sets the base image for subsequent instructions
FROM continuumio/miniconda3

#copy files into the container
COPY ./api /api

#set the current working directory
WORKDIR /api

#dowloads the package lists form the repositories and 'updates' them to get incormation on the newsest versions of packages and their dependancies
RUN apt-get update 

# update conda
RUN conda update -n base -c defaults conda

# create the environment
RUN conda env create -f environment.yml

# activate spacy environment
RUN echo "source activate spacy" > ~/.bashrc
ENV PATH /opt/conda/envs/spacy/bin:$PATH

# download model
RUN python -m spacy download en_core_web_sm

# run the gunicorn command to start the api in docker
CMD ["gunicorn", "-w", "1", "-b", ":5000", "-t", "360", "wsgi:app"]
