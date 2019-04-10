-- Create views in news database for report_tool.py

CREATE VIEW requests AS
	-- SELECT REGEXP_REPLACE(to_char(log.time, 'Month DD, YYYY'),'\s+',' ') AS date,
	SELECT time::date AS date,
	COUNT(log.status) AS all_requests
	FROM log
	GROUP BY date
	ORDER BY date ASC;

CREATE VIEW errors AS
	-- SELECT REGEXP_REPLACE(to_char(log.time, 'Month DD, YYYY'),'\s+',' ') AS date,
	SELECT time::date AS date,
	COUNT(log.status) AS errors
	FROM log
	WHERE log.status <> '200 OK'
	GROUP BY date
	ORDER BY date ASC;