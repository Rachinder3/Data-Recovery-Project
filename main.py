from DataRecovery.DataRecovery import DataRecovery

if __name__ == '__main__':
    file_paths = ['Input_files\\414982.jpg',
                  'Input_files\\Data Science.txt',
                  'Input_files\\input_mp3.mp3',
                  'Input_files\\results.pdf',
                  'Input_files\\sample video.mp4']

    dr = DataRecovery(file_paths) # creating the data recovery object

    # creating the backups
    backup_key = "abcde"

    dr.create_Backups(backup_key)

    # recovering files
    recover_key = "abcde"

    dr.recover_files(recover_key)



