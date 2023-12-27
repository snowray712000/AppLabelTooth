import gzip
import json
from flask import Response

def easy_response_text(text:str, statusCode=200, isGzip = True):
    '''text/plain'''
    data = text.encode()
    
    header = {
        'Content-Type': 'text/plain; charset=utf-8', 
        }
    
    if isGzip:
        data = gzip.compress(data)
        header['Content-Encoding'] = 'gzip'
    return Response(data, headers=header,status=statusCode)  
def easy_response_json(dict, statusCode=200, isGzip = True):
    '''application/json'''
    text = json.dumps(dict)
    data = text.encode()
    
    header = {
        'Content-Type': 'application/json; charset=utf-8',        
        }
    
    if isGzip:
        data = gzip.compress(data)
        header['Content-Encoding'] = 'gzip'

    return Response(data, headers=header,status=statusCode)
