# online-book-store (StoryKeeper)
<h3>First thing first</h3>
<p>Create a virtual environment</p>
Run <code>pip install requirements.txt</code>
<h3>To use mysql as db:<h3>
<ul>
  <li><p>uncomment: mysql databse in <code>settins.py</code> and comment sqlite3 database</p>
    <p>add a <code>my.cnf</code> file in following format:<br>
    <code>[client]
    database = DB_NAME
    host = localhost
    user = DB_USER
    password = DB_PASSWORD
    default-character-set = utf8</code>
    </p>
  </li>
  <li> 
    <p>add path to your <code>my.cnf</code> file in:<br>
    <code>'read_default_file': '/path/to/my.cnf'</code>
    </p>
  </li>
  <li>
    <p>run <code>makemigrations</code> and <code>migrate</code> commands in terminal</p>
    <p>create a <code>superuser</code> and add data manually to MySql DB</p>
  </li>
  <li>
    <p>run management command <code>python manage.py import_csv_data patch/to/csv</p>
    <p>csv provided in <code>src</code></p>
  </li>
</ul>

