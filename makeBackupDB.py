import shutil
import os.path as op
import os
import datetime

def create_backup_of_DB(active_database) :
    backup_dir_name = "db_backups\\"
    source_db = active_database

    current_path = op.dirname(__file__)
    active_db_path = op.join(current_path,source_db)
    backup_dir = op.join(current_path,backup_dir_name)

    if not op.isdir(backup_dir) : # Creates backup directory if one does not exists
        os.mkdir(backup_dir)

    current_date = datetime.date.today()

    backup_path = op.join(backup_dir,source_db[:-3]+"("+str(current_date)+").db")

    if not op.isfile(backup_path) :
        shutil.copy2(active_db_path, backup_path)
        print("Backup successfully created!")
    else :
        print("Backup not created, already exists.")