def simple_app(environ, start_response):
    from urllib.parse import parse_qs
    import json

    try:
        method = environ['REQUEST_METHOD']
        print(f"Request method: {method}")

        if method == 'GET':
            params = parse_qs(environ['QUERY_STRING'])
            print(f"GET params: {params}")
        elif method == 'POST':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
            except (ValueError):
                request_body_size = 0
            request_body = environ['wsgi.input'].read(request_body_size)
            params = parse_qs(request_body.decode('utf-8'))
            print(f"POST params: {params}")
        
        response_body = json.dumps({k: v for k, v in params.items()})
        print(f"Response body: {response_body}")

        status = '200 OK'
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]
        
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]

    except Exception as e:
        print(f"Error: {e}")
        status = '500 Internal Server Error'
        response_body = json.dumps({'error': str(e)})
        response_headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body.encode('utf-8')]

