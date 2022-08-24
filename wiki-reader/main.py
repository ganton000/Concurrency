from workers.WikiWorker import WikiWorker

def get_sp_stock_symbols():
	url_to_fetch = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

	wikiWorker = WikiWorker(url=url_to_fetch)

	symbol_list = []
	for symbol in wikiWorker.get_sp_500_companies():
		symbol_list.append(symbol)

	assert len(symbol_list) == 503, "Not all symbols were retrieved!"

if __name__ == '__main__':
	get_sp_stock_symbols()