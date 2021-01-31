#Catherine Qi

from configparser import ConfigParser
import numpy
import pandas
import pyodbc

#All calculations are based on Close values
class Market_Analysis:

	#all Config variables: BKX path, GSPC path, SOX path, server, database, table_name, A, B, C, D, E

	global connection
	global cursor
	global BKX
	global GSPC
	global SOX
	global server
	global database
	global table_name
	global data_types
	global all_df
	global a
	global b
	global c
	global d
	global e

	config = ConfigParser()
	config.read('config.ini')

	#csv file path locations
	BKX = pandas.read_csv(filepath_or_buffer=config['CSV FILES']['BKX'])
	GSPC = pandas.read_csv(filepath_or_buffer=config['CSV FILES']['GSPC'])
	SOX = pandas.read_csv(filepath_or_buffer=config['CSV FILES']['SOX'])

	server = config['USER']['server']
	database = config['USER']['database']	
	table_name = config['USER']['table_name']

	data_types = ['BKX', 'GSPC', 'SOX']
	all_df = [BKX, GSPC, SOX]

	#variables that make up various parameters such as days and multiplier
	a = int(config['VARIABLES']['a'])
	b = int(config['VARIABLES']['b'])
	c = int(config['VARIABLES']['c'])
	d = int(config['VARIABLES']['d'])
	e = int(config['VARIABLES']['e'])

	connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
								SERVER=' + server + ';\
								DATABASE=' + database +';\
								Trusted_Connection=yes;')
	cursor = connection.cursor()

	#inserts statistics into database; need all other function calls made before insert_stat(df) is called
	def insert_stat(df):
		stat_array = []
		df_name = [x for x in globals() if globals()[x] is df][0]
		for i in range(len(df.index)):
			stat_array.append([df.Date.values[i],df_name,df.Close.values[i],df.ln_Close.values[i],df.Diff_of_ln_Close_and_ln_GSPC.values[i],
							  df.Sum_of_ln_Close_and_ln_GSPC.values[i], df.EWMA.values[i], df.Rolling_Standard_Deviation.values[i], df.Upper_Standard_Deviation_Bands.values[i],
							  df.Lower_Standard_Deviation_Bands.values[i], df.Upper_Band_Limit.values[i], df.Lower_Band_Limit.values[i]])
		for index, row in enumerate(stat_array):
			if (str(row[2]) != 'nan'):
				insert_query = 'INSERT INTO ' + table_name + ' (date_value, data_type, close_value, ln_index, ln_diff, ln_sum, exponential_moving_average, standard_deviation, \
																upper_standard_deviation, lower_standard_deviation, upper_band_limit, lower_band_limit) VALUES(\'' + row[0] + '\',\'' + \
																str(row[1]) + '\',\'' + str(row[2]) + '\',\'' + str(row[3]) + '\',\'' + str(row[4]) + '\',\'' + str(row[5]) + '\',\'' + \
																str(row[6]) + '\',\'' + str(row[7]) + '\',\'' + str(row[8]) + '\',\'' + str(row[9]) + '\',\'' + str(row[10]) + '\',\'' + \
																str(row[11]) + '\');'
				print(insert_query)
				cursor.execute(insert_query)
		connection.commit();

	#calculates ln(index)
	def ln(df):
		df['ln_Close'] = numpy.log(df['Close'])
	
	#calculates ln(index)-ln(GSPC)
	def ln_diff(df):
		df['Diff_of_ln_Close_and_ln_GSPC'] = numpy.log(df['Close']) - numpy.log(GSPC['Close'])

	#calculates ln(index)+ln(GSPC)
	def ln_sum(df):
		df['Sum_of_ln_Close_and_ln_GSPC'] = numpy.log(df['Close']) + numpy.log(GSPC['Close'])

	#calculates exponential moving average of rolling x days
	def ema(df,days):
		df['EWMA'] = df['Close'].ewm(span=days, adjust=False).mean()

	#calculates standard deviation of rolling x days
	def rolling_standard_deviation(df,days):
		df['Rolling_Standard_Deviation'] = df['Close'].rolling(window=days).std()

	#calculates simple moving average of x days plus standard deviation times multiplier
	def upper_standard_deviation(df,days,multiplier):
		df['Upper_Standard_Deviation_Bands'] = df['Close'].rolling(window=days).mean() + df['Close'].rolling(window=days).std() * multiplier

	#calculates simple moving average of x days minus standard deviation times multiplier
	def lower_standard_deviation(df,days,multiplier):
		df['Lower_Standard_Deviation_Bands'] = df['Close'].rolling(window=days).mean() - df['Close'].rolling(window=days).std() * multiplier

	#calculates rolling minimum of upper standard deviation bands of x days; needs a upper_standard_deviation(df,days,multiplier) call on same df before
	def upper_band_limit(df,days):
		df['Upper_Band_Limit'] = df['Upper_Standard_Deviation_Bands'].rolling(window=days).min()

	#calculates rolling minimum of lower standard deviation bands of x days; needds a lower_standard_deviation(df,days,multiplier) call on same df before
	def lower_band_limit(df,days):
		df['Lower_Band_Limit'] = df['Lower_Standard_Deviation_Bands'].rolling(window=days).min()

	if __name__ == "__main__":
		for i in all_df:
			ln(i)
			ln_diff(i)
			ln_sum(i)
			ema(i,a)
			rolling_standard_deviation(i,b)
			upper_standard_deviation(i,b,c)
			lower_standard_deviation(i,b,d)
			upper_band_limit(i,e)
			lower_band_limit(i,e)
			insert_stat(i)