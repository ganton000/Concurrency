from time import time

from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkers import YahooFinanceWorker

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

if __name__ == '__main__':
	list_of_symbols = get_sp_stock_symbols()
	#get_price_of_stock("AAPL")

	get_stock_price_threading(
		YahooFinanceWorker=YahooFinanceWorker,
		symbol_list=list_of_symbols
		)
