from cgi import parse_qs, escape

html="""
<html>
<body>
   <form method="post" action="">
        <p>
           Message: <input type="text" name="msg" value="%(msg)s">
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Message: %(msg)s<br>
    </p>
</body>
</html>
"""
def hello(environ, start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    body = 'Hello, world!'
    start_response(status, headers)
    return [ body ]

def get_params(environ, start_response):
	d = parse_qs(environ['QUERY_STRING'])

	res_template = "{0}: {1} </br>"
	response = "GET params: </br>"
	for key, value in d.items():
		response += res_template.format(escape(key), [escape(x) for x in value])

	start_response("200 OK", [
		("Content-Type", "text/html"),
		("Content-Length", str(len(response)))
		])
	return iter([response])

def post_params(environ, start_response):
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    msg = d.get('msg', [''])[0]
    msg = escape(msg)
    response_body = html % { 
        'msg': msg or 'Empty',
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]
