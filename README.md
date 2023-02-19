# File Transfer
Program connects to an external FTP server, and retrieves a list of files in a specific directory.
Program checks if a local directory where the files will be saved exists, If not it raises an exception.
Program goes through the files on the FTP server, and downloads them to the local directory.
Finally, it moves the files from the local directory to an internal network destination.
It is scheduled to run every day at 10:30.

# Log
Program creates a log file to save the data about file transfers.

# Requirements
Additional libraries are required to install.
It is recommended to use a new virtual envinronment.
Use this command in terminal to install requirements from requirements.txt.
>pip install -r requirements.txt