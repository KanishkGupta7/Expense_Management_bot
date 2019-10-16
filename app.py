  
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import mimetypes
import os
from urllib.parse import urlparse
from PIL import Image
#import PIL.Image
import re
from pytesseract import image_to_string
import pytesseract
import requests
import glob
import textract

#from webhook import reply_whatsapp
pytesseract.pytesseract.tesseract_cmd = os.environ.get('/app/.apt/usr/bin/tesseract')
from dialog import fetch_reply

app = Flask(__name__)
#print(app.root_path)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['GET','POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    resp = MessagingResponse()

    msg = request.form.get('Body')
    phone_no = request.form.get('From')
    media=int(request.values.get("NumMedia"))
    if media:
        reply=reply_whatsapp()
 #       resp.message(reply)
        print("#####")
        print(reply)
        
    else:
        reply = fetch_reply(msg, phone_no)

        
#        resp.message(reply)
          
          
 #   reply = fetch_reply(msg, phone_no)
    # Create reply
#    resp = MessagingResponse()
    resp.message(reply)
#    print(resp)
#    print(reply)
    return str(resp)
#    return resp.message("Thank you , we have received your payment. Here's your ticket")


def reply_whatsapp():
    
    print("@@@")
#    path='C:/Users/Administrator/Desktop/data/'
    num_media = int(request.values.get("NumMedia"))
    response = MessagingResponse()
    media_files = []
    for idx in range(num_media):
        media_url = request.values.get(f'MediaUrl{idx}')
        mime_type = request.values.get(f'MediaContentType{idx}')
        media_files.append((media_url, mime_type))
        
        req = requests.get(media_url)
        file_extension = mimetypes.guess_extension(mime_type)
        media_sid = os.path.basename(urlparse(media_url).path)
        
        if num_media:
            msg = response.message("thank you for the image")

        with open(f"data/{media_sid}{file_extension}", 'wb') as f:
            f.write(req.content)
            print(f)
#        f.close()   
#	with open(f"data/{media_sid}.png","wb") as f2:
#	    f2.write(req.content)     
    k=get_image_data('data/')
    print(k)
    
    k="Your voucher has been uploaded , the value is - " +k+'\n'+'Please confirm or type the correct value.'
    
#    response = MessagingResponse()
#    response=response.message(k)
    
#    print(type(response))
    return k
#    return response.message("Thank you , we have received your payment. Here's your ticket")
    
def get_image_data(path2):
    directories=[path2]
   
    list_of_files = glob.glob('data/*.jpe') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    if latest_file.endswith(".jpe") :
                   filename1=latest_file
                   print(filename1)
                   im = Image.open(filename1)
                   rgb_im = im.convert('RGB')
                   rgb_im.save('data/colors.png')
                   print(os.getcwd())

                   #m=(720,1280)
#                   text = Image.open('data/im.jpe').convert("RGB")
                   b = textract.process('data/colors.png', method='tesseract')
                   c= os.path.join(os.getcwd() + '/data/', 'colors.png')
                   print(c)
                   im = Image.open(c)
                   #rgb_im = im.convert('RGB')
                   im.save(c)
                   
                   #print(type(b))
		#   print(b)
		 #  print(type(b))
                   
#                   b=pytesseract.image_to_string(text)
        #               b=py.image_to_string(Image.open("/home/user/Downloads/grand.JPEG"))
                
                   print(b)        
                   b=b.decode('utf-8').split()
                   n=b[::-1]
                   print(n)
                   r=re.compile('^(AMOUNT*|Total*|Amount*|CASH*|Total*)')
                   p=list(filter(r.search,n))
                   p=n.index(p[0])
                  # print(p)
                   print('Test Check')    
                   return n[p-1]
				   
      
        


if __name__ == "__main__":
    app.run(debug=True)
