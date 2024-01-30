
import logging
import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from datetime import date
from datetime import datetime
import paho.mqtt.client as mqtt
import os


logger = logging.getLogger(__name__)
# snippet-end:[python.example_code.dynamodb.helper.Movies.imports]
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("iot")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message  = str(msg.payload.decode("UTF-8"))
    print("Topic: {} / Message: {}".format(msg.topic, message))
    if(msg.payload.decode("UTF-8") == "Reply"):
        client.publish("python", os.environ.get('OS',''))

    try:
        
        run_scenario(
            'RelevadoDeEsfuerzos-Resistencia1-Proceso1', boto3.resource('dynamodb'), message)
    except Exception as e:
        print(f"Something went wrong with the demo! Here's what: {e}")



# snippet-start:[python.example_code.dynamodb.helper.Movies.class_full]
# snippet-start:[python.example_code.dynamodb.helper.Movies.class_decl]
class Temperaturas:
    """Encapsulates an Amazon DynamoDB table of movie data."""
    def __init__(self, dyn_resource):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = dyn_resource
        self.table = None
# snippet-end:[python.example_code.dynamodb.helper.Movies.class_decl]

    # snippet-start:[python.example_code.dynamodb.DescribeTable]
    def exists(self, table_name):
        """
        Determines whether a table exists. As a side effect, stores the table in
        a member variable.
        :param table_name: The name of the table to check.
        :return: True when the table exists; otherwise, False.
        """
        try:
            table = self.dyn_resource.Table(table_name)
            table.load()
            exists = True
        except ClientError as err:
            if err.response['Error']['Code'] == 'ResourceNotFoundException':
                exists = False
            else:
                logger.error(
                    "Couldn't check for existence of %s. Here's why: %s: %s",
                    table_name,
                    err.response['Error']['Code'], err.response['Error']['Message'])
                raise
        else:
            self.table = table
        return exists
    # snippet-end:[python.example_code.dynamodb.DescribeTable]

    # snippet-start:[python.example_code.dynamodb.CreateTable]
    def create_table(self, table_name):
        """
        Creates an Amazon DynamoDB table that can be used to store movie data.
        The table uses the release year of the movie as the partition key and the
        title as the sort key.
        :param table_name: The name of the table to create.
        :return: The newly created table.
        """
        try:
            self.table = self.dyn_resource.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'Hora', 'KeyType': 'HASH'},  # Partition key
                    {'AttributeName': 'Temperatura', 'KeyType': 'RANGE'}  # Sort key
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'Hora', 'AttributeType': 'S'},
                    {'AttributeName': 'Temperatura', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10})
            self.table.wait_until_exists()
        except ClientError as err:
            logger.error(
                "Couldn't create table %s. Here's why: %s: %s", table_name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return self.table
    # snippet-end:[python.example_code.dynamodb.CreateTable]

    # snippet-start:[python.example_code.dynamodb.ListTables]
    def list_tables(self):
        """
        Lists the Amazon DynamoDB tables for the current account.
        :return: The list of tables.
        """
        try:
            tables = []
            for table in self.dyn_resource.tables.all():
                print(table.name)
                tables.append(table)
        except ClientError as err:
            logger.error(
                "Couldn't list tables. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            return tables
    # snippet-end:[python.example_code.dynamodb.ListTables]

    # snippet-start:[python.example_code.dynamodb.BatchWriteItem]
    def write_batch(self, temperaturas):
        """
        Fills an Amazon DynamoDB table with the specified data, using the Boto3
        Table.batch_writer() function to put the items in the table.
        Inside the context manager, Table.batch_writer builds a list of
        requests. On exiting the context manager, Table.batch_writer starts sending
        batches of write requests to Amazon DynamoDB and automatically
        handles chunking, buffering, and retrying.
        :param movies: The data to put in the table. Each item must contain at least
                       the keys required by the schema that was specified when the
                       table was created.
        """
        try:
            with self.table.batch_writer() as writer:
                for temperatura in temperaturas:
                    writer.put_item(Item=temperatura)
        except ClientError as err:
            logger.error(
                "Couldn't load data into table %s. Here's why: %s: %s", self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
    # snippet-end:[python.example_code.dynamodb.BatchWriteItem]

    # snippet-start:[python.example_code.dynamodb.PutItem]
    def add_temp(self, time, temp):
        """
        Adds a temperature to the table.
        :param Hora: The title of the movie.
        :param Temperatura: The release year of the movie.
        
        """
        try:
            self.table.put_item(
                Item={
                    'Hora': time,
                    'Temperatura': temp})
        except ClientError as err:
            logger.error(
                "No se pudo agregar la temperatura %s to table %s. Here's why: %s: %s",
                temp, self.table.name,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
   


def run_scenario(table_name, dyn_resource, new_temp):
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    #print('-'*88)
    #print("Welcome to the Amazon DynamoDB getting started demo.")
    #print('-'*88)

    temperaturas = Temperaturas(dyn_resource)
    temp_exists = temperaturas.exists(table_name)
    if not temp_exists:
        print(f"\nCreating table {table_name}...")
        temperaturas.create_table(table_name)
        print(f"\nCreated table {temperaturas.table.name}.")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    new_data = {}
    new_data['Hora'] = dt_string
    new_data['Temperatura']  = new_temp
    #new_data = {"tiempo": dt_string, "Temperatura": new_temp} 
    
    temperaturas.add_temp(dt_string, new_temp)
    print(f"\nAdded '{new_data['Temperatura']}' to '{temperaturas.table.name}'.")
    print('-'*88)

    
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    SERVER_IP_ADDRESS = "127.0.0.1"
    client.connect(SERVER_IP_ADDRESS, 1883, 60)
    client.loop_forever()

# snippet-end:[python.example_code.dynamodb.Scenario_GettingStartedMovies]
