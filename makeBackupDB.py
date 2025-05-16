import shutil

source_path = 'hilbertDatabase.db'
backup_path = 'hilbertDatabase_backup.db'

shutil.copy2(source_path, backup_path)
print("Backup created successfully!")