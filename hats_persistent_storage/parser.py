import dateutil.parser
GET_FUNCTION_TOKEN_RANGES = {\
            'HD': '2', 'RD': '3', 'HT': '3', 'RT': '4',\
            'BU': '2,3', 'BH': '2,3', 'BR': '3', 'BD': '4',\
            'AL': '3-5', 'AT': '6', 'AI': '6',\
            'CL': '3-5', 'CT': '6', 'CI': '6', 'DD': '4'}
POST_FUNCTION_TOKEN_RANGES = {'D': '4', 'R': '2', 'H': '1', 'U': '1'}
PATCH_FUNCTION_TOKEN_RANGES = {'A': '4-6', 'C': '4-6'}
DELETE_FUNCTION_TOKEN_RANGES = {'A': '2', 'D': '5', 'R': '4', 'H': '2', 'U': '2'}

def validateGetRequest(path): 
    tokenizedPath = path.strip('/').split('/')
    if not tokenizedPath[0] in GET_FUNCTION_TOKEN_RANGES:
        return False
    print tokenizedPath[0], len(tokenizedPath)
    return (isInRange(len(tokenizedPath), GET_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

def validatePostRequest(path):
        if (path == 'H' or path == 'U'):
            return True
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in POST_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), POST_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

      
def validatePatchRequest(path):
    tokenizedPath = path.strip('/').split('/')
    if not tokenizedPath[0] in PATCH_FUNCTION_TOKEN_RANGES:
        return False
    return (isInRange(len(tokenizedPath), PATCH_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))


def validateDeleteRequest(path):
    tokenizedPath = path.strip('/').split('/')
    if not tokenizedPath[0] in DELETE_FUNCTION_TOKEN_RANGES:
        return False
    return (isInRange(len(tokenizedPath), DELETE_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))


def getHouseID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'HD' or tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'HT' or tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'BH' or tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R' or tokenizedPath[0] == 'H' or tokenizedPath[0] == 'BR' or tokenizedPath[0] == 'BD' or tokenizedPath[0] == 'DD':
        return tokenizedPath[1]
    elif (tokenizedPath[0] == 'AL' and len(tokenizedPath) > 3) or tokenizedPath[0] == 'CL' or (tokenizedPath[0] == 'A' and len(tokenizedPath) >2) or tokenizedPath[0] == 'C':
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
        return tokenizedPath[4]
    else:
        return False

def getUserID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'BU' or tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI' or tokenizedPath[0] == 'U' or tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C':
        return tokenizedPath[1]
    else:
        return False
    
def getRoomID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'DD' or tokenizedPath[0] == 'BR':
        return tokenizedPath[2]
    elif tokenizedPath[0] == 'AL' and len(tokenizedPath) > 3:
        return tokenizedPath[4]
    elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R' or tokenizedPath[0] == 'BD':
        return tokenizedPath[2]
    elif (tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C') and len(tokenizedPath) > 4:
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'A':
        return tokenizedPath[1]
    else:
        return False

def getDeviceID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CI' or tokenizedPath[0] == 'DD':
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'D' and len(tokenizedPath) > 5:
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'D':#second d request
        return tokenizedPath[4]
    elif (tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C') and len(tokenizedPath) > 4:
        return tokenizedPath[4]
    elif tokenizedPath[0] == 'BD':
        return tokenizedPath[3]
    else:
        return False

def getDeviceType(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'HT':
        return tokenizedPath[2]
    elif tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'CT': 
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'D':
        return tokenizedPath[2]
    else:
        return False

def getVersion(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'D':
        return tokenizedPath[2]
    elif tokenizedPath[0] == 'R':
        return tokenizedPath[2]
    else:
        return False

def getTimeFrame(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI' or (tokenizedPath == 'A' and  len(tokenizedPath) > 2) or tokenizedPath[0] == 'C':
        return dateutil.parser.parse(tokenizedPath[2])
    else:
        return False

def isInRange(i, strRange):
    if '+' in strRange:
        min = int(strRange.split('+')[0])
        return i >= min

    allowable = []
    for onePart in strRange.split(','):
        if '-' in onePart:
            lo, hi = onePart.split('-')
            lo, hi = int(lo), int(hi)
            allowable.extend(range(lo, hi+1))
        else:
            allowable.append(int(onePart))
    
    return i in allowable
