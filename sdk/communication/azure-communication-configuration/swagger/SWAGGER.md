# Azure Communication Configuration for Python

> see https://aka.ms/autorest

### Setup
```ps
cd C:\work
git clone --recursive https://github.com/Azure/autorest.python.git
cd autorest.python
git checkout azure-core
npm install
```

### Generation
```ps
cd <swagger-folder>
autorest ../README.md --use=C:/work/autorest.python --version=2.0.4280
```

### Settings
``` yaml
input-file: ./swagger.json
output-folder: ../azure/communication/configuration/_generated
namespace: azure.communication.configuration
license-header: MICROSOFT_MIT_NO_VERSION
payload-flattening-threshold: 3
no-namespace-folders: true
clear-output-folder: true
python: true
```