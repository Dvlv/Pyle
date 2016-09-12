import sys
import time
import os
import subprocess
from jsmin import jsmin
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

def getOutput(command):
    output = subprocess.Popen([command], shell="True", stdout=subprocess.PIPE).stdout
    return output.read().decode('utf-8').split('\n')


class LessCompiler(FileSystemEventHandler):
    def on_modified(self, event):
        cmdLess = 'lessc assets/less/main.less assets/css/main.css'
        print event.src_path
#        print 'calling %s' % cmdLess
#        print getOutput(cmdLess)
#        with open('assets/js/custom_scripts.js') as js_file:
#            miniJs = jsmin(js_file.read(), quote_chars="'\"`")
#        cmdJs = 'echo %s > assets/js/custom_scripts.min.js' % miniJs
#        print getOutput(cmdJs)        

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LessCompiler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
