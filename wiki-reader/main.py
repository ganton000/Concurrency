from time import time

from yaml_reader import YamlPipelineExecutor

def main():

	#path to pipeline yaml file
	pipeline_path = "pipelines/wiki_yahoo_scraper_pipeline.yaml"

	scraper_start_time = time()

	yamlPipelineExecutor = YamlPipelineExecutor(pipeline_path)
	yamlPipelineExecutor.process_pipeline()

	print('Extraction time took:', round(time() - scraper_start_time, 1))

if __name__ == '__main__':
	main()
