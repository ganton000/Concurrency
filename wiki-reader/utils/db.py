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
				{
				"AttributeName": "price",
				"AttributeType": "S"
				},
				{
				"AttributeName": "extracted_time",
				"AttributeType": "S"
				},
			],
			TableName=table_name,
			KeySchema=[{
				"AttributeName": "id",
				"KeyType": "RANGE"
			}]
		)
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
	pass

if __name__ == "__main__":
	table_name = "prices"

	create_table(table_name)

	main()