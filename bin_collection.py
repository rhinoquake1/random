#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pandas as pd

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


# In[2]:


soup = BeautifulSoup(response.text, "html.parser")


# In[3]:


data = soup.find('div', attrs={'id': lambda e: e.endswith('BinResultsDetails') if e else False})


# In[4]:


result = data.find_all('div', attrs={'class': 'selectedContainer'})


# In[23]:


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

# The bin type is give in tag h3
# The subsequent dates are given as seperate li elements
# the below will create a new row for the bin type and the date for collection
for i in result:
    bin_type = i.h3.contents[1]
    bin_type = get_bin_type(bin_type)
    for j in i.find_all('li'):
        date = str(j.contents[0])
        date = date[date.find(' ')+1:]
        date = datetime.strptime(date, r'%d %b %Y').date()
        df_row = pd.DataFrame([[bin_type, date]], columns=dfs_cols)
        df = pd.concat([df, df_row])
print(df.sort_values('Dates').reset_index(drop=True))
    


# In[24]:


df = df.groupby(['Dates'])['Bin'].apply(list).reset_index()

