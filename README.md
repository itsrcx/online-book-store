# online-book-store
<h3>To use mysql as db:<h3>
<p>uncomment: mysql databse in <code>settins.py</code> and comment sqlite3 database</p>
<p>add a <code>my.cnf</code> file in followinf format:<br>
<code>[client]
database = DB_NAME
host = localhost
user = DB_USER
password = DB_PASSWORD
default-character-set = utf8</code>
</p>
<p>add path to your <code>my.cnf</code> file in:<br>
<code>'read_default_file': '/path/to/my.cnf'</code>
</p> 
<p>run <code>makemigrations</code> and <code>migrate</code> commands in terminal</p>
