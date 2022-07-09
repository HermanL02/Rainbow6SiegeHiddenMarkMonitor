import time
import pyttsx3
from urllib.request import Request, urlopen


def findMark(dictNameGameName, name):
    """
    The function is to retrieve mark from the website
    :param dictNameGameName:
    :param name:
    :return:
    """
    try:
        gameName = dictNameGameName[name]
        url = "https://r6.tracker.network/profile/pc/" + gameName
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0', "Cache-Control": "no-cache", "Pragma": "no-cache"})
        time.sleep(1)
        content = urlopen(req).read().decode('utf-8')
        specialChar = '<span class="trn-text--dimmed" style="width: 55px;">Casual</span>'
        specialChar2 = '\n<span>0.47 <span class="trn-text--dimmed">KD</span></span>\n<span>'
        lengthSS = len(specialChar) + len(specialChar2)
        pos = int(content.find(specialChar))
        markComma = content[pos + lengthSS:pos + 5 + lengthSS]
        markComma = markComma.replace(',', '')
        markComma = markComma.replace("<", '')
        markComma = markComma.replace("s", '')
        markComma = markComma.replace("p", '')
        markComma = markComma.replace("a", '')
        mark = int(markComma)
        return mark
    except:
        print("Access to the website error! ")
        return -1


readEngine = pyttsx3.init()
# for voice in readEngine.getProperty('voices'):
#     print(voice)
dictNameGameName = {}  # "老侯": "woshishenmou", "刘维": "minghaixiaoyao", "梁逸群": "HermanLYQ"
dictNameGameMark = {}  # "老侯": 0, "刘维": 0, "梁逸群": 0
dictNameNextTime = {}  # "老侯": 0, "刘维": 0, "梁逸群": 0
while True:
    name = input("Please enter the nickname you want to hear: (For example: 'Tom') [Enter 'exit' to exit]\n")
    if name == "exit":
        break
    nameInG = input("Please enter the username in Rainbow 6 Siege: \n")
    dictNameGameName[name] = nameInG
    dictNameNextTime[name] = 0
    dictNameGameMark[name] = 0
    print("You monitored {}", name, ", and his username is", nameInG)

while True:
    for i in dictNameGameName.keys():
        mark = findMark(dictNameGameName, i)
        if mark == -1:
            continue
        currentTime = time.time()
        if time.time() > dictNameNextTime[i]:
            if mark > dictNameGameMark[i]:
                readEngine.say(i + "Highered" + str(mark))
                readEngine.runAndWait()
                dictNameNextTime[i] = time.time() + 240
            if mark < dictNameGameMark[i]:
                readEngine.say(i + "Lowered" + str(mark))
                readEngine.runAndWait()
                dictNameNextTime[i] = time.time() + 240
        print(i + " " + str(mark))
        dictNameGameMark[i] = mark
        time.sleep(1)
