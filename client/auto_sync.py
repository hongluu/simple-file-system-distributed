# import time module, Observer, FileSystemEventHandler 
import time 
from watchdog.observers import Observer 
import watchdog.events 
import time 
import os
import rpyc
import logging
logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)
class OnMyWatch: 
    # Set the directory on watch 
    watchDirectory = "./data"
    
    def __init__(self): 
        self.observer = Observer()
         
  
    def run(self): 
        con=rpyc.connect("master",port=2131)
        master=con.root.Master()
        event_handler = Handler(master) 
        self.observer.schedule(event_handler, path=self.watchDirectory, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(100) 
        except: 
            self.observer.stop() 
            print("Observer Stopped") 
  
        self.observer.join()
  
class Handler(watchdog.events.PatternMatchingEventHandler): 
    def __init__(self,master): 
        self.master =master
        # Set the patterns for PatternMatchingEventHandler 
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.txt'], 
                                                             ignore_directories=True, case_sensitive=False)


    def send_to_data_node(self,block_uuid,data,minions):
        LOG.info("sending: " + str(block_uuid) + str(minions))
        minion=minions[0]
        minions=minions[1:]
        host,port=minion
        con=rpyc.connect(host,port=port)
        minion = con.root.Minion()
        minion.put(block_uuid,data,minions)

    def put_to_data_node(self,master,source,dest):
      LOG.debug("Update file % s to Date Node." % dest) 
      size = os.path.getsize(source)
      blocks = master.write(dest,size)
      with open(source) as f:
        for b in blocks:
            data = f.read(master.get_block_size())
            block_uuid=b[0]
            minions = [master.get_minions()[_] for _ in b[1]]
            self.send_to_data_node(block_uuid,data,minions)
  
    def get_file_name(self, file_path):
        if(file_path == None and file_path == ""):
            return ""
        file_path_splits = file_path.split("/")
        len_file_path = len(file_path_splits)
        if(len_file_path == 0):
            return file_path
        else:
            return file_path_splits[len_file_path -1]
    def on_created(self, event): 
        self.put_to_data_node(self.master,event.src_path,event.src_path)
  
    def on_modified(self, event): 
        file_path = event.src_path;
        file_name = self.get_file_name(file_path)
        self.put_to_data_node(self.master,file_path,file_name) 
            
              
  
if __name__ == '__main__': 
    watch = OnMyWatch() 
    watch.run() 