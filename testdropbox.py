import dropbox
from dropbox.files import WriteMode

dbx = dropbox.Dropbox(open("keys/access_dropbox.txt", "r").read())

print(dbx.users_get_current_account())

with open("C:\\Users\\Shandy\\Projects\\PycharmProjects\\InventoryStore\\backup\\db\\default-SHANDY-DELL-G3-2021-07-26-152115.dump", 'rb') as f:
    dbx.files_upload(f.read(), "/backup/db/test.dump")