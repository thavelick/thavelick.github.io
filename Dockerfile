FROM ubuntu:24.04
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*
ENTRYPOINT ["sqlite3"]
