
import sys
from cgi import parse_qs, escape

sys.path.insert(0, '/var/www/schilder')

from render import render

def application(environ,start_response):   
    d = parse_qs(environ['QUERY_STRING'])
    response_body = render(d.get('text','Text fehlt')[0],
                           d.get('seed',[1])[0],
                           d.get('align','left')[0],
                           int(d.get('fillbackground','0')[0]),
                           float(d.get('linespacing','0')[0]),
                           float(d.get('rotation','1')[0])/10.0)

    # HTTP response code and message
    status = '200 OK'

    # These are HTTP headers expected by the client.
    # They must be wrapped as a list of tupled pairs:
    # [(Header name, Header value)].
    response_headers = [('Content-Type', 'image/png'),
                        ('Content-Length', str(len(response_body)))]

    # Send them to the server using the supplied function
    start_response(status, response_headers)

    # Return the response body.
    # Notice it is wrapped in a list although it could be any iterable.
    return [response_body]
