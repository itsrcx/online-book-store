# StoryKeeper

<b>First thing first</b>
<p>Create a virtual environment</p>
Run <code>pip install -r requirements.txt</code><br>

<b>To use mysql as db:</b>

- <p>uncomment: mysql databse in <code>settins.py</code> and comment sqlite3 database</p>
- <p>add a <code>my.cnf</code> file in following format:<br>
  <code>[client]<br>
  database = DB_NAME<br>
  host = localhost<br>
  user = DB_USER<br>
  password = DB_PASSWORD<br>
  default-character-set = utf8</code>
  </p>

- <p>add path to your <code>my.cnf</code> file in:<br>
  <code>'read_default_file': '/path/to/my.cnf'</code>
  </p>

-  <p>run <code>makemigrations</code> and <code>migrate</code> commands in terminal</p>
-  <p>create a <code>superuser</code> and add data manually to MySql DB</p>

-  <p>run management command <code>python manage.py import_csv_data patch/to/csv</code></p>
   <p>csv provided in <code>src</code></p>

<b>Use of Google Auth</b> 
-  if you want to use google authentecation: 
    - goto: https://developers.google.com/identity/protocols/oauth2 
    - login console and create project
    - put your client_id and secret in<code>SOCIALACCOUNT_PROVIDERS in setting.py</code>


-  other imp. stuff
    - you can change session time from <code>member.forms</code> to play with
    - fork if you want to contribute.