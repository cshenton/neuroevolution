FROM python:3.5

# Download and install cmake binary, zlib
RUN wget https://cmake.org/files/v3.10/cmake-3.10.3-Linux-x86_64.tar.gz
RUN tar xzf cmake-3.10.3-Linux-x86_64.tar.gz && \
    mkdir /opt/cmake && \
    mv cmake-3.10.3-Linux-x86_64/* /opt/cmake/ && \
    ln -s /opt/cmake/bin/cmake /usr/local/bin/cmake
RUN apt-get update && apt-get install zlib1g-dev

# Install python dependencies
RUN pip install \
    grpcio \
    gym[atari] \
    tensorflow

# Add source and generated code
WORKDIR /neuro-worker
ADD worker/ worker/
ADD proto/neuroevolution_pb2.py proto/neuroevolution_pb2.py
ADD proto/neuroevolution_pb2_grpc.py proto/neuroevolution_pb2_grpc.py

ENV PYTHONUNBUFFERED=0

CMD ["python","-m","worker.main"]