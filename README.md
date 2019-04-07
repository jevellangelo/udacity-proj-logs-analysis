# PROJECT: Logs Analysis

You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.

### Load the data into PostgreSQL
```
psql -d news -f news data.sql
```

### Connect to database 
Using the psycopg2 DB-API tool, connect to the news database. 
```
db = psycopg2.connect("dbname=news")
```

### Run the code
After loading the data into the database, run the code!
```
python report_tool.py
```