__author__ = 'Administrator'
import os
import xml
#[pathsync settings]
#pssversion=1
#path1=F:\Blender\Character
#path2=H:\Blender\Character
#ignflags=0
#defbeh= 0 1 2 3 4
#       0 Bidirectional
#       1 Local -> Remote(do not delete missing files/folders)
#       2 Remote -> Local(do not delete missing files/folders)
#       3 Local -> Remote
#       4 Remote -> Local
#logpath=
#include=!*.blend1;!*.blend2;Dolores\*;Ezisa\*;
#throttlespd=1024
#throttle=0
#syncfolders=1

#config
mask_blend12 = '!*.blend1;!*.blend2;'
mask_krita = '!*.*~;'
beh = 3
#path config
path_office = 'F:\Blender\Character'
office_selector = {True: 'F:\\', False: 'G:\\'}
path_home = 'G:/Blender/'


class SyncInfo:
    def __init__(self, mask, beh, path):
        self.mask = mask
        self.beh = beh
        self.path = path


_S = SyncInfo
queue = [_S(mask_blend12 + mask_krita + 'Dolores\*;Ezisa\*;', beh, 'Blender\Character'),
         _S(mask_blend12 + mask_krita + '*;', beh, 'Scene\9'), ]


def is_office():
    return os.path.exists(path_office)


def open_pss(mask, path1, path2, beh=0, syncfolders=1):
    pss_setting = '[pathsync settings]\n' + \
                  'pssversion=1\n' + \
                  'path1={1}\n' + \
                  'path2={2}\n' + \
                  'ignflags=0\n' + \
                  'defbeh={3}\n' + \
                  'logpath=\n' + \
                  'include={0}\n' + \
                  'throttlespd=1024\n' + \
                  'throttle=0\n' + \
                  'syncfolders={4}\n'
    pss_setting = pss_setting.format(mask, path1, path2, beh, syncfolders)
    f = open('c:/tmp.PSS', 'w')
    f.write(pss_setting)
    f.close()
    print('write tmp.PSS')
    tmp_pss = 'c:\\tmp.PSS'
    #os.system('h:/pathsync.exe -loadpss c:\\tmp.PSS',)
    os.system('pathsync.exe -loadpss {0}'.format(tmp_pss))
    os.remove(tmp_pss)
    pass


def get_path(path_to_sync):
    #print is_office()
    #get path disk
    path1 = office_selector[is_office()] + path_to_sync
    #get path upan
    curdir = os.path.abspath('.')
    path2 = curdir + path_to_sync
    return path1, path2


def sync_queue():
    for idx in range(0, len(queue)):
        mask = queue[idx].mask
        beh = queue[idx].beh
        path = queue[idx].path
        path1, path2 = get_path(path)
        open_pss(mask, path1, path2, beh)
        print ("[Queue] " + str(idx) + ' end')
        pass
    print ("[Queue] fin")
    pass


if __name__ == '__main__':
    #path1, path2 = get_path(path_char)
    #print path1, path2
    sync_queue()
    #open_pss(mask_blend12 + 'Dolores\*;Ezisa\*;', path1, path2)
    pass