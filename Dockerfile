ARG config.file
# Use an official Python runtime as a parent image
FROM python:3.6.5-slim

RUN apt-get update && apt-get install -y build-essential curl

# Set the working directory to /app
WORKDIR /app
ADD . /app

# Copy the current directory contents into the container at /app

# Install requirements
RUN pip install numpy==1.14.3 && \
    pip install pandas==0.23.3 && \
    pip install pystan==2.17.1.0 && \
    pip install fbprophet==0.3.post2 && \
    pip install statsmodels==0.9.0&& \
    pip install scipy==1.1.0

# Define environment variable
ENV NAME sibur

# Run code when the container launches
CMD python code_base/first_track.py && python code_base/second_track.py && ls data