from app.utils.config_manager import ChangeSetting


class AllowFileMoving:

    def __init__(self):
        self.conf = ChangeSetting()

        self.main_path = "/work"

    def __check_input_source(self, src):

        list_src = self.conf.get_input_file_source()

        flag_src = False

        for src_DIR in list_src:
            if src_DIR == (self.main_path + src):
                flag_src = True

        return flag_src

    def __check_input_distination(self, dis):
        list_dis = self.conf.get_input_file_distination()

        flag_Dir = False

        for dis_DIR in list_dis:
            if dis_DIR == (self.main_path + dis):
                flag_Dir = True

        return flag_Dir

    def __check_output_source(self, src):

        list_src = self.conf.get_out_file_source()

        flag_src = False

        for src_DIR in list_src:
            if src_DIR == (self.main_path + src):
                flag_src = True

        return flag_src

    def __check_output_distination(self, dis):
        list_dis = self.conf.get_out_file_distination()

        flag_Dir = False

        for dis_DIR in list_dis:
            if dis_DIR == (self.main_path + dis):
                flag_Dir = True

        return flag_Dir

    def check_permition_path(self, src, dis):

        flag_cheking = -1

        if self.__check_input_source(src):
            if self.__check_input_distination(dis):
                flag_cheking = 0
            else:
                flag_cheking = 2
        elif self.__check_output_source(src):
            if self.__check_output_distination(dis):
                flag_cheking = 0
            else:
                flag_cheking = 2
        else:
            flag_cheking = 1

        return flag_cheking

