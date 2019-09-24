from wsgiref.simple_server import make_server


def default_wsgi_worker(process):
    httpd = make_server(process.host, int(process.port), process.app)
    # process.port = httpd.server_address[1]
    process.queue.put((process.pid, httpd.server_address[1]))
    httpd.serve_forever()