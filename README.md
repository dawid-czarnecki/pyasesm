# ArcSight ESM ActiveList connector

**Latest release**: 1.0
**License**: GNU GPL

This is a library to connect to Active List in ArcSight ESM tool and perform simple actions like list/add/remove entries.
It uses REST API through requests2 and json body of requests and responses.

## Requirements
* simplejson
* requests

## Installation
```
git clone https://github.com/dawid-czarnecki/pyasesm

pip install .
```

## Usage example

### Get info about active list
```python
from pyasesm import ActiveLists

active_list = ActiveLists('https://localhost:8443', 'admin', 'password', proxies=None, verify=False, list_id='YWJjCg==')
print(active_list.info()['act.getResourceByIdResponse']['act.return']['fieldNames'])
```

### Get all entries
```python
from active_list import ActiveLists

active_list = ActiveLists('https://localhost:8443', 'admin', 'password', proxies=None, verify=False, list_id='YWJjCg==')
print(active_list.getEntries())
```

## Development
Here are some resources to make future development easier:
* https://<esm_url>:8443/www/manager-service/services/ActiveListService?wsdl
* https://h41382.www4.hpe.com/gfs-shared/downloads-273.pdf

In case of extending this lib to more than Active List this is a list of three letter extensions for requests:
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/activeListService/", "act");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/archiveReportService/", "arc");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/caseService/", "cas");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/conAppService/", "cap");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/connectorService/", "con");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/dashboardService/", "das");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/dataMonitorQoSService/", "dmq");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/dataMonitorService/", "dat");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/drilldownListService/", "drl");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/drilldownService/", "dri");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/fieldSetService/", "fie");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/fileResourceService/", "fil");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/graphService/", "gra");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/groupService/", "gro");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/internalService/", "int");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/managerAuthenticationService/", "man");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/networkService/", "net");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/portletService/", "por");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/queryService/", "que");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/queryViewerService/", "qvs");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/reportService/", "rep");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/resourceService/", "res");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/securityEventIntrospectorService/", "sei");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/securityEventService/", "sev");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/serverConfigurationService/", "ser");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/userResourceService/", "use");
    ns.put("http://ws.v1.service.resource.manager.product.arcsight.com/viewerConfigurationService/", "vie");
    ns.put("http://ws.v1.service.manager.product.arcsight.com/infoService/", "inf");
    ns.put("http://ws.v1.service.manager.product.arcsight.com/managerSearchService/", "mss");

## License
[GNU General Public License v3.0](https://github.com/dawid-czarnecki/pyasesm/COPYING)