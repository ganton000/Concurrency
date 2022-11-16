from time import time
from multiprocessing import Queue

from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkers import YahooFinancePriceScheduler, YahooFinanceWorker
from workers.DynamoWorker import DynamoMasterScheduler

def get_sp_stock_symbols():
	url_to_fetch = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

	wikiWorker = WikiWorker(url=url_to_fetch)

	symbol_list = []
	for symbol in wikiWorker.get_sp_500_companies():
		symbol_list.append(symbol)

	assert len(symbol_list) == 503, "Not all symbols were retrieved!"

	return symbol_list

def get_price_of_stock(stock_symbol):
	YahooFinanceWorker(stock_symbol).run()

def get_stock_price_threading(YahooFinanceWorker, symbol_list):
	scraper_start_time = time()

	current_workers = []

	for symbol in symbol_list:
		yahooFinancePriceWorker = YahooFinanceWorker(symbol=symbol)
		current_workers.append(yahooFinancePriceWorker)

	for i in range(len(current_workers)):
		current_workers[i].join()

	print('Extraction time took:', round(time() - scraper_start_time, 1))

def main():
	url_to_fetch = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

	#initialize queues
	symbol_queue = Queue()
	dynamo_queue = Queue()

	scraper_start_time = time()


	wikiWorker = WikiWorker(url=url_to_fetch)

	yahoo_finance_price_scheduler_threads = []
	num_yahoo_finance_price_workers = 4
	for i in range(num_yahoo_finance_price_workers):
		yahooFinancePriceScheduler = YahooFinancePriceScheduler(input_queue=symbol_queue, output_queue=[dynamo_queue])
		yahoo_finance_price_scheduler_threads.append(yahooFinancePriceScheduler)

	dynamo_scheduler_threads = []
	num_dynamo_workers = 4
	for i in range(num_dynamo_workers):
		dynamoScheduler = DynamoMasterScheduler(input_queue=dynamo_queue)
		dynamo_scheduler_threads.append(dynamoScheduler)

	for symbol in wikiWorker.get_sp_500_companies():
		print('Inserting first symbol into queue')
		symbol_queue.put(symbol)

	for _ in range(len(yahoo_finance_price_scheduler_threads)):
		symbol_queue.put('DONE') #DONE for each thread

	for i in range(len(yahoo_finance_price_scheduler_threads)):
		yahoo_finance_price_scheduler_threads[i].join()

	for i in range(len(dynamo_scheduler_threads)):
		dynamo_scheduler_threads[i].join()

	print('Extraction time took:', round(time() - scraper_start_time, 1))

if __name__ == '__main__':

	#list_of_symbols = get_sp_stock_symbols()
	#get_price_of_stock("AAPL")

	#get_stock_price_threading(
	#	YahooFinanceWorker=YahooFinanceWorker,
	#	symbol_list=list_of_symbols
	#	)

	main()
