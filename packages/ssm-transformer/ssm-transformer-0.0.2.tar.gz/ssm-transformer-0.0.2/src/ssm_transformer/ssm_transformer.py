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

        # Store the message for further use and initiate some other variables
        self.message = message
        self.event_name = False

    def __determine_event_type(self):
        """ Helper function to determine the event type """
        if self.message.get('detail-type') == 'SSM Incident Start':
            self.event_name = 'incident_started'

    def __determing_incident_title(self):
        """ Helper function to determine the title of the incident """
        self.incident_title = self.message.get('detail').get('incidentTitle')

    def __determing_incident_id(self):
        """ Helper function to determine the id of the incident """
        self.incident_id = self.message.get('resources')[0]

    def transform(self):
        """ Main transformation function

            :return (dict): The base event
        """
        # Extract the info
        self.__determine_event_type()
        self.__determing_incident_title()
        self.__determing_incident_id()

        # Return base of the event info
        return {
            'event_name': self.event_name,
            'event_body': {
                'title': self.incident_title,
                'id': self.incident_id
            }
        }
