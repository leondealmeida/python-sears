"""
Products module

Comprises all product-related classes

"""

class _BaseProduct(object):
    """"""
    
    
    def __init__(self):
        self._supported_keys = []
        self._stored_keys = []
    
        self._boolean_keys = []
        self._float_keys = []
        self._int_keys = []
        self._special_keys = []
        
    def __getattr__(self, name):
        if name not in self._stored_keys and name in self._supported_keys:
            return None
        else:
            raise AttributeError("%s instance has no attribute named %s." %
                                 (self.__class__.__name__, name))
    
    @property
    def available_properties(self):
        return self._stored_keys
    
    def _handle_special_keys(self, key, data):
        raise NotImplementedError("%s must override _handle_special_keys." % 
                                  self.__class__.__name__)
    
    def _store_data(self, data):
        """Stores available data and sets the proper storage indicators."""
        
        true_values = ['1', 'true', 'yes', 'y', True]
        
        # store each supported key
        for key in self._supported_keys:
            if data.has_key(key):
                # special keys require special handling
                if key in self._special_keys:
                    self._handle_special_keys(key, data[key])
                else:
                    # convert known boolean keys
                    if key in self._boolean_keys:
                        setattr(self, key, (data[key].lower() in true_values))
                    else:
                        # convert known float keys
                        if key in self._float_keys or key in self._int_keys:
                            if data[key] == "":
                                setattr(self, key, None)
                            else:
                                if key in self._int_keys:
                                    setattr(self, key, int(data[key]))
                                else:
                                    setattr(self, key, float(data[key]))
                        else:
                            setattr(self, key, data[key])
                
                self._stored_keys.append(key)



class SimpleProduct(_BaseProduct):
    
    
    def __init__(self, data):
        super(SimpleProduct, self).__init__()
        
        self._supported_keys = [
            'automotivedivision', 'beantype', 'brandname', 'catentryid', 
            'clearanceindicator', 'cutprice', 'defaultfullfillment',
            'directdelivery', 'displayprice', 'freeshippingeligible', 
            'hero', 'image', 'imageid', 'ksnvalue', 'mfgpartnumber', 'name',  
            'newbundleexperience', 'partnumber', 'pbtype', 'promoind', 
            'regionalpriceindicator', 'sellercount', 'skupartnumber',
            'source', 'stockindicator', 'storeorigin'
        ]
        
        self._boolean_keys = [
            'promoind', 'clearanceindicator', 'hero', 'freeshippingeligible',
            'newbundleexperience', 'regionalpriceindicator', 
            'directdelivery', 'stockindicator'
        ]
        
        self._float_keys = ['cutprice', 'displayprice']
        self._int_keys = ['sellercount']
        
        self._store_data(data)
        
        
                  
class DetailedProduct(_BaseProduct):
    
    
    def __init__(self, data):
        super(DetailedProduct, self).__init__()
        
        self._supported_keys = ['accessory', 'arrivalmethods', 
            'automotivedivision', 'brandname', 'catalogid', 'catentryid',
            'checkoutenable', 'clicktotalk', 'connection', 'descriptionname', 
            'distributioncenter', 'expresscheckouteligible',
            'fitmentrequired', 'followitflag', 'freeshippingeligible',
            'giftwrap',  'groupdescription', 'haulaway', 'imageurls',
            'installationkit', 'instock',  'isfrequencymodel', 'iskmartspu',
            'ksnvalue', 'langid', 'lmpstoredetails',  'longdescription',
            'mailinrebate', 'mainimageurl', 'maintenanceagreement',
            'mapindicator', 'mappedpriceindicator', 'mappricedescription',
            'mappricevaliddate', 'mfgpartnumber', 
            'mobileexpresscheckouteligible', 'numreview', 'onlineonlyprice', 
            'optiontab', 'othercpcmerchants',  'otherfbmmerchants', 
            'partnumber', 'pickupoption', 'presellind',  'presellreleasedate', 
            'productprotectionplan', 'productvariant',  'productvariants', 
            'rating', 'regavlmainflag', 'regularprice', 'relatedurl',  
            'saleprice', 'savestory', 'sellercount', 'shortdescription', 
            'skudiff',  'skulist', 'smartplan', 'soldby', 'specialoffer', 
            'sreseligible', 'storeid',  'storepickupeligible', 'ststype', 
            'swatches', 'variant', 'viewonly',  'webstatus', 'zerofinance'] 

        self._boolean_keys = ['automotivedivision', 'checkoutenable',
            'clicktotalk', 'expresscheckouteligible', 'followitflag',  
            'freeshippingeligible', 'instock', 'iskmartspu', 'mailinrebate', 
            'mainimageurl','mobileexpresscheckouteligible', 'onlineonlyprice', 
            'optiontab','pickupoption', 'presellind', 'regavlmainflag', 
            'specialoffer', 'sreseligible', 'storepickupeligible', 
            'webstatus']
            
        self._float_keys = ['regularprice', 'saleprice']
        
        self._int_keys = ['catalogid', 'catentryid', 'ksnvalue', 'storeid']
        
        self._special_keys = ['arrivalmethods', 'imageurls', 
            'lmpstoredetails', 'othercpcmerchants', 'otherfbmmerchants',         
            'productvariants', 'skulist', 'swatches']

        self._store_data(data)
        
    # override special keys handling method
    def _handle_special_keys(self, key, data):
        values = []
        
        # keys that hold simple lists
        if key in ['arrivalmethods', 'imageurls']:
            single_key = key[:-1:]
            if data[single_key][0]:
                values = data[single_key][1]
        
        # skulist is specialized
        if key == 'skulist':
            if data['sku'][0]:
                values = [{'catentryid': item['catentryid']} 
                          for item in data['sku'][1]]
        
        setattr(self, key, values)
        
        # productvariants is very specialized
        return