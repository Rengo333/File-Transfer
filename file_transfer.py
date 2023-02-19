import logging
import os
import shutil
import time
from ftplib import FTP

import schedule

logging.basicConfig(filename='download.log', level=logging.INFO)

host = input('Please, enter ftp server host:\n')
user = input('Please, enter user name:\n')
password = input('Please, enter password:\n')
remote_dir = input('Please, enter directory address on ftp server:\n')
local_dir = input('Please, enter directory address on the local computer:\n')
destination = input('Please, enter the address on the internal network:\n ')


def download_files(user, password, remote_dir, local_dir, destination):
    '''
    It connects to an external FTP server, and retrieves a list of files in a specific directory.
    It checks if a local directory where the files will be saved exists, If not it raises an exception.
    It goes through the files on the FTP server, and downloads them to the local directory.
    Finally, it moves the files from the local directory to an internal network destination.
    '''

    try:
        # Connect to the FTP server
        ftp = FTP(host)
        ftp.login(user=user, passwd=password)

        # Log successful connection
        logging.info('The connection is established.')

        # Check if the local directory exists, if not create it
        if os.path.exists(local_dir) is not True:
            directory = input('Please, enter the name of the new folder:\n')
            parent_dir = input('Enter the path where you want to create the folder:\n')
            path = os.path.join(parent_dir, directory)
            os.mkdir(path)

        # Change the working directory on the FTP server
        ftp.cwd(remote_dir)

        # Retrieve a list of files in the directory
        files = ftp.nlst()

        # Iterate through the files, download and save to the local directory
        for file_name in files:
            logging.info(f'Downloading... {file_name}')
            ftp.retrbinary('RETR %s' % file_name,
                           open(os.path.join(local_dir, file_name), 'wb').write)
        # Close the FTP connection
        ftp.close()
    except Exception as e:
        logging.error(f'Error connecting to FTP host: {e}')

    try:
        # Moving downloaded files from a local directory to an internal network destination
        shutil.move(local_dir, destination)
        logging.info(f'{file_name} moved to {destination}')
    except Exception as e:
        logging.error(f'Error moving file: {e}')


def script_schedule(user, password, remote_dir, local_dir, destination):
    '''
    Script scheduled to run every day at 10:30.
    '''
    schedule.every().day.at("10:30").do(download_files,
                                        user=user,
                                        password=password,
                                        remote_dir=remote_dir,
                                        local_dir=local_dir,
                                        destination=destination)
    logging.info('Script is running...')


def main():
    script_schedule(user, password, remote_dir, local_dir, destination)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
