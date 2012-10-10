"""
Python Wrapper for the Sears API (v1)

Author: Leon de Almeida
https://github.com/leondealmeida/python-sears

"""

import json
from urllib import urlencode
from urllib2 import urlopen, URLError

from sears.lib.products import SimpleProduct, DetailedProduct


class SearsAPI:
    def __init__(self, apikey):
        self.apikey = apikey
        self.store = "Sears"
        
        self.api_url = "http://api.developer.sears.com/v1/"
        
        
    def _prepare_qs(self, opts):
        """Adds the common required parameters to all REST calls to the passed
        dictionary
        
        """
        
        common = { 'apikey': self.apikey, 'store': self.store, 
            'contentType': 'json' }
        opts.update(common)
        
        return opts
        
        
    def _read_url(self, url):
        """Wraps the URL reading routine"""
        try:
            info = urlopen(url)
    
            if info.getcode() != 200:
                raise Exception("HTTP return code %i received for url %s." %
                                (info.getcode(), url))
                
            return info.read()
            
        except URLError as e:
            raise e
        
        
    def product_search(self, keywords, search_type="keyword"):
        """Searches for products based on keywords
        #TODO: support other Sears' search methods
        
        """

        opts = urlencode(self._prepare_qs({'keyword': ','.join(keywords),
                        'searchType': 'keyword'}))
        search_url = "%sproductsearch?%s" % (self.api_url, opts)
        
        data = self._read_url(search_url)
            
        #parse data
        data_dict = json.loads(data)['mercadoresult']
        
        if int(data_dict['status']) != 0:
            raise Exception("Error %s detected: %s" % 
                            (data_dict['status'], data_dict['errormessage']))
            
        if int(data_dict['productcount']) == 0:
            return []
        else:
            return [SimpleProduct(p) for p in                   
                    data_dict['products']['product'][1]]
        
        
    def product_lookup(self, part_number):
        """Retrieves details about a single product"""
        
        opts = urlencode(self._prepare_qs({'partNumber': part_number, 'Showspec': '1'}))
        details_url = "%sproductdetails?%s" % (self.api_url, opts)
        
        data = self._read_url(details_url)
        
        #parse data
        data_dict = json.loads(data)['productdetail']
        
        if int(data_dict['statusdata']['responsecode']) != 0:
            raise Exception("Error %s detected: %s" %       
                            (data_dict['statusdata']['responsecode'],       
                            data_dict['statusdata']['errormessage']))

        return DetailedProduct(data_dict['softhardproductdetails'][1][0])
        
        
    