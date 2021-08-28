FROM python:3.9

WORKDIR /properly
COPY ./ /properly

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt