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
  
@APP.route('/v1/status', methods=['GET'])
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
  
def setup_logging():
    wlog = logging.getLogger('werkzeug')
    wlog.disabled = True
    APP.logger.handlers = []
    APP.logger.addHandler(logging.StreamHandler())
    APP.logger.setLevel(logging.DEBUG)
 
def _main():
    setup_logging()
 
    # Note that for host portion, use of localhost, 127.0.0.1 or leaving it unspecified will
    # likely result in your container not only being unable to respond to health checks
    # but also inhibit traffic flow from Kuberentes Services networking layer into the container.
    APP.logger.info("cheeseshop pod is using address {}:8080 for server socket binding".format(hostip))
    APP.run(host=hostip, port=8080)
  
if __name__ == '__main__':
    _main()
