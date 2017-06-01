import os
import re
import logging
import hashlib
import socket
logger = logging.getLogger('scancardinfo')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('./scancardinfo.log')
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)s %(filename)s %(levelname)s %(processName)s %(threadName)s %(message)s')
fh.setFormatter(formatter)
allfiles = []
for root, dirs, files in os.walk('/home/'):
    for name in files:
        if(name.endswith(".log")):
            allfiles.append(os.path.join(root, name))
str = ""
for file in allfiles:
    f = open(file)
    iter_f = iter(f)
    for line in iter_f:
        matches = re.findall(r'(^|\D)(((6011|5610)(\d|\*){12,15})|((62|34|37|65|35|51|52|53|54|55|95)(\d|\*){14,17})|((4)(\d|\*){15,18}))($|\D)',line)
        if matches:
            #print(file)
            #print(line)
            m = hashlib.md5()
            m.update(line)
            md5str = m.hexdigest()
            ip = socket.gethostbyname(socket.gethostname())
            logger.addHandler(fh)
            logger.info('#XMDT#{path=' + file + ' md5=' + md5str + ' ip=' + ip + '}#XMDT#' + ' ' + line)
