from http.server import BaseHTTPRequestHandler

class LogEntryRequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP request to this hardware device. This is used to report 
    the hardware's status to clients. From this, clients can detect if there's 
    something wrong with the hardware.
    """

    OUTPUT_ENCODING = "utf-8"
    service_status = None

    @classmethod
    def update_service_status(cls, service_status):
        LogEntryRequestHandler.service_status = service_status

    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            
            output = bytes(
                LogEntryRequestHandler.service_status.__str__(), 
                LogEntryRequestHandler.OUTPUT_ENCODING)

            self.wfile.write(output)
        else:
            self.send_response(500)
