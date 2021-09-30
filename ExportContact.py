from asyncio.windows_events import NULL
# from typing import Text
from telethon.errors import SessionPasswordNeededError
from telethon.client.account import _TakeoutClient
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon import errors
import getpass
import base64,os,click,datetime,time

# Telegram information conection
api_id = 1234564
api_hash = "api_hash"
name = "CSV_contact_maker_for_phone"
phone = 989120000000


PhotoVCF = click.prompt('[1] Do you need your contact photo', default= "yes" , type =bool)
fileNameVCF = click.prompt('[2] Your VCF file name', default= "MyContactTelegramToPhone" , type =str)

# add date to file name
fileNameVCF = fileNameVCF + "_" + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H-%M-%S')
if PhotoVCF :
    bigPhoto = click.prompt('[3] Photo with maximum quality?', default= "no" , type =bool)
    keepPHOTO = click.prompt('[4] Save contact photos to your system (not recommend)?', default= "no" , type =bool)
    partial = click.prompt('[5] Number of user contact each vcf file \nhelp:\nSome phones do not support large vcf file, so we split vcf file. prefer', default= 5, type=int)
else:
    partial = NULL

# download user photo and convert to base 64
def download_photo(client,id,bigPhoto=False):
    path = client.download_profile_photo(id,download_big=bigPhoto)
    if(path != None):
        with open(path, "rb") as image_file:
            data = base64.standard_b64encode(image_file.read()).decode('utf-8')
            if keepPHOTO != True:
                image_file.close()
                os.remove(path)
            return "ENCODING=BASE64;TYPE=JPEG:" + "\n" + str(data)+ "\n"
    return NULL

# make vcf files
def writer(myName,family,phone, FileName ,photo = NULL):
    name = "BEGIN:VCARD\nVERSION:2.1\nN:"+ family +";" + myName + "\n"
    family = "FN:" + myName + " " + family + "\n"
    phone = "TEL;CELL:" + phone + "\n"
    if photo != NULL:
        photo = "PHOTO;" + photo + "\n"
        end = photo + "END:VCARD\n"
    else :   
        end = "END:VCARD\n"
    with open(str(FileName)+".vcf", 'a+',encoding='utf-8') as outfile:
        outfile.writelines([name, family, phone, end])

# check F/name 
def checkStr(string):
    if string and string !=0 and string != "0" and string != "-" and string != "_" and string != "." and string != NULL and string != None:
        return str(string)
    return ""

# connect to telegram
with TelegramClient(name, api_id, api_hash) as client:
    
    # If there is an error, you can use the following code
    # client.sign_in(phone=phone)
    # try:
    #     client.sign_in(code=input('Enter code: '))
    # except SessionPasswordNeededError:
    #     client.sign_in(password=getpass.getpass())
    
    try:
        users = client(functions.contacts.GetContactIDsRequest(
            hash=0
        ))
        FilePart = 1 if partial != NULL else ""
        i = 1
        for userID in users:
            result = client(functions.users.GetUsersRequest(
            id = [int(userID)]
            ))
            userInfo = []
            for x in result:
                print("phone : " , "+" + str(x.phone))
                
                if PhotoVCF :
                    photo = download_photo(client,x.id, bigPhoto)
                else:
                    photo = NULL
                
                phone = "+" + str(x.phone)
                
                VCFname = fileNameVCF if partial == NULL else fileNameVCF + "(" + str(FilePart) +")"
                writer(checkStr(x.first_name),checkStr(x.last_name),phone,VCFname,photo)
                print("______________________")
                
                if partial != NULL:
                    if (i % partial) == 0 :
                        FilePart += 1
                    i+=1
                
    except errors.TakeoutInitDelayError as e:
        print('Must wait', e.seconds, 'before takeout')
