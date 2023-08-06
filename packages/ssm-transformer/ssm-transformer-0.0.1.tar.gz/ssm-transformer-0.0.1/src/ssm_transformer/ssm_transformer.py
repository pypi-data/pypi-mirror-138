import json


class TooManyRecords(Exception):
    """ Raised when moren then 1 record comes in from SNS """
    pass


class SSM_Notifications_Transformer:
    """ Class to transform a notification from the incident manager to a business even """

    def __init__(self, notification_payload) -> None:
        # Check that we only have one record, otherwise we must revise the logic here
        if len(notification_payload.get('Records')) != 1:
            raise TooManyRecords

        # Get the message and read the json from the string
        message = json.loads(notification_payload.get(
            'Records')[0].get('Sns').get('Message'))

        # Store the message for further use
        self.message = message

    def __determine_event_type(self):
        """ Helper function to determine the event type """
        if self.message.get('detail-type') == 'SSM Incident Start':
            self.event_name = 'incident_started'
        else:
            self.event_name = False

    def transform(self):
        """ Main transformation function """
        if self.event_name:
            return {
                'event_name': self.event_name
            }

        return False
