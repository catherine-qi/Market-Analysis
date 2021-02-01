CREATE TABLE market_statistic (
	date_value DATE,
	data_type CHAR(80),
	close_value FLOAT,
	ln_index FLOAT,
	ln_diff FLOAT,
	ln_sum FLOAT,
	exponential_moving_average FLOAT,
	standard_deviation CHAR(80),
	upper_standard_deviation CHAR(80),
	lower_standard_deviation CHAR(80),
	upper_band_limit CHAR(80),
	lower_band_limit CHAR(80),
	PRIMARY KEY(date_value, data_type)
)

DROP TABLE market_statistic

SELECT *
	FROM market_statistic