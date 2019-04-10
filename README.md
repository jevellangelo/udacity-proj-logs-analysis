# PROJECT: Logs Analysis

You've been hired onto a team working on a newspaper site. The user-facing newspaper site frontend itself, and the database behind it, are already built and running. You've been asked to build an **internal reporting tool** that will use information from the database to discover what kind of articles the site's readers like.


## Prepare the Software and Data
To start on this project, you'll need database software (provided by a Linux virtual machine) and the data to analyze.

### Install VirtualBox
VirtualBox is the software that actually runs the virtual machine. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) Install the platform package for your operating system. You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it; Vagrant will do that.

Currently (October 2017), the supported version of VirtualBox to install is version 5.1. Newer versions do not work with the current release of Vagrant.

**Ubuntu users:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center instead. Due to a reported bug, installing VirtualBox from the site may uninstall other software you need.

### Install Vagrant
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html) Install the version for your operating system.

### The Virtual Machine
This project makes use a Linux-based virtual machine (VM) with the following preinstalled software:
- Python 2.7.12
- psql (PostgreSQL) 9.5.16

This will give you the PostgreSQL database and support software needed for this project. If you have used an older version of this VM, you may need to install it into a new directory.

You can bring the virtual machine online with the command ```vagrant up```. Then log into it with ```vagrant ssh```.

### Download the data
Next, [download the data here.](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) You will need to unzip this file after downloading it. The file inside is called ```newsdata.sql```. Put this file into the ```vagrant``` directory, which is shared with your virtual machine.

### Load the data into PostgreSQL
To build the reporting tool, you'll need to load the site's data into your local database using the ```psql``` command

To load the data, ```cd``` into the ```vagrant``` directory and use the command:
```psql -d news -f newsdata.sql```

Here's what this command does:

- ```psql``` — the PostgreSQL command line program
- ```-d news``` — connect to the database named news which has been set up for you
- ```-f newsdata.sql``` — run the SQL statements in the file newsdata.sql

Running this command will connect to your installed database server and execute the SQL commands in the downloaded file, creating tables and populating them with data.


### Explore the data
The database includes three tables:

The ```authors``` table includes information about the authors of articles.
```
                           Table "public.articles"
 Column |           Type           |                       Modifiers            
--------+--------------------------+-------------------------------------------------------
 author | integer                  | not null
 title  | text                     | not null
 slug   | text                     | not null
 lead   | text                     |
 body   | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('articles_id_seq'::regclass)
Indexes:
    "articles_pkey" PRIMARY KEY, btree (id)
    "articles_slug_key" UNIQUE CONSTRAINT, btree (slug)
Foreign-key constraints:
    "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```

The ```articles``` table includes the articles themselves.
```                  Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```

The ```log``` table includes one entry for each time a user has accessed the site.
```
                                  Table "public.log"
 Column |           Type           |                    Modifiers               
--------+--------------------------+--------------------------------------------------
 path   | text                     |
 ip     | inet                     |
 method | text                     |
 status | text                     |
 time   | timestamp with time zone | default now()
 id     | integer                  | not null default nextval('log_id_seq'::regclass)
Indexes:
    "log_pkey" PRIMARY KEY, btree (id)
```

### Create the views for use with the report_tool.py
```
psql -d news -f create_views.sql
```
```
CREATE VIEW requests AS
	SELECT time::date AS date,
	COUNT(log.status) AS all_requests
	FROM log
	GROUP BY date
	ORDER BY date ASC;
```
```
CREATE VIEW errors AS
	SELECT time::date AS date,
	COUNT(log.status) AS errors
	FROM log
	WHERE log.status <> '200 OK'
	GROUP BY date
	ORDER BY date ASC;
```

## Run the code
After loading the data into the database, run the code!
```
python report_tool.py
```