from logger.logger import Logger


class Cipher:
    """class implementing encrypt and decrypt functions"""

    __log_obj = Logger("logs\\Log.log")

    @staticmethod
    def encrypt_file(byte_array_data, key):
        try:

            for index, item in enumerate(byte_array_data):
                byte_array_data[index] = byte_array_data[index] ^ key  # doing XOR so that we can encrypt each bit

            Cipher.__log_obj.add_log("Encryption successful")
            return byte_array_data



        except Exception as e:
            Cipher.__log_obj.add_log("problem in encrypt_file function")
            Cipher.__log_obj.add_log(str(e))

    @staticmethod
    def decrypt_file(byte_array_data, key):
        try:

            for index, item in enumerate(byte_array_data):
                byte_array_data[index] = byte_array_data[index] ^ key

            Cipher.__log_obj.add_log("Decryption successful")
            return byte_array_data


        except Exception as e:
            Cipher.__log_obj.add_log("Problem in decryption file function")
            Cipher.__log_obj.add_log(str(e))
