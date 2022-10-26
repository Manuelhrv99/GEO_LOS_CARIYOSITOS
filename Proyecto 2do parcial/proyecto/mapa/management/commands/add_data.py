from django.core.management.base import BaseCommand
import pandas as pd
from mapa.models import Transport
from sqlalchemy import create_engine

import boto3
from io import StringIO

class Command(BaseCommand):
    help = 'A command to add data from a csv file to the database'
    def handle(self, *args, **options):
        '''client = boto3.client('s3', aws_access_key_id='AKIAY6GROA5JUANGUVEX',
            aws_secret_access_key='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')

        bucket_name = 'transports-csv'
        object_key = 'transports.csv'
        csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
        body = csv_obj['Body']
        csv_string = body.read().decode('utf-8')

        df = pd.read_csv(StringIO(csv_string))'''

        df = pd.read_csv('../transports.csv')
        engine = create_engine('sqlite:///db.sqlite3')
        df.to_sql(Transport._meta.db_table, if_exists='replace', con=engine, index=False)
        print('Se actualizo la base de datos')