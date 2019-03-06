"""Python API using the REST interface of ArcSight ESM."""

try:
    import simplejson as json
except ImportError:
    import json
import requests

class ActiveLists(object):
    """Python API for ArcSight ESM active lists.

    Example:
        from pyasesm import ActiveLists
        active_list = ActiveLists('https://localhost:8443', 'admin', 'password', proxies=None, verify=False, list_id='YWJjCg==')
        print(active_list.info()['act.getResourceByIdResponse']['act.return']['fieldNames'])

    Attributes:
        url (str): URL of the ArcSight ESM you want to connect to.
        verify (bool): can be True or False. Check the validity of the certificate.
        proxies (dict): Proxy dict as describes here: http://docs.python-requests.org/en/master/user/advanced/#proxies
            Example: proxies={'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
        list_id (str): Resource id of active list.
        _key (str): API key to access ArcSight ESM.

    Args:
        url (str): URL of the ArcSight ESM you want to connect to.
        login (str): Your username.
        password (str): Your password.
        verify (bool): Check the validity of ArcSight certificate.
        proxies (dict): Proxy dict as describes here: http://docs.python-requests.org/en/master/user/advanced/#proxies
            Example: proxies={'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
        list_id (str): Id of the default active list.
        al_service (str): Constant string to referrence active list service.
        key (str): API key returned after authentication.
        active_lists (dict): Dict with list of columns. Keys are ids of active lists.

    Raises:
        Exception: If the url, login, or password was not provided. If could not connect to ArcSight ESM

    """
    
    _key = None

    def __init__(self, url, login, password, verify=True, proxies=None, list_id=None):
        if not url:
            raise Exception('Please provide the URL of your ArcSight ESM.')
        if not login or not password:
            raise Exception('Please provide your login and password.')

        self.url = url
        self.verify = verify
        self.proxies = proxies
        self.list_id = list_id
        self.al_service = 'ActiveListService'
        self.active_lists = {}

        data={'log.login':{'log.login': login, 'log.password': password}}

        self._key = self._send('LoginService', 'login', data=data, service_type='core-service')
        if self._key is False:
            raise Exception('Could not connect to ArcSight ESM')

        self._key = self._key['log.loginResponse']['log.return']

    def __exit__(self):
        """Logout on exit"""

        code = self._send('LoginService', 'logout', data={"log.logout":{}}, service_type='core-service')

    def info(self, resource_id=None):
        """Retrives info about active list.

        Args:
            resource_id (str): Id of the default active list.

        Returns:
            Result from self._send method.

        Raises:
            Exception: If no resource_id and default list_id was provided

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        data = {'act.getResourceById': {'act.resourceId':resource_id}}
        return self._send(self.al_service, 'getResourceById', data=data)

    def getEntries(self, resource_id=None):
        """Retrives entries from active list.

        Args:
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.

        Returns:
            list: List of dicts with all the entries from a specific active list.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        operation = 'getEntries'
        result = self._send(self.al_service, operation, data={'act.'+operation: {'act.resourceId':resource_id}})['act.getEntriesResponse']['act.return']
        columns = result['columns']
        if resource_id not in self.active_lists:
            self.active_lists[resource_id] = columns
        entries = []
        if 'entryList' in result:
            if not isinstance(result['entryList'], list):
                result['entryList'] = [result['entryList']]
            for row in result['entryList']:
                tmp = {}
                for i,column in enumerate(columns):
                    tmp[column] = row['entry'][i]
                entries.append(tmp)

        return entries

    def addEntry(self, entry, resource_id=None):
        """Retrives info about active list.

        Args:
            entry (dict): Entry to add to active list.
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.

        Returns:
            Result from self._send method.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        columns = []
        entry_list = []
        tmp = []
        for column, value in entry.items():
            columns.append(column)
            tmp.append(entry[column])

        entry_list.append({'entry': tmp})
        data = {'act.addEntries': {'act.resourceId':resource_id, 'act.entryList': {'columns': columns, 'entryList': entry_list}}}
        return self._send(self.al_service, 'addEntries', data=data)

    def addEntries(self, entries, resource_id=None):
        """Retrives info about active list.

        Args:
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.
            entries (list of dicts): List of entries to add to active list.

        Returns:
            Result from self._send method.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        columns = []
        entry_list = []
        for entry in entries:
            if not columns:
                for column, value in entry.items():
                    columns.append(column)

            tmp = []
            for column in columns:
                tmp.append(entry[column])

            entry_list.append({'entry': tmp})
        data = {'act.addEntries': {'act.resourceId':resource_id, 'act.entryList': {'columns': columns, 'entryList': entry_list}}}
        # addEntry or insert
        return self._send(self.al_service, 'addEntries', data=data)

    def deleteEntry(self, entry, resource_id=None):
        """Retrives info about active list.

        Args:
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.
            entry (dict): Entry to remove from active list.

        Returns:
            Result from self._send method.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        columns = []
        entry_list = []
        tmp = []
        for column, value in entry.items():
            columns.append(column)
            tmp.append(entry[column])

        entry_list.append({'entry': tmp})

        data = {'act.deleteEntries': {'act.resourceId':resource_id, 'act.entryList': {'columns': columns, 'entryList': entry_list}}}

        return self._send(self.al_service, 'deleteEntries', data=data)

    def deleteEntries(self, entries, resource_id=None):
        """Retrives info about active list.

        Args:
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.
            entries (list of dicts): List of entries to remove from active list.

        Returns:
            Result from self._send method.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        columns = []
        entry_list = []
        for entry in entries:
            if not columns:
                for column, value in entry.items():
                    columns.append(column)

            tmp = []
            for column in columns:
                tmp.append(entry[column])

            entry_list.append({'entry': tmp})
        data = {'act.deleteEntries': {'act.resourceId':resource_id, 'act.entryList': {'columns': columns, 'entryList': entry_list}}}

        return self._send(self.al_service, 'deleteEntries', data=data)

    def clearList(self, resource_id=None):
        """Removes all elements from list.

        Args:
            resource_id (str): Resource id of active list. If None default (self.list_id) will be used.

        Returns:
            Result from self._send method.

        Raises:
            Exception: Exception: If no resource_id and default list_id was provided.

        """

        if resource_id is None and self.list_id is None:
            raise Exception('No resource_id and list_id has been provided.')

        if resource_id is None:
            resource_id = self.list_id

        data = {'act.clearEntries': {'act.resourceId': resource_id}}

        return self._send(self.al_service, 'clearEntries', data=data)

    def _send(self, service, operation, data=None, service_type='manager-service', protocol='rest'):
        """Send request to ArcSight ESM.

        Args:
            service (str): Name of the ArcSight service. Described in <url>/www/<service_type>/services/listServices
            operation (str): Name of the ArcSight operation. Described in <url>/www/<service_type>/services/listServices
            data (dict): Request body.
            service_type (str): Either core-service or manager-service
            protocol (string): REST API (rest) or SOAP (services)

        Returns:
            dict: If proper response was provided return response as dict.
            int: When there is no json respons return status code.

        Raises:
            BaseException: If was unexpected response from ArcSight was received.

        """

        # Stupid format of request body 0.o
        for k in data:
            prefix = k[:k.find('.')]+'.'
            break

        full_operation = prefix + operation
        if self._key is not None and operation != 'login' and prefix+'authToken' not in data[full_operation]:
            data[full_operation][prefix+'authToken'] = self._key

        full_url = "{}/www/{}/{}/{}/{}?alt=json".format(self.url, service_type, protocol, service, operation)
        try:
            response = requests.post(full_url, json=data, proxies=self.proxies, verify=self.verify)
            if response.status_code != 200 and response.status_code != 204 and response.status_code != 500:
                raise BaseException('{} {} {}'.format(response.status_code, response.reason, response.content))
            elif response.status_code == 500:
                e = response.content.decode('utf-8')
                const = '</head><body><h1>'
                e = e[e.find(const)+len(const):]
                const = '</h1><HR size="1" noshade="noshade"><p>'
                e = e[:e.find(const)]
                print(e)
                exit(2)

        except Exception as e:
            print('Unable to connect to ArcSight ({}). Please make sure the login, password and the URL are correct (http/https is required): {}'.format(self.url, str(e)))
            exit(1)

        if response.status_code == 200:
            if isinstance(response.content, bytes):
                response = response.content.decode('utf-8')
            else:
                response = response.content

            r = json.loads(response)
            return r
        else:
            return response.status_code