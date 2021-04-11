Create a virtualenv and Install the requirements using pip install -r requirements.txt.
After that run the main.py script.
Please check if SQLITE.EXE is in your system variables.
Download the SQLITE3 tool from https://www.sqlite.org/2021/sqlite-tools-win32-x86-3350400.zip

Test the API in Postman

Sample Request body 

For song
{"audioFileType":"song","audioFileMetadata":{"ID":1,"Name":"Sai","Duration":120}}

For Podcast
{"audioFileType":"podcast","audioFileMetadata":{"ID":1,"Name":"Flask Podcast","Duration":300, "Host":"Sai Pavan", Participants:""}}

For Audiobook
{"audioFileType":"audiobook","audioFileMetadata":{"ID":1,"Title":"Flask Beginner","Duration":300, "Author":"Sai Pavan", Narrator:"Red"}}