# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:27:06 2020

@author: J.S. Kroodsma


"""
import re, datetime as dt # core modules
import requests, lxml
from lxml import etree
  
class TreeParser():
    """
    #class variables: same for all instances of class 
    """
    """initialization"""
    def __init__(self,url=None,tree=None,schemas=None,raise_error=True):
        # placeholders
        self.html=None
        if url==None and tree==None:
            raise ValueError('no url and tree set')
        elif url!=None and tree==None:
            tree=self.__get_html_tree__(url)
        self.tree=tree
        self.schemas=schemas
        self.RAISE_ERROR=raise_error
        pass
    
    """property setters"""
    
    """class functions"""
    def __get_html_tree__(self,url):
        #body         
        res=requests.get(url)
        if res.status_code<=299: # error handling
            self.html=res.text
        else:
            raise ValueError('GET on {0} gives status_code {1}'.format(url,res.status_code)) 
        # parse html
        tree = etree.HTML(self.html)
        return(tree)
   
    def __serialize__(self,x):
       """ serialize element to value """
       #body  
       if type(x) in [lxml.etree._ElementUnicodeResult]:
           v=str(x)
       elif hasattr(x,'text'):
           v=x.text
       else:
           #v=str(x)
           v=x
       return(v)
    
    def __transform__(self,x,transform):
       #body         
       # transform element
       if transform!=None:
           if not callable(transform):
               raise NOT_CALLABLE_ERROR(transform)
           v=transform(x)
       else:
           v=x
       return(v)
       
    def apply(self,schema=None,ky=None,t=None):
        """ apply a single schema to the html tree. returns dictionary {value,elements,element} """
        try:
            #body
            # get the schema
            schema=self.schemas[ky] if ky!=None else schema
            # unpack variables from schema
            name,xpath,all_elements,cast,transform=from_kwargs(schema,'name','xpath','all','cast','transform')
            transform=nvl(t,transform)
            # prep outputs
            elements=[]
            value=None
            outputs={'value':None,'elements':elements,'element':None}
            # execute xpath 
            if len(xpath)>0:
                try:
                    elements=self.tree.xpath(xpath)
                except Exception as e:
                    print("exception at xpath {0}:{1}".format(xpath,e))
                    if self.RAISE_ERROR:
                        raise e  
                # get first element
                element=elements[0] if len(elements)>0 else None
                # transform + serialize
                if all_elements==True: # use the first result element
                    value_input=elements
                else:
                    value_input=element
                value=self.__serialize__(self.__transform__(value_input,transform)) # use all elements
                # set as attributesL elements,element
                self.elements=elements
                self.element=element
                outputs={'value':value,'elements':elements,'element':element}
            self.outputs=outputs
        except Exception as e:
            print('error in apply')
            raise e
        #return value
        return(self.outputs)   
        
    def apply_schemas(self,metadata_fields={}):
        """ apply all schemas to html tree and return map name:value """
        try:
            #body
            map0={k:self.apply(ky=k).get('value') for k in self.schemas}
            [map0.update({k:metadata_fields[k]}) for k in metadata_fields]
        except Exception as e:
            print('error in apply_schemas')
            raise e
        #return value
        return(map0) 

# helpers
def nvl(x,default=''):
    return(default if x==None else x)

def from_kwargs(kwargs,*args):
    """ unpack key-values from kwargs into args variables """
    try:
        #body
        kw=tuple([kwargs.get(arg) for arg in args])
    except Exception as e:
        print('error in from_kwargs')
        raise e
    #return value
    return(kw)
    
# custom error classes
class NOT_CALLABLE_ERROR(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)
        self.errors = errors