# bact-ARF

A series of systematic analyses on Alternative Reading Frames (ARFs) of bacterial genomes.

## Execution environment

- The execution envionment of our analysis can be reproduced with docker and docker-compose.
- All the analyses with Python were performed on jupyter lab, which was built under a docker-compose service called 'jupyterlab'.
  - Execute `docker-compose up -d jupyterlab` to activate the environment.
  - The port number on the host side is set to 6543 in `docker-compose.yml`. Change it according to your environment.
  - Run the following command to list the running instance of jupyter lab: `docker-compose exec jupyterlab jupyter lab list`. This will display the access link to the jupyter server as "http://0.0.0.0:8888/?token=<access token> :: /home/jovyan".
  - Replace "0.0.0.0:8888" with the appropriate IP and port number (e.g. "localhost:6543"), and type the link into a browser such as Chrome.
- The instructions for dockers to run external tools can be found in the jupyter notebooks where the relevant analyses were performed. They can be found in `notebooks/`.

## Files

- `data/` is a large directory that contains omics data downloaded from public databases and intermediate files of analyses. Since it is symbolically linked to the other disk, the content is not exposed to the repository.
- `metadata/` is a directory that contains files describing the location of public data, additional information about the data, and so on. See `metadata/README.md` for more details.
- `notebooks/` is the directory that contains all the analysis code (jupyter notebooks). See `notebooks/README.md` for more details.
- `pyscripts/` is a directory where we place files to be imported when conducting Python analysis in notebooks. See `pyscripts/README.md` for more details.
- `docker/` contains the Dockerfiles, which describe the instructions to build docker images for different types of analysis. See also `docker-compose.yml`, whch describes the settings for running docker.
- `scripts/` includes the scripts for batch analysis with external tools. Note that these codes are intended to be mounted and executed in docker containers.


## Citation

Yamanouchi, S., and Iwasaki, W. (2021). *Genomic evidence for disordered proteins encoded by alternative reading frames.* Manuscript submitted for publication.

