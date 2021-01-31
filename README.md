# Market-Analysis
Takes data from chosen CSV files, then transforms, plots, and transfers data into a database.

Download CSV files from Yahoo Finance, with set date of 1/1/2016 - 12/31/2020. Can use ^GSPC S&P 500 Index, ^SOX Semiconductor, and ^BKX Banks for example.

Computes ln(index), ln(index)-ln(GSPC), ln(index)+ln(GSPC), exponential moving average of rolling A days, standard deviation of rolling B days, upper standard devitaion bands (simple moving average of B days plus standard deviation times C), lower standard deviation bands (simple moving average of B days minus standard deviation times C), upper band limit (rolling minimum of upper standard deviation bands of E days), and lower band limit (rolling minimum of lower standard deviation bands of E days).
A, B, C, D, and E are parameters. 

When trying to change what to plot, please keep in mind what the dataframe columns are named in the code as to not cause any errors. 
