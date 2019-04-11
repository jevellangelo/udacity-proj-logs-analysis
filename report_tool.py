#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Internal reporting tool using the DB-API Psycopg2

import psycopg2
from unicodedata import *

DBNAME = "news"

# Database query for top_articles: 
#   What are the three most popular articles of all time?
request_articles = """SELECT articles.title, COUNT(log.status) AS views
            FROM log, articles
            WHERE SUBSTRING(log.path, 10) = articles.slug
            AND log.status = '200 OK'
            GROUP BY articles.title
            ORDER BY views DESC
            LIMIT 3;
            """

# Database query for top_authors: 
#   Who are the most popular article authors of all time?
request_authors = """SELECT authors.name, COUNT(articles.slug) AS views
            FROM articles, authors, log
            WHERE SUBSTRING(log.path, 10) = articles.slug
            AND authors.id = articles.author
            GROUP BY authors.name
            ORDER BY views DESC;
            """

# Database query for most_errors: 
#   On which days did more than 1% of requests lead to errors?
request_errors = """SELECT to_char(date, 'FMMonth DD, YYYY'), percent
            FROM (
                SELECT errors.date,
                round((errors.errors::numeric/requests.all_requests::numeric)*100,2)
                AS percent
                FROM errors, requests
                WHERE errors.date = requests.date
                ) AS foo
            WHERE percent > 1.0;
            """


# Query data from database, open and close the connection
def sql_query(sql_request):
    try:
        conn = psycopg2.connect(database=DBNAME)
        c = conn.cursor()
        # Print PostgreSQL Connection properties for debugging
        # print(conn.get_dsn_parameters(),"\n")
        c.execute(sql_request)
        results = c.fetchall()
    except psycopg2.DatabaseError, e:
        print("Error connecting to {} database.\nError: {}".format(DBNAME, e))
    finally:
        if conn is not None:
            conn.close()
            return results


def top_articles():
    """Prints the top 3 articles in a sorted list"""
    top_3 = sql_query(request_articles)
    print('Most popular three articles of all time:')
    for row in top_3:
        print('  ' + u'\u2022' + ' "%s" -- %s views' % row)
    print('\n')


def top_authors():
    """Prints the top authors in a sorted list"""
    most_popular = sql_query(request_authors)
    print('Most popular article authors of all time:')
    for row in most_popular:
        print('  ' + u'\u2022' + ' %s -- %s views' % row)
    print('\n')


def most_errors():
    """Prints which days did more than 1% of requests lead to errors"""
    most_errors = sql_query(request_errors)
    print('The days with more than one percent of requests lead to errors:')
    for row in most_errors:
        print('  ' + u'\u2022' + ' %s -- %s views' % row)
    print('\n')


if __name__ == '__main__':
    top_articles()
    top_authors()
    most_errors()
