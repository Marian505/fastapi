# FastApi HTML to PDF generator
Simple HTML to PDF generator programmed in FastApi and python.
This project is just example.

Documentation is on path:
http://ip:8000/docs

API is on path:
http://ip:8000/api


# OpenApi generation WIP
Does not work yet
```bash
npm i -g @openapitools/openapi-generator-cli
openapi-generator-cli version

openapi-generator-cli generate \
  -i openapi.yaml \
  -g python-fastapi \
  -o generated \
  --global-property=models \
  --additional-properties=modelPackage=models
```