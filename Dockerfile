FROM python:3.7-alpine
COPY . /app
WORKDIR /app
ENTRYPOINT [ "python", "get_duplicate_files.py" ]
CMD ["."]