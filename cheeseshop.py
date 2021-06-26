'''
The Cheeseshop Application.
'''
import socket
import logging
from pathlib import Path
 
from flask import Flask
from flask import json
  
STATUS_OK = 200
  
APP = Flask(__name__)
 
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)
namespace = None
  
@APP.route('/', methods=['GET'])
def get_status():
    '''
    Gets the status and health of the Cheeseshop service.
    '''
    global namespace
 
    if not namespace:
      # namespace
      ns_file = Path("/var/run/secrets/kubernetes.io/serviceaccount/namespace")
      if ns_file.is_file():
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as afile:
          namespace = afile.read()
      else:
          namespace = "i-am-not-a-k8s-namespace"
 
    response_message = "cheeseshop pod %s with (%s) in %s is OK" % (hostname, hostip, namespace)
 
    APP.logger.info(response_message)
    return APP.response_class(response=json.dumps({'msg': response_message}),
                              status=STATUS_OK,
                              mimetype='application/json')
