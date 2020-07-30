# Azure Communication Configuration for Python

> see https://aka.ms/autorest

### Setup
```ps
npm install -g autorest
```

### Generation
```ps
cd <swagger-folder>
autorest README.md
```

### Settings
``` yaml
input-file: ./swagger.json
output-folder: ../azure/communication/chat/_generated
namespace: azure.communication.chat
license-header: MICROSOFT_MIT_NO_VERSION
payload-flattening-threshold: 3
no-namespace-folders: true
clear-output-folder: true
python: true
```