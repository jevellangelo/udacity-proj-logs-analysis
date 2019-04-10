# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Internal reporting tool using the DB-API Psycopg2

import psycopg2
from unicodedata import *

DBNAME = "news"

def top_articles():
	"""Prints the top 3 articles in a sorted list"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()
	c.execute("""
			SELECT articles.title, COUNT(log.status) AS views
				FROM log, articles
				WHERE SUBSTRING(log.path, 10) = articles.slug
				AND log.status = '200 OK'
				GROUP BY articles.title
				ORDER BY views DESC
				LIMIT 3;
			""")
	top_3 = c.fetchall()
	conn.close()
	print('Most popular three articles of all time:')
	for row in top_3:
		print('  ' + u'\u2022' +  ' "%s" -- %s views' % row)

	print('\n')



def top_authors():
	"""Prints the top authors in a sorted list"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()
	c.execute("""
		SELECT authors.name, COUNT(articles.slug) AS views
			FROM articles, authors, log
			WHERE SUBSTRING(log.path, 10) = articles.slug
			AND authors.id = articles.author
			GROUP BY authors.name
			ORDER BY views DESC;
		""")
	most_popular = c.fetchall()
	conn.close()
	print('Most popular article authors of all time:')
	for row in most_popular:
		print('  ' + u'\u2022' + ' %s -- %s views' % row)

	print('\n')



def most_errors():
	"""Prints which days did more than 1% of requests lead to errors"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()

	c.execute("""
		SELECT to_char(date, 'FMMonth DD, YYYY'), percent
			FROM (
				SELECT errors.date,
				round((errors.errors::numeric/requests.all_requests::numeric)*100,2) AS percent
				FROM errors, requests
				WHERE errors.date = requests.date
				) AS foo
			WHERE percent > 1.0;
		""")

	most_errors = c.fetchall()
	# whitespace = ' '
	conn.close()
	print('The days with more than one percent of requests lead to errors:')
	for row in most_errors:
		# dates = u'\u2022' + ' %s -- %s views' % row
		print('  ' + u'\u2022' + ' %s -- %s views' % row)
		
	print('\n')


if __name__ == '__main__':
	top_articles()
	top_authors()
	most_errors()
	