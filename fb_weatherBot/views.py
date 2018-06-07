
import json, requests, random, re
import pyowm
import apiai
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



PAGE_ACCESS_TOKEN = "EAACuhUNoWHcBAGU6YC1DqIvesUQhDOcL9axSMVzEmgzBNmxmWAlbyrbUxJDls6GtwSjwxbQUZBwu5e8gejTRpT3V6Ag4TZAYtCUT9ZBS3yWXyazjqgJooqNHqsZCd4ZAFbx6oWZCT2M5y2AoZAm58oc0uiGHWGgGixmj7NmCYT8YwZDZD"
VERIFY_TOKEN = "111152222"
Access_TokenApiai='231e8348713d476d9eb49abe3c3ce7da'



ai=apiai.ApiAI(Access_TokenApiai)





def post_facebook_message(fbid, recevied_message):

    request=ai.text_request()
    request.query=recevied_message

    intent_Name=''
    warm_weather='The temperature is high right now , make sure to wear something light & dont go out in the sun much !'
    cold_weather='The temperature is low right now , make sure to wear heavy clothes to keep you warm ! '
    response= json.loads(request.getresponse().read().decode('utf-8'))  #getting the response from the agent.
    responseStatus = response['status']['code']

    if (responseStatus==200):
        print("Bot response", response['result']['fulfillment']['speech'])
        try:
           intent_Name= response['result']['metadata']['intentName']

        except:
            reply=' '

        if(intent_Name=='Current-weather'):
            try:
              input_city=response['result']['parameters']['geo-city']
              owm = pyowm.OWM('5124e78e5d11b3dad24c4cf0a3b4ba4f')
              observation = owm.weather_at_place(input_city)
              w = observation.get_weather()
              curr_temp = str(w.get_temperature('celsius')['temp'])
              max_temp = str(w.get_temperature('celsius')['temp_max'])
              min_temp = str(w.get_temperature('celsius')['temp_min'])

              if(float(curr_temp) > 33):
                  reply= response['result']['fulfillment'][
                          'speech'] + curr_temp + ' celsius' + ' it has a high of ' + max_temp + ' C' +' and a low of ' + min_temp +' C' + '\n' +warm_weather

              elif(float(curr_temp) < 17):
                  reply = response['result']['fulfillment'][
                              'speech'] + curr_temp + ' celsius' + ' it has a high of ' + max_temp + ' C' + ' and a low of ' + min_temp + ' C' + '\n'+ cold_weather
              else:
                  reply = response['result']['fulfillment'][
                          'speech'] + curr_temp + ' celsius' + ' it has a high of ' + max_temp + ' C' +' and a low of ' + min_temp +' C'
            except:
                reply='Something wrong happened , please try again'


        else:
            reply=response['result']['fulfillment']['speech']
    else:
        reply='I didnt understand what you mean , please ask again'

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAACuhUNoWHcBAGU6YC1DqIvesUQhDOcL9axSMVzEmgzBNmxmWAlbyrbUxJDls6GtwSjwxbQUZBwu5e8gejTRpT3V6Ag4TZAYtCUT9ZBS3yWXyazjqgJooqNHqsZCd4ZAFbx6oWZCT2M5y2AoZAm58oc0uiGHWGgGixmj7NmCYT8YwZDZD'
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":reply}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


# Create your views here.
class weatherBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')
        
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        # Converts the text into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Printing the message to the terminal
                    pprint(message)    
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    post_facebook_message(message['sender']['id'], message['message']['text'])

        return HttpResponse()    