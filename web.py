import os
import urllib2, urllib

from flask import Flask, request, make_response
app = Flask(__name__)

app.debug = True

if os.environ.get('PROXIMO_URL', '') != '':
  proxy  = urllib2.ProxyHandler({'http': os.environ.get('PROXIMO_URL', '')})
  auth   = urllib2.HTTPBasicAuthHandler()
  opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
  urllib2.install_opener(opener)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catchall(path):
  conn = urllib2.urlopen('http://httpbin.org/%s' % path)
  resp = make_response(conn.read())
  for header in conn.headers:
    resp.headers[header] = conn.headers[header]
  return resp

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)
