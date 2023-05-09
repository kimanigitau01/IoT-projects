from typing import List
import logging

import azure.functions as func
from azure.functions import EventHubEvent

def main(event: func.EventHubEvent):
    event_data = event.body
    # process event_data here
    logging.info('Python EventHub trigger processed an event: %s',
                event.get_body().decode('utf-8'))