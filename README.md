# DDL Shenanigans

I am a lazy programmer and I hate mucking about with SQL DDL with various
databases. I like to work with SQLite as much as possible and then switch
to a more full-featured database like PostgreSQL when I need the extra
capabilities.

This repo contains a demonstration of how I combine SQLAlchemy and Alembic
to manage my database schema and generate DDL.

## Example usage

Create an initial SQLite migration:

```shell
DATABASE_URL="sqlite:///foo.db" rye run alembic revision --autogenerate -m "ignore"
```

Spit out the SQL:

```shell
DATABASE_URL="sqlite:///foo.db" rye run alembic upgrade head --sql
```

Then I just change the database URL to another driver (e.g. postgres) and run
the commands again after deleting the existing migrations.

```shell
rm src/ddl_shenanigans/migrations/versions/*.py
DATABASE_URL="postgresql://somepghost:5432/somedb" rye run alembic ...
```

## Replicating this demo repo with Rye

Note: If you just want to use the repo as a reference you can skip this. Read on
to see details of what I change from the generic init templates.

### Rye install

I use [asdf](https://asdf-vm.com/) to manage as many tools as I can. I plan to
experiment with [Mise](https://mise.jdx.dev/) in the future. (TODO: Try mise)

```shell
asdf plugin add rye
asdf install rye latest
```

### Python init

```shell
rye init --py 3.12.3
rye add sqlite alembic
rye sync
```

### Alembic init

```shell
cd src/ddl_shenanigans
alembic init migrations
mv alembic.ini ../..
cd ../..
```

Edit `alembic.ini`:

```diff
# alembic.ini
...
- script_location = migrations
+ script_location = src/ddl_shenanigans/migrations  
...
- sqlalchemy.url = driver://user:pass@localhost/dbname
...
```

### SQLAlchemy setup

Create a file to create the database connection and session from an environment
variable.

```python
# src/ddl_shenanigans/dbx.py
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(os.environ["DATABASE_URL"])
Session = sessionmaker(bind=engine)

def connect():
    return Session()
```

Edit the migration `env.py` to use the session:

```diff
# alembic/env.py
...
+ from ddl_shenanigans.dbx import engine
+ from ddl_shenanigans.models import Base
...
- target_metadata = None
+ target_metadata = Base.metadata
...
-    url = config.get_main_option("sqlalchemy.url")
-    context.configure(
-        url=url,
+    context.configure(
+        connection=engine.connect(),
...
-    connectable = engine_from_config(
-        config.get_section(config.config_ini_section, {}),
-        prefix="sqlalchemy.",
-        poolclass=pool.NullPool,
-    )
-
-    with connectable.connect() as connection:
+    with engine.connect() as connection:
...
```
