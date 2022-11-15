To run script type in Windows cnd or PowerShell: python <your-path>/main.py
Instead of <your-path> place your own path to directory where main.py is stored.
AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION_NAME) should be saved in environmental variables.


config_data/main_config.json contains 'delete_flag', if it's set to 'True' then raw files in 'raw_data_dir' directory
will be deleted without moving to 'dir_to_move' directory where raw files are moved by default.

It's allowed to set paths to files and directories for Windows OS with the forward slash ('/').
Add all prefixes and folder names to config files only ended with forward slash '/'.