import os
import CloudFlare

DEBUGCF=os.environ.get('DEBUGCF',False)

class CFzone:
    """ CloudFlare dns zone """

    def __init__(self, cf_domain, ):

        self._domain = cf_domain
        self._cf = CloudFlare.CloudFlare(debug=DEBUGCF)

        cfzones = self._cf.zones.get(params={'match':'all','name':cf_domain})
        if len(cfzones) != 1:
            raise Exception('Zone not unique')

        self._zoneinfo = cfzones[0] 

        self.zoneid = self._zoneinfo['id']


    def create(self,params):
        """ Add a record, return the record id """

        r = self._cf.zones.dns_records.post(self.zoneid, data=params)        
        return r['id']


    def get(self,params={}):
        """ Get a record """

        r = self._cf.zones.dns_records.get(self.zoneid,params=params)
        return r


    def getid(self,params={}):
        """ Return a specific record id """

        r = self.get(params)
        recs = len(r)
        if recs == 1:
            return r[0]['id']
        elif recs == 0:
            return 0
        else:
            raise Exception('Multiple records found') 


    def set(self,rid,params={}):
        """ Set (update) a specific record id """

        r = self._cf.zones.dns_records.put(self.zoneid, rid, data=params)

        return r['id']        


    def delete(self,rid):
        """ Delete a DNS record """
        r = self._cf.zones.dns_records.delete(self.zoneid, rid)


class   TXTrec:
    """  DNS TXT record abstraction """

    def __init__(self, domain):

        self.zone = CFzone(domain)
        self.domain = domain

    def set(self, name, contents):
        """ set (update or create) a TXT record """

        fqdn = name if name.endswith(self.domain) else f'{name}.{self.domain}'

        rid = self.zone.getid({'name':fqdn,'type': 'TXT', 'match': 'all'})
        if rid:
            # update record
            self.zone.set(rid,{'name': name, 'type': 'TXT', 'content': contents})
        else:
            # new record
            self.zone.create({'name': name, 'type': 'TXT', 'content': contents})


    def get(self, name):
        """ get contents of a TXT record """

        fqdn = name if name.endswith(self.domain) else f'{name}.{self.domain}'

        r =  self.zone.get({'name': fqdn, 'type': 'TXT', 'match': 'all'})

        recs = len(r)
        if recs == 1:
            return r[0]['content']
        elif recs == 0:
            return None
        else:
            raise Exception("Multiple records found")


    def rem(self, name):
        """ remove a TXT record """

        fqdn = name if name.endswith(self.domain) else f'{name}.{self.domain}'

        rid = self.zone.getid({'name':fqdn,'type': 'TXT', 'match': 'all'})
        if rid:
            r = self.zone.delete(rid)
            return True
        else:
            return False
    
