# Find Duplicate files

A simple python script to find duplicate files within a directory. The function takes the directory as the argument and return the duplicate files.

### Run with Docker

1. Build image
`docker build -t find-duplicate-files .`

2. Run image
`docker run -v <path-directory-to-mount>:/test find-duplicate-files /test`

### Process

1. Group files with same size
2. Compare the files in each group by repeatedly checking md5 checksum for a chunk size of 1k
3. Print duplicate files in a seperate lines

### Code Improvements implemented

1. Multithreading for each group of files with same size
2. Not checking the duplicates of files that dont have same size

### Improvements to be done

1. Multiprocessing with multithreading

### Assumptions

1. duplicate files should have same size
