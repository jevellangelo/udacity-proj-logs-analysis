# -*- coding: utf-8 -*-
# python 2

# Internal reporting tool using the DB-API Psycopg2

import psycopg2
from unicodedata import *

DBNAME = "news"

def top_articles():
	"""Prints the top 3 articles in a sorted list"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()
	c.execute(
		"SELECT articles.title, COUNT(log.status) AS views \
			FROM log \
			JOIN articles \
			ON log.path LIKE CONCAT('%', articles.slug, '%') \
			WHERE log.status LIKE '200%' \
			GROUP BY articles.title \
			ORDER BY views DESC \
			LIMIT 3;")
	top_3 = c.fetchall()
	conn.close()
	print('Most popular three articles of all time:')
	for row in top_3:
		print('  ' + u'\u2022' +  ' "%s" -- %s views' % row)

	print('\n')


top_articles()

def top_authors():
	"""Prints the top authors in a sorted list"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()
	c.execute(
		"CREATE VIEW authorSlug as \
			SELECT authors.name, articles.slug \
			FROM articles, authors \
			WHERE authors.id = articles.author;")
	c.execute(
		"SELECT authorSlug.name, COUNT(log.status) AS views \
			FROM authorSlug, log JOIN articles \
			ON log.path LIKE CONCAT('%', articles.slug, '%') \
			WHERE log.status LIKE '200%' \
			GROUP BY authorSlug.name \
			ORDER BY views desc;")
	most_popular = c.fetchall()
	conn.close()
	print('Most popular article authors of all time:')
	for row in most_popular:
		print('  ' + u'\u2022' + ' %s -- %s views' % row)

	print('\n')

top_authors()

def most_errors():
	"""Prints which days did more than 1% of requests lead to errors"""
	conn = psycopg2.connect(database=DBNAME)
	c = conn.cursor()
	c.execute(
		"CREATE VIEW no_error AS \
			SELECT REGEXP_REPLACE(to_char(log.time, 'Month DD, YYYY'),'\s+',' ') AS date, \
			count(log.status) AS views \
			FROM log \
			WHERE (log.status = '200 OK'::text) \
			GROUP BY date \
			ORDER BY date DESC;")
	c.execute(
		"CREATE VIEW error AS \
			SELECT REGEXP_REPLACE(to_char(log.time, 'Month DD, YYYY'),'\s+',' ') AS date, \
			count(log.status) AS no_views \
			FROM log \
			WHERE (log.status <> '200 OK'::text) \
			GROUP BY date \
			ORDER BY date DESC;")
	c.execute(
		"CREATE VIEW all_views AS \
			SELECT error.date, \
			no_error.views, \
			error.no_views \
			FROM (error \
			JOIN no_error ON ((error.date = no_error.date))) \
			ORDER BY error.no_views DESC;")
	c.execute(
		"SELECT date, round(percent::numeric,2) \
			FROM \
				(SELECT date, (no_views/views::float)*100 AS percent \
				FROM all_views) AS foo \
				WHERE percent > 1;")
	errors = c.fetchall()
	whitespace = ' '
	conn.close()
	print('The days with more than one percent of requests lead to errors:')
	for row in errors:
		dates = u'\u2022' + ' %s -- %s views' % row
		print('  ' + whitespace.join(dates.split()))
		
	print('\n')


most_errors()