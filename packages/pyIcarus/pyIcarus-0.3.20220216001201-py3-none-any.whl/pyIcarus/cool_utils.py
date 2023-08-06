import win32com.client as wincom


def speak(text):
    tts = wincom.Dispatch("SAPI.SpVoice")
    tts.Rate = 1
    tts.Speak(text)


speak('''Never gonna give you up
Never gonna let you down
Never gonna run around and desert you
Never gonna make you cry
Never gonna say goodbye
Never gonna tell a lie and hurt you''')

"""Lyrics:
    Songwriters: M Aitken / P Waterman / M Stock
    Never Gonna Give You Up lyrics © All Boys Music Ltd., Sids Songs Ltd., Mike Stock Publishing Limited
"""
