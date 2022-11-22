from time import time
import os

from yaml_reader import YamlPipelineExecutor

def main():

	#path to pipeline yaml file
	pipeline_path = os.environ.get("PIPELINE_LOCATION")
	if pipeline_path is None:
		print("Pipeline path is not defined")
		exit(1)

	scraper_start_time = time()

	yamlPipelineExecutor = YamlPipelineExecutor(pipeline_path)
	yamlPipelineExecutor.start()
	yamlPipelineExecutor.join()

	print('Extraction time took:', round(time() - scraper_start_time, 1))

if __name__ == '__main__':
	main()
