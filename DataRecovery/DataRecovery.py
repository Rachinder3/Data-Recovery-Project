import os
import shutil
from logger.logger import Logger
from HuffmanCoding.HuffmanCoding import HuffmanCoding


class DataRecovery:
    __log_obj = Logger("logs\\Log.log") # log object

    def __init__(self, file_paths):

        # creating the staging folder, which stores all the files in one place
        if os.path.exists("staging\\"):
            shutil.rmtree("staging\\")
        # create staging folder
        os.mkdir("staging")

        for file in file_paths:
            file_name = file.split("\\")[-1]

            shutil.copyfile(file, "staging//" + file_name)

        #list storing the huffman tree object for each file
        self.huffman_trees = []

    def create_Backups(self, key1):
        try:
            """function that helps in creating the backup for each file"""
            # create backup folder

            key = 0
            for i in key1:
                key += ord(i)

            key = key % 256

            if os.path.exists("backups\\"):
                shutil.rmtree("backups\\")
            os.mkdir("backups")

            for index, file in enumerate(os.listdir("staging\\")):
                # iterate over each file to create its backup

                filename, file_extension = os.path.splitext(file)

                hc = HuffmanCoding("staging\\" + file)

                output_path = "backups\\" + "backup_" + filename

                hc.compress(output_path, key)

                self.huffman_trees.append(hc)

        except Exception as e:
            DataRecovery.__log_obj.add_log("Problem in create_Backups function")
            DataRecovery.__log_obj.add_log(str(e))

    def recover_files(self, key1):
        """function that helps in recovering data from backup files"""
        try:
            key = 0
            for i in key1:
                key += ord(i)

            key = key % 256

            # Create recovered files folder

            if os.path.exists("recovered_files//"):
                shutil.rmtree("recovered_files//")
            os.mkdir("recovered_files")

            # iterate over each backup file and recover data from it.
            for index, file in enumerate(os.listdir("backups\\")):
                filename, file_extension = os.path.splitext(file)

                filename = filename.split("backup_")[1]  # getting the filename


                # getting the huffman tree for this file
                hc = self.huffman_trees[index]

                output_path = "recovered_files//" + "recovered_" + filename

                hc.decompress("backups\\" + file, output_path, key) # recovering the file from the backup

            if os.path.exists("temp.bin"): # removing the extra created temp file
                os.remove("temp.bin")

        except Exception as e:
            DataRecovery.__log_obj.add_log("Problem in Recover Files function")
            DataRecovery.__log_obj.add_log(str(e))

