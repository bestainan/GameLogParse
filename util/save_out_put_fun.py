#coding:utf-8
import os
import cPickle
from util.logs_out_path_of_parse import get_parse_path
class Los_Class():
    def __init__(self,cur_data,dir_name,file_name):
        self.cur_data = cur_data
        self.dir_name = dir_name
        self.file_name = file_name
        self.LOCAL_LOG_PATH_NAME_LST, self.OUT_PUT_PATH_LST = get_parse_path(self.cur_data)
    def save_file(self,lst):

        for path_key,path_value in self.OUT_PUT_PATH_LST.items():
            try:
               os.mkdir(path_value.format(cur_date = str(self.cur_data),
                                          use_path = self.dir_name) )
            except:
                pass
            path = path_value + str(self.cur_data) +os.sep+ self.dir_name + os.sep + self.file_name
            with open(path,'w') as f:
                cPickle.dump(lst,f)

    def save_one_server(self,lst,server_id):
        path_value = self.OUT_PUT_PATH_LST[server_id]
        try:

            os.mkdir(path_value.format(cur_date = str(self.cur_data),
                                      use_path = self.dir_name))

        except:
            pass
        path = path_value.format(cur_date = str(self.cur_data),
                                 use_path = self.dir_name) + self.file_name
        with open(path,'w') as f:
            cPickle.dump(lst,f)

