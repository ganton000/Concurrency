from workers.WikiWorker import WikiWorker

def main():
	url_to_fetch = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

	wikiWorker = WikiWorker(url=url_to_fetch)

if __name__ == '__main__':
	pass