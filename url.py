import urllib2

def URL_to_dict(strURL):
    dict_result = {}
    index = strURL.find("://")
    if index < 1:
        return None
    strURL_tmp = strURL[index + 3:]
    dict_result["schema"] = strURL[:index]
    index = strURL_tmp.find("@")
    if index > 0:
        strURL_uspass = strURL_tmp[:index]
        strURL_tmp = strURL_tmp[index + 1:]
        index = strURL_uspass.find(":")
        if index > 0:
            dict_result["name"] = strURL_uspass[:index]
            dict_result["pass"] = strURL_uspass[index + 1:]
            if len(dict_result["pass"]) <= 0:
                return None
        elif index < 0:
            dict_result["name"] = strURL_uspass
            dict_result["pass"] = ""
        else:
            return None
    elif index < 0:
        dict_result["name"] = ""
        dict_result["pass"] = ""
    else:
        return None
    index = strURL_tmp.find("/")
    if index > 0:
        dict_result["path"] = strURL_tmp[index:]
        strURL_tmp = strURL_tmp[0:index]
    elif index < 0:
        dict_result["path"] = ""
    else:
        return None

    index = strURL_tmp.find(":")
    if index > 0:
        dict_result["port"] = strURL_tmp[index + 1:]
        dict_result["domain"] = strURL_tmp[:index]
    elif index < 0:
        dict_result["port"] = ""
        dict_result["domain"] = strURL_tmp
    else:
        return None
    return dict_result

def joinURL(strURL1, strURL2):
    strURL = ""
    strPath1 = ""
    strPath2 = ""

    dictURL1 = URL_to_dict(strURL1)
    if dictURL1 == None:
        return None

    dictURL2 = URL_to_dict(strURL2)
    if dictURL2 != None:
        if dictURL2['path'] == "":
            strURL = dictURL2['schema'] + "://" + dictURL2['domain']
        else:
            strURL = dictURL1['schema'] + "://" + dictURL1['domain']

        strPath2 = dictURL2['path']
    else:
        strURL = dictURL1['schema'] + "://" + dictURL1['domain']
        strPath2 = strURL2

    strPath1 = dictURL1['path']
    if len(strPath2) == 0:
        return strURL + strPath1
    if strPath2[0] == "/":
        strURL = strURL + strPath2
    else:
        strURL = strURL + strPath1 + "/" + strPath2

    return strURL

def urlLinks(url, level):
    strPage = urllib2.urlopen(url).read()
    index = 0
    strLink = ""
    arrLinks = []
    while index >= 0:
        index = strPage.find("\"")
        if index < 0:
            break
        strPage = strPage[index + 1:]
        index = strPage.find("\"")
        strLink = strPage[:index]
        strPage = strPage[index + 1:]
        dictLink = URL_to_dict(strLink)
        if dictLink != None:
            strPath = dictLink['path']
            strPath = strPath.strip("/")
            massLevels = strPath.split("/")
            if len(massLevels) <= level:
                arrLinks.append(strLink)
    return arrLinks

def testURL():
    assert URL_to_dict("http://google.com/a/b") == { 'name':'', 'domain':'google.com',\
    'schema':'http', 'pass':'', 'path':'/a/b', 'port':''}
    assert URL_to_dict("http://yser:pass@google.com:80/a/b") == { 'name':'yser',\
    'domain':'google.com', 'pass':'pass', 'path':'/a/b', 'port':'80', 'schema':'http'}
    assert URL_to_dict("http://yser:pass@google.com:80") == { 'name':'yser',\
    'domain':'google.com', 'pass':'pass', 'path':'', 'port':'80', 'schema':'http'}
    assert URL_to_dict("http://yser:pass@google.com:/a/b") == { 'name':'yser',\
    'domain':'google.com', 'pass':'pass', 'path':'/a/b', 'port':'', 'schema':'http'}
    assert URL_to_dict("http://yser@google.com:80/a/b") == { 'name':'yser',\
    'domain':'google.com', 'pass':'', 'path':'/a/b', 'port':'80', 'schema':'http'}
    assert URL_to_dict("http://:pass@google.com:80/a/b") == None
    assert URL_to_dict("http://yser:@google.com:80/a/b") == None
    assert URL_to_dict("http://@google.com:80/a/b") == None
    assert URL_to_dict("://yser:pass@google.com:80/a/b") == None
    assert URL_to_dict("http:yser:pass@google.com:80/a/b") == None
    assert URL_to_dict("http://yser:pass@:80/a/b") == None

    print "Test URL passed ok!"

def testJoinURL():
    assert joinURL("http://a.com/x", "http://b.com") == "http://b.com/x"
    assert joinURL("http://a.com/x", "/a/b/c") == "http://a.com/a/b/c"
    assert joinURL("http://a.com/x", "a/b/c") == "http://a.com/x/a/b/c"
    assert joinURL("//a.com/x", "a/b/c") == None
    assert joinURL("", "") == None
    assert joinURL("", "a/b/c") == None
    assert joinURL("http://a.com/x", "") == "http://a.com/x"

    print "Test joinURL passed ok!"

def testUrlLinks():
    for i in urlLinks("http://google.com", 2):
        print i

def main():
    testURL()
    testJoinURL()
    testUrlLinks()

if __name__ == "__main__":
    exit(main())