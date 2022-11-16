import boto3

#initialize clients
dynamo = boto3.client("dynamodb")


def create_table(table_name):
	try:
		dynamo.create_table(
			AttributeDefinitions=[
				{
				"AttributeName": "id",
				"AttributeType": "N"
				},
				{
				"AttributeName": "symbol",
				"AttributeType": "S"
				},
			],
			TableName=table_name,
			KeySchema=[
				{
				"AttributeName": "symbol",
				"KeyType": "HASH"
				},
				{
				"AttributeName": "id",
				"KeyType": "RANGE"
				}
			],
			ProvisionedThroughput={
				"ReadCapacityUnits": 1,
				"WriteCapacityUnits": 1
    		}
		)
	except dynamo.exceptions.ResourceInUseException as err:
		print(err.response)
		print(f'{err.response["Error"]["Code"]}:: {err.response["Error"]["Message"]}')
	except Exception as err:
		print(err)
		exit(1)

def add_item(table_name, item):
	try:
		dynamo.put_item(
			TableName=table_name,
			Item=item
		)
	except Exception as err:
		print(err)
		exit(1)

def main():

	table_name = "prices"

	items = [
		{
			"id": { "N": "1" },
			"symbol": { "S": "a" },
			"price": { "N": "3" },
			"extracted_time": { "S": "3"}
		},
		{
			"id": { "N": "2" },
			"symbol": { "S": "b" },
			"price": { "N": "4" },
			"extracted_time": { "S": "4"}
		},
		{
			"id": { "N": "3" },
			"symbol": { "S": "a" },
			"price": { "N": "5" },
			"extracted_time": { "S": "5"}
		}
	]

	try:
		create_table(table_name)
		#for item in items:
		#	add_item(table_name, item)
		#print(dynamo.exceptions._code_to_exception)
		print(dynamo.exceptions._code_to_exception["ResourceInUseException"].MSG_TEMPLATE)
	except dynamo.exceptions.ResourceInUseException as err:
		print(f'{err.response["Error"]["Code"]}:: {err.response["Error"]["Message"]}')
		print("Will attempt to still add items to table...")
		for item in items:
			add_item(table_name, item)

if __name__ == "__main__":
	main()