from twilio.rest import Client


class TwilioApi(Client):

    def __init__(self, account_sid, auth_token, twilio_number, admin_number):
        super().__init__(account_sid, auth_token)
        self.number = twilio_number
        self.admin_number = admin_number

    def send_text(self, to_number, message):
        self.messages.create(from_=self.number, to=to_number, body=message)

    def send_text_to_admin(self, message):
        self.messages.create(from_=self.number, to=self.admin_number, body=message)
