#!/usr/bin/env python
# coding: utf-8

# jupyter nbconvert --to script 'bin_collection.ipynb'
# 
# pip3 freeze > requirements.txt

# In[504]:


from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd

# response request for curr address
# need to create a more deynamic response where https://www.leeds.gov.uk/residents/bins-and-recycling/check-your-bin-day is opened
# and the form is submitted with the address to get to get a dynamic request

headers = {
    'authority': 'www.leeds.gov.uk',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'upgrade-insecure-requests': '1',
    'origin': 'https://www.leeds.gov.uk',
    'content-type': 'application/x-www-form-urlencoded',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.leeds.gov.uk/residents/bins-and-recycling/check-your-bin-day',
    'accept-language': 'en-US,en;q=0.9,en-GB;q=0.8',
    'cookie': 'visid_incap_2048550=7e7cFK+xQauOWWDiWO3uemBkImIAAAAAQUIPAAAAAADFKLfevW6TU6A4h6OFDgYM; incap_ses_1319_2048550=InbcEXla1RyAWPTo8gdOEmBkImIAAAAALDxorjVCWSYu5GvZL4wsiA==; WSS_FullScreenMode=false; SearchSession=3378e4b6%2D76c6%2D4a71%2D99b3%2Ddc98acd0f5c1',
}

data = {
  '_wpcmWpid': '',
  'wpcmVal': '',
  'MSOWebPartPage_PostbackSource': '',
  'MSOTlPn_SelectedWpId': '',
  'MSOTlPn_View': '0',
  'MSOTlPn_ShowSettings': 'False',
  'MSOGallery_SelectedLibrary': '',
  'MSOGallery_FilterString': '',
  'MSOTlPn_Button': 'none',
  '__EVENTTARGET': 'ctl00$ctl48$g_eea1a8ba_4306_488e_96f2_97f22038e29f$ctl00$ddlAddressList',
  '__EVENTARGUMENT': '',
  '__REQUESTDIGEST': '0x8825035918BD1CCA7917CA58A5622ECF8662B586D34D66FE1B47E01CAF45B92FC32B3E1FB970B2251BB46D46DFCE4F27E72AAB8650619351F8BF9F13D9FFD277,04 Mar 2022 19:24:16 -0000',
  'MSOSPWebPartManager_DisplayModeName': 'Browse',
  'MSOSPWebPartManager_ExitingDesignMode': 'false',
  'MSOWebPartPage_Shared': '',
  'MSOLayout_LayoutChanges': '',
  'MSOLayout_InDesignMode': '',
  '_wpSelected': '',
  '_wzSelected': '',
  'MSOSPWebPartManager_OldDisplayModeName': 'Browse',
  'MSOSPWebPartManager_StartWebPartEditingName': 'false',
  'MSOSPWebPartManager_EndWebPartEditing': 'false',
  '__LASTFOCUS': '',
  '__VIEWSTATE': '/wEPDwUBMA9kFgJmD2QWAgIBD2QWCAIBD2QWBAIZD2QWAmYPZBYCAgEPFgIeE1ByZXZpb3VzQ29udHJvbE1vZGULKYgBTWljcm9zb2Z0LlNoYXJlUG9pbnQuV2ViQ29udHJvbHMuU1BDb250cm9sTW9kZSwgTWljcm9zb2Z0LlNoYXJlUG9pbnQsIFZlcnNpb249MTUuMC4wLjAsIEN1bHR1cmU9bmV1dHJhbCwgUHVibGljS2V5VG9rZW49NzFlOWJjZTExMWU5NDI5YwFkAiUPZBYCAgMPZBYCZg9kFgJmDzwrAAYAZAIDD2QWAgIBD2QWAgUmZ19lZWExYThiYV80MzA2XzQ4OGVfOTZmMl85N2YyMjAzOGUyOWYPZBYCZg9kFgQCAQ8PFgQeBFRleHRlHgdWaXNpYmxlaGRkAgkPDxYCHwJnZBYGAgMPEA8WCh4HVG9vbFRpcAVzUGxlYXNlIHNlbGVjdCB5b3VyIGFkZHJlc3MgZnJvbSB0aGUgbGlzdC4gVGhlcmUgaXMgbW9yZSB0aGFuIG9uZSBzZWxlY3Rpb24gYXZhaWxhYmxlIGZvciBwb3N0Y29kZSB5b3UgaGF2ZSBlbnRlcmVkLh4ORGF0YVZhbHVlRmllbGQFA0tleR4NRGF0YVRleHRGaWVsZAUFVmFsdWUeC18hRGF0YUJvdW5kZx8CZ2QQFSMoUGxlYXNlIHNlbGVjdCB5b3VyIGFkZHJlc3MgZnJvbSB0aGUgbGlzdDExLCBNQUdHSUUgQkFSS0VSIEFWRU5VRSwgTUFOU1RPTiwgTEVFRFMsIExTMTUgOEZIMTIsIE1BR0dJRSBCQVJLRVIgQVZFTlVFLCBNQU5TVE9OLCBMRUVEUywgTFMxNSA4RkgxMywgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDE0LCBNQUdHSUUgQkFSS0VSIEFWRU5VRSwgTUFOU1RPTiwgTEVFRFMsIExTMTUgOEZIMTUsIE1BR0dJRSBCQVJLRVIgQVZFTlVFLCBNQU5TVE9OLCBMRUVEUywgTFMxNSA4RkgxNiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDE3LCBNQUdHSUUgQkFSS0VSIEFWRU5VRSwgTUFOU1RPTiwgTEVFRFMsIExTMTUgOEZIMTgsIE1BR0dJRSBCQVJLRVIgQVZFTlVFLCBNQU5TVE9OLCBMRUVEUywgTFMxNSA4RkgxOSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxMCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxMSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxMiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxNCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxNSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxNiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxNywgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxOCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIxOSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyMCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyMSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyMiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyMywgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyNCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyNSwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyNiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyNywgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIyOCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIzMCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIzMiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIzNCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIzNiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDIzOCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDI0MCwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSDI0MiwgTUFHR0lFIEJBUktFUiBBVkVOVUUsIE1BTlNUT04sIExFRURTLCBMUzE1IDhGSBUjKFBsZWFzZSBzZWxlY3QgeW91ciBhZGRyZXNzIGZyb20gdGhlIGxpc3QINzI3MjcxMDcINzI3MjcxNTcINzI3MjcxMDgINzI3MjcxNTYINzI3MjcxMDkINzI3MjcxNDcINzI3MjcxMTAINzI3MjcxNDYINzI3MjcxMTEINzI3MjcxNDUINzI3MjcxMTIINzI3MjcxNDQINzI3MjcxNDMINzI3MjcxMTMINzI3MjcxNDIINzI3MjcxMTQINzI3MjcxNDEINzI3MjcxMTUINzI3MjcxMzMINzI3MjcxMTYINzI3MjcxMzIINzI3MjcxMTcINzI3MjcxMzEINzI3MjcyMDkINzI3MjcxMzAINzI3MjcyMTAINzI3MjcxMjkINzI3MjcxMTkINzI3MjcxMTgINzI3MjcyMzUINzI3MjcyMjEINzI3MjcyMjIINzI3MjcyMjMINzI3MjcyMjQUKwMjZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2dnZ2cWAQIXZAIFDxYCHwJnZAIHDw8WBB8CZx8DBVRZb3UgY2FuIG5vdyB2aWV3IGFuZCBwcmludCB5b3VyIG5leHQgMTMgYmluIGNvbGxlY3Rpb24gZGF0ZXMgZm9yIGFsbCB5b3VyIGJpbiB0eXBlcy5kZAIJD2QWBAIFD2QWAgICD2QWAgIFD2QWAgIDDxYCHwJoFgJmD2QWBAICD2QWBgIBDxYCHwJoZAIDDxYCHwJoZAIFDxYCHwJoZAIDDw8WAh4JQWNjZXNzS2V5BQEvZGQCDw9kFgICAg9kFggCBQ88KwAFAQAPFgIeD1NpdGVNYXBQcm92aWRlcgUjQ3VycmVudE5hdmlnYXRpb25Td2l0Y2hhYmxlUHJvdmlkZXJkZAIHDxYCHwALKwQBZAIJDxYCHwALKwQBZAINDxYCHwALKwQBZAIlD2QWAgIBDxYCHwALKwQBZGR149LXHlFdPSo2+bcmByJ9Btmn6AdvEnJ/6ckCvU3M0Q==',
  '__VIEWSTATEGENERATOR': 'BAB98CB3',
  '__EVENTVALIDATION': '/wEdACfmAbi/+YKlU0wY1kVwT6+GPp4eGrXbzCYgL3WjGmh6mlsGyRQXXkettmkh8ZFeH7Zo1gImlgzdQ4X1OwOIKHYub/7mAEI76G5/BF99Jh0SXuAEeTUgkiEyeX5972qLdRFaJZ34rGldHk0BxaPaPTIXnlHcSD9jLIZXiL9BsZaIDqZ97Y5tLnzQtC5kiYqQ8XGfXalc+1l4TwyN9qUK12Lit/QR/SAeUW604JptSykN6Uy9zbgXa7CJFW7sEbTsGOgNU5arrxUUjpLq269oCTTNOasdWTzCIlGpBZesXOPP8fhgVtdDpxwDaDsrlamOZRnjtt+cKisgB3g4ECXge9WZEd1+yaQizbfT6nE2m3OWmdZeXWVVj/XyDgwtmM8FZiRJp16n3R0a1ca9YYorkSKCNaoX6PLK6nntrVbX9/rV3A4xpK31lehvzIVDzkWrFZf4caL2GHtnysxekFSsQBodaJH/hqo3mmeLjKg8waFxa/9uP0nIJJHUQsVunENjYaxr0JfK+PaY482gNjnlE9HHOSG47tA5ecBGLCzFCdQ/fFc5tse7FabghVbTUI4kGlSNyzcmavhRViDeA8cn/wQFjYzAI4eQ4+qXP0Datp1v4gVtAuk9QaFMuDro4/9YVzpO+5oR+g/CYY7rAEssK/5zWnemHiHi82MMCUmSQkIuy0ua0S24XaIN/mdVGLAbAumnVBRlR/hbXGLNImNf/iQ5Gwq0mu3sulfTtAEOkQ2/3yRb1r2dm4OOE/HmaQtPGrQK3sZU+lZC/vC6lrA4dv2gLnL0ipMldtHkT6FyHYBwbDAJza6ufUk3uNekSvyrCsvjho3dvCou1xBSzEItK1wuDf0H+IfG5I4qPuLsFkcrWA==',
  'ctl00$ctl48$g_eea1a8ba_4306_488e_96f2_97f22038e29f$ctl00$txtPostCode': 'LS15 8fh',
  'ctl00$ctl48$g_eea1a8ba_4306_488e_96f2_97f22038e29f$ctl00$ddlAddressList': '72727132'
}

response = requests.post('https://www.leeds.gov.uk/residents/bins-and-recycling/check-your-bin-day', headers=headers, data=data)


# In[505]:


# convert to html
soup = BeautifulSoup(response.text, "html.parser")


# In[506]:


# filter html to BinResultsDetails tag, and keep as soup
data = soup.find('div', attrs={'id': lambda e: e.endswith('BinResultsDetails') if e else False})


# In[507]:


# returns seperate containers for each bin type
result = data.find_all('div', attrs={'class': 'selectedContainer'})


# In[508]:


dfs_cols = ['Bin', 'Dates']
df = pd.DataFrame(columns=dfs_cols)


def get_bin_type(raw_text):
    # searches each word in sentence describing bin in pageweb until a match is found
    # if there is no match the bin is sus 
    bins = ['Black', 'Green', 'Brown']
    words = raw_text.split(' ')
    for bin in bins:
        for word in words:
                if bin.lower() in word.lower():
                    return bin
    return 'sus'

# this iterates through each block bin to pull data
# The bin type is give in tag h3
# The subsequent dates are given as seperate li elements
# the below will create a new row for the bin type and the date for collection
for i in result:
    bin_type = i.h3.contents[1]
    bin_type = get_bin_type(bin_type)
    for j in i.find_all('li'):
        date = str(j.contents[0])
        date = date[date.find(' ')+1:]
        date = datetime.datetime.strptime(date, r'%d %b %Y').date()
        df_row = pd.DataFrame([[bin_type, date]], columns=dfs_cols)
        df = pd.concat([df, df_row])
print(df.sort_values('Dates').reset_index(drop=True))
    


# In[509]:


# Group by date and aggregate dates into lists
df = df.groupby(['Dates'])['Bin'].apply(list).reset_index()


# https://realpython.com/python-send-email/
# Gmail req: Turn Allow less secure apps to ON. Be aware that this makes it easier for others to gain access to your account.

# In[510]:


import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_bin_email(bin_colour, msg_text):
    port = 465  # For SSL
    password = 'maggie_barker_22_2022'

    sender_email = "rhinoquake@gmail.com"
    receiver_email = "rhinoquake@gmail.com"

    message = MIMEMultipart("alternative")
    message["Subject"] = f'The {bin_colour} bin'
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """    This isn't right >.<"""
    html = msg_text

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


# In[513]:


df = df.reindex(columns=dfs_cols) # reorder columns
df['Bin'] = df.apply(lambda x: '& '.join(x['Bin']), axis = 1) # combines the lists in each row with an &
next_bins = df.iloc[0] # next bin collection


# In[514]:


df['Dates'] = pd.to_datetime(df['Dates']) # convert date vals to datetime types
df['date'] = df['Dates'].dt.day_name() + ' ' + df['Dates'].dt.strftime(r'%d %b %y') # format the date to: Dayname Day Mon Yr


# In[515]:


df


# In[544]:


email_table = df.iloc[1:8] # next x collections
email_table : pd.DataFrame = email_table.drop('Dates', axis=1).to_html(index=False, header=False, classes='table, th, td style="width:100%;padding:200px;border-collapse:collapse;', border=0)


# In[545]:


email_table


# In[561]:


# the email text starts with saying which bin is due for collection the next day. It then gives the next x collections as a table
consolidated_email_text = f'''
<html>
<body>
<p>Hi,<br>
        It's me, the {next_bins.Bin} bin<br>
        Please take me out tonight (∩︵∩)<br>
        Thx xoxo
    </p>
<p><small>btw, please don't forget about my fwiends ^-^</h3>\n
{email_table}
</p></small></body>
</html>
'''


# In[562]:


def send_bin_email_day_before(next_bins, consolidated_email_text, check_date=True):
    if check_date:
        if next_bins.Dates == (date.today() + datetime.timedelta(days=1)):
            send_bin_email(next_bins.Bin, consolidated_email_text)
    else:
        send_bin_email(next_bins.Bin, consolidated_email_text)


# In[ ]:


send_bin_email_day_before(next_bins, consolidated_email_text)

