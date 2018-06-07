import re
import pyowm
import apiai
import json

Access_TokenApiai='231e8348713d476d9eb49abe3c3ce7da'


owm=pyowm.OWM('5124e78e5d11b3dad24c4cf0a3b4ba4f')
ai=apiai.ApiAI(Access_TokenApiai)




reply='Got nothing'

request=ai.text_request()
request.query='what about tomorrow ?'

response= json.loads(request.getresponse().read().decode('utf-8'))  #getting the response from the agent.
responseStatus = response['status']['code']

if (responseStatus==200):
    print("Bot response", response)






