from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys


AWS_ACCESS_KEY_ID = os.getenv('ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = os.getenv('SECRET_KEY')
REGION_NAME = "eu-west-2"


class Polly:

    def __init__(self):
        self.session = Session(aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                               region_name=REGION_NAME)
        self.polly = self.session.client("polly")
        self.output = ""

    def convert(self, text, file_name):
        try:
            response = self.polly.synthesize_speech(Text=text,
                                                    OutputFormat="mp3",
                                                    VoiceId="Matthew")
        except (BotoCoreError, ClientError) as error:
            print(error)
            sys.exit(-1)

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                self.output = f"{file_name}.mp3"
                try:
                    with open(self.output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    print(error)
                    sys.exit(-1)
        else:
            print("Could not stream audio")
            sys.exit(-1)
