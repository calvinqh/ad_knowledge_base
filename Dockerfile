FROM python3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents to the container's /app directory
ADD . /app

# Install any needed packages specified by the requirements
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Define enviroment variable
ENV NAME ADKB

# Run the cli program when container launches
CMD ["python","cli.py"]
