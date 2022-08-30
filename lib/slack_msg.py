import requests
import time
import datetime
OK = 0


class slackbot:

    def __init__(self, channel, token):
        self.channel = channel
        self.token = token

    def post_message(self,text):

        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+ self.token},
            data={"channel": self.channel,"text": text}

        )

        return response

    def post_message_print(self, text):
        if text != "":
            print(text)
            self.post_message(text)


    def msg_filter_post(self, msg_list):
        msg_total = ""
        for msg in msg_list :

            if msg != None:
                msg = str(msg)
                msg_total = msg_total + "\n" + msg

        self.post_message_print(msg_total)




if __name__ == '__main__':

    while(1):
        slack = slackbot("#bitbot", token)
        slack.post_message(datetime.datetime.now())
