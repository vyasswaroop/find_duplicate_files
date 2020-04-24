# Find Duplicate files

A simple python script to find duplicate files within a directory. The function takes the directory as the argument and return the duplicate files.

### Run with Docker

1. Build image
`docker build -t find-duplicate-files .`

2. Run image
`docker run -v <path-directory-to-mount>:/test find-duplicate-files /test`
