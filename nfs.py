import os
import time
import logging

from configparser import ConfigParser
from prettytable import PrettyTable

LOG = logging.getLogger(__name__)


class Nfs(object):
    def __init__(self, local_dir, config_file):
        self.local_dir = local_dir
        LOG.debug('NFS runs in path: %s', self.local_dir)

        cfg = ConfigParser()
        cfg.read(config_file)

        cs = cfg.__getitem__('nfs')

        self.nfs_ip = cs.get('ip')
        self.nfs_dir = cs.get('dir')
        self.ignore = cs.get('ignore').replace(" ", "").split(',')

        table = PrettyTable()
        table.add_column('key', ['ip', 'dir', 'ignore'])
        table.add_column('value', [self.nfs_ip, self.nfs_dir, self.ignore])
        LOG.debug(table)

    def get_list(self):
        return self.scan_path()

    def mount(self):
        # Mount nfs
        LOG.debug(" Mounting nfs")

        if not os.path.isdir(self.local_dir):
            LOG.debug('%s does not exist, try to create', self.local_dir)
            os.makedirs(self.local_dir)

        while os.system("mount | grep " + self.local_dir) != 0:
            cmd = "sudo mount -t nfs " + self.nfs_ip + ":" + self.nfs_dir + " " + self.local_dir
            LOG.debug("run-cmd: %s", cmd)
            mount_return = os.popen(cmd).read()
            # Todo: 'popen' does not return if cmd error
            LOG.debug(mount_return)
            time.sleep(5)

    def scan_path(self):
        # 1. Find the root media directories
        LOG.debug(" Walking in path: %s", self.local_dir)

        raw_dirs = os.listdir(self.local_dir)
        dirs = list(set(raw_dirs) - set(self.ignore))
        LOG.debug("p1: %s", dirs)

        classifies = []
        for directory in dirs:
            abs_dir = self.local_dir + "/" + directory
            # LOG.debug(" Scan directory: " + abs_dir)
            if os.path.isdir(abs_dir):
                # LOG.debug(" New classify directory")
                classifies.append(abs_dir)

        LOG.debug("p2: %s", str(classifies))

        # 2. Get all the play contents
        contents = []
        for classify in classifies:
            ones = os.listdir(classify)
            for one in ones:
                contents.append((classify + "/" + one)[len(self.local_dir):])

        return contents
