# Use Python 3.8 image as the base image
FROM python:3.8-buster

# Install the necessary dependencies
RUN apt-get update && apt-get install -y wget

# Download the wkhtmltopdf package
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.buster_amd64.deb

# Install the package
RUN apt-get install -y --no-install-recommends ./wkhtmltox_0.12.6-1.buster_amd64.deb

# Copy the requirements.txt file
COPY requirements.txt /app/

# Change the working directory
WORKDIR /app/

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the app files
COPY src/ /app/src/
COPY app.py /app/


# Expose port 7860
EXPOSE 7860

# Set the command to run when the container starts
CMD ["python3", "-m" ,"streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]

