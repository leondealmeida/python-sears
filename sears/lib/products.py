#coding: utf-8
"""
Products module

Comprises all product-related classes

"""

class SimpleProduct:
    def __init__(self, data):
        self._supported_keys = [
            'automotivedivision', 'beantype', 'brandname', 'catentryid', 
            'clearanceindicator', 'cutprice', 'defaultfullfillment',
            'directdelivery', 'displayprice', 'freeshippingeligible', 
            'hero', 'image', 'imageid', 'ksnvalue', 'mfgpartnumber', 'name',  
            'newbundleexperience', 'partnumber', 'pbtype', 'promoind', 
            'regionalpriceindicator', 'sellercount', 'skupartnumber', 'source',  
            'stockindicator', 'storeorigin'
        ]
        
        self._stored_keys = []
        
        boolean_keys = [
            'promoind', 'clearanceindicator', 'hero', 'freeshippingeligible',
            'newbundleexperience', 'regionalpriceindicator', 
            'directdelivery', 'stockindicator'
        ]
        true_values = ['1', 'true', 'yes']
        
        float_keys = ['cutprice', 'displayprice']
        int_keys = ['sellercount']
        
        # store each supported key
        for key in self._supported_keys:
            if data.has_key(key):
                # convert known boolean keys
                if key in boolean_keys:
                    setattr(self, key, (data[key].lower() in true_values))
                else:
                    # convert known float keys
                    if key in float_keys or key in int_keys:
                        if data[key] == "":
                            setattr(self, key, 0)
                        else:
                            if key in int_keys:
                                setattr(self, key, int(data[key]))
                            else:
                                setattr(self, key, float(data[key]))
                    else:
                        setattr(self, key, data[key])
                
                self._stored_keys.append(key)
        
    def __getattr__(self, name):
      if name not in self._stored_keys and name in self._supported_keys:
          return None
      else:
          raise AttributeError("SimpleProduct instance has no attribute named %s." % name)
          
class DetailedProduct:
    def __init__(self, data):
        raise NotImplementedError("DetailedProduct class is not ready for parsing and storing info yet.")

