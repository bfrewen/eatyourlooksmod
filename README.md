# Eat Your Looks
A POC for doing optical character recognition on recipes to automate indexing for Eat Your Books.

## Getting Started
### Create a virtual environment
python3 -m venv venv
source venv/bin/activate

You can run `deactivate` to exit the virtula environment

### Install the dependencies
Until I create requirements.txt, here is what I've installed

pip install -U pytest
pip install --upgrade google-cloud-vision

### Setup credentials for accessing the Google Vision API
Create a credetials file from the Cloud Console and define an environment variable pointing to that file.

`export GOOGLE_APPLICATION_CREDENTIALS="/path/to/file.json"`

### Run the tests
pytest

## References
Quick start guide for using API client libraries.
https://cloud.google.com/vision/docs/quickstart-client-libraries
