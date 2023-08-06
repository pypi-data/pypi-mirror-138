# Subsalt

Subsalt is a synthetic datastore that makes sensitive datasets shareable. This library provides an interface for retrieving data from Subsalt tables for use in other applications.

## Installation

```
pip install subsalt
```

## Usage

**Note:** this library is currently in beta, and the interface may change significantly over time.

Retrieving data from Subsalt requires valid credentials. For access, contact the data owner or email `hello@getsubsalt.com`.

### Authentication

```python
client = subsalt.Client(
    client_id=os.getenv('SUBSALT_CLIENT_ID'),
    client_secret=os.getenv('SUBSALT_CLIENT_SECRET'),
)

# `client` can retrieve data on your behalf
```

### Retrieving data

```python
client = subsalt.Client(
    client_id=os.getenv('SUBSALT_CLIENT_ID'),
    client_secret=os.getenv('SUBSALT_CLIENT_SECRET'),
)

# Retrieve the first 50 records from model_id='2'
# You can find the appropriate model_id by looking up the dataset 
# at https://portal.getsubsalt.com.
client.get(model_id='2', limit=50)
```

### Retrieving data via SQL

Subsalt also supports a SQL-based interface. If you'd like to run a query on a Subsalt table, use a Postgres-compatible
library like [psycopg2](https://pypi.org/project/psycopg2/) and connect using the credentials available in the
[management portal](https://portal.getsubsalt.com).