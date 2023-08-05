# aqur1n-tools
Collection of modules for convenient work.

# Simple examples:
```python
from atools.basic import *
print(get_directory()) # Get the directory of the current file.
```
```python
from atools.path import Path

print(str(Path("exaples") + Path("test"))) # exaples\test
```
```python
from atools.sqlite3 import *

sql = sql("my name") # Initializes the class.
sql.connect("db\\my_db.db") # Connecting to db

sql.execute(f"CREATE TABLE IF NOT EXISTS my_table (test TEXT)", func=sql.commit) # Executes the query and calls the sql.commit function
```
You can see more on the wiki: [click](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
