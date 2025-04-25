import os
import sys
import time
from datetime import datetime

from nebule import nod_check_nid, blk_generate, blk_sign


class Robot:
    SERVER_EID_FILE = 'e'
    RID_TIMESTAMP = 'e87d82829a2a4e6ba055e1f09a975398e1a89b434e99d6e75f34ff87461086c71867.none.272'
    BH = 'nebule:link/2:0'
    loop = False
    eid = ''
    timestamp = ''
    current_date = ''

    def get_args(self):
        if '-l' in sys.argv:
            self.loop = True

    def get_entity(self):
        if not os.path.isfile(self.SERVER_EID_FILE):
            print(f"no server entity file {self.SERVER_EID_FILE}")
            os._exit('2')
        try:
            with open(self.SERVER_EID_FILE) as file:
                self.eid = file.read().strip()
        except Exception as e:
            print(f"cannot read server entity file {self.SERVER_EID_FILE}: {e}")
            os._exit(2)
        if not nod_check_nid(nid=self.eid):
            print(f"invalid server entity on file {self.SERVER_EID_FILE}")
            os._exit(2)
        print(f"eid={self.eid}")

    def get_time(self):
        d = datetime.now()
        self.timestamp = d.strftime('%s')
        print(f"timestamp={self.timestamp}")
        self.current_date = d.strftime('0%Y%m%d%H%M%S')
        print(f"date={self.current_date}")

    def get_link(self):
        s = len(self.timestamp)*4
        bh_bl = blk_generate(f"0>{self.current_date}", 'f', self.RID_TIMESTAMP, f"{self.timestamp}.none.{s}")
        return blk_sign(bh_bl)

    def __init__(self):
        self.get_args()
        self.get_entity()
        self.get_time()
        link = self.get_link()
        while True:
            print(f"link={link}")
            if not self.loop:
                break
            time.sleep(60)


# OK, now play...
if __name__ == '__main__':
    try:
        Robot()
    except Exception as e:
        print(f"Error main: {e}")
        os._exit(1)
