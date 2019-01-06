from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import sys
import threading
import re

from Adb_Handler import Adb_Handler as AdbHandler

class Server(BaseHTTPRequestHandler):
    verbose = False
    key = ''
    deviceId = ''
    adbHandler = AdbHandler

    def start(self, ip, port, key, deviceId, verbose):
        self.verbose = verbose
        self.key = key
        self.deviceId = deviceId
        print('Starting server...')
        server_address = (ip, port)
        self.httpd = HTTPServer(server_address, Server)
        thread = threading.Thread(target = self.httpd.serve_forever)
        thread.daemon = True
        thread.start()        
        print('Server started on: ' + ip + ':' + str(port))

    def stop(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        print('Server stopped')

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers() 

        print(self.headers['content-type'])

        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        
        if ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postVars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postVars = {}

        if bytes('key', 'utf8') in postVars:
            try:
                key = postVars[bytes('key', 'utf8')][0].decode('utf-8')
                msg = postVars[bytes('msg', 'utf8')][0].decode('utf-8')
                rec = postVars[bytes('rec', 'utf8')][0].decode('utf-8')
            except:
                message = '{ "status":"error_decoding_params" }'
                self.wfile.write(bytes(message, 'utf8'))
                return                
        else:
            message = '{ "status":"no_auth" }'
            self.wfile.write(bytes(message, 'utf8'))
            return

        if key == self.key:
            rule = re.compile(r'(^\+[0-9]{1,3}[0-9]{10,11}$)')
            if rule.search(rec): 
                if len(msg) == 0:
                    message = '{ "status":"EMPTY_MESSAGE" }'
                elif len(msg) > 160:
                    message = '{ "status":"MESSAGE_EXCEEDS_160_CHAR_LIMIT" }'
                else:
                    if (self.adbHandler.sendSms(AdbHandler, self.deviceId, rec, msg)):
                        message = '{ "status":"REQUEST_PROCESSED" }'
                    else:
                        message = '{ "status":"ERROR_PROCESSING_REQUEST" }'
            else:
                    message = '{ "status":"INVALID_RECEIVER" }'
        else:
            message = '{ "status":"WRONG_AUTH" }'

        self.wfile.write(bytes(message, 'utf8'))

        if self.verbose:
            print(postVars)
    
    def log_message(self, format, *args):
        if self.verbose:
            sys.stderr.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                            self.log_date_time_string(),
                            format%args))