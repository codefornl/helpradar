# Install and run
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

this will generate the `helpradar.db` sqlite file. No sqlite3? Don't worry, you can upload the database to https://sqliteonline.com/ and view it there!

Read [bronnen](bronnen.md) for our roadmap of platforms to scrape

## Migrations
I chose this [Alembic](https://alembic.sqlalchemy.org/en/latest/) migrations framework because it allows for autogeneration of migrations 
based on diffs between classes and schema.

* If you pulled in new code that contains a database migration run: 'alembic upgrade head' from an actiated environment.
* If you changed or added model classes run: alembic revision --autogenerate -m "version suffix message"
* If a migration fails, just checkout the sqlite database. Because it will think it's in the previous state. 
So downgrading usually doesn't work then.
* Downgrading by the way can be done by 'alembic downgrade -n' where n is the amount of migrations you want to revert.
* Always test the downgrade before committing.
* Sqlite doesn't support a lot alter statement requiring changes to be made in 
[batch mode](https://alembic.sqlalchemy.org/en/latest/batch.html?highlight=batch%20mode) which moves and copies the whole table.

## Tests
Simply run pytest from the command line.

