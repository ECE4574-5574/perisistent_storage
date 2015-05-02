import dateutil.parser
GET_FUNCTION_TOKEN_RANGES = {\
            'HD': '2', 'RD': '3', 'HT': '3', 'RT': '4',\
            'BU': '2,3', 'BH': '2,3', 'BR': '3', 'BD': '4',\
            'AL': '4-6', 'AT': '6-7', 'AI': '6-7',\
            'CL': '4-6', 'CT': '6-7', 'CI': '6-7', 'DD': '4',\
            'IU': '3', 'TU': '2'}
POST_FUNCTION_TOKEN_RANGES = {'D': '4', 'R': '2', 'H': '1', 'U': '3', 'UBU': '2', 'UPU': '3', 'UTU': '3', 'UH':'2', 'UR':'3', 'UD':'4', 'H': '1', 'RESET': '1'}
PATCH_FUNCTION_TOKEN_RANGES = {'A': '4-7', 'C': '4-7'}
DELETE_FUNCTION_TOKEN_RANGES = {'A': '2', 'D': '4', 'R': '3', 'H': '2'}
FUNCTION_HOUSE_ID_LOCATIONS = {\
  'HD':1, 'RD':1, 'HT':1, 'RT':1, 'BH':1, 'D':1,\
  'R':1, 'H':1, 'BR':1, 'BD':1, 'DD':1, 'UH':1, 'UR':1, 'UD':1, 'AL':4,\
  'CL':4, 'A':3, 'C':3, 'AT':5, 'AI':5, 'CT':5, 'CI':5}

def validateGetRequest(path): 
    tokenizedPath = path.strip('/').split('/')
    if not tokenizedPath[0] in GET_FUNCTION_TOKEN_RANGES:
        return False
    return (isInRange(len(tokenizedPath), GET_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

def validatePostRequest(path):
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
   
    if tokenizedPath[0] == 'HD' or tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'HT' or tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'BH' or tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R' or tokenizedPath[0] == 'H' or tokenizedPath[0] == 'BR' or tokenizedPath[0] == 'BD' or tokenizedPath[0] == 'DD' or tokenizedPath[0] == 'UH' or tokenizedPath[0] == 'UR' or tokenizedPath[0] == 'UD':
        return tokenizedPath[1]
    elif tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C':
        return tokenizedPath[3]
    elif (tokenizedPath[0] == 'AL' and len(tokenizedPath) > 4) or (tokenizedPath[0] == 'CL' and len(tokenizedPath) > 4):
        return tokenizedPath[4]
    elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
        return tokenizedPath[5]
    else:
        return None

def getUserID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'BU' or tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI' or tokenizedPath[0] == 'U' or tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C' or tokenizedPath[0] == 'UU' or tokenizedPath[0] == 'TU' or tokenizedPath[0] == 'UBU' or tokenizedPath[0] == 'UPU' or tokenizedPath[0] == 'UTU':
        return tokenizedPath[1]
    else:
        return None

def getUserName(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'U' or tokenizedPath[0] == 'IU':
        return tokenizedPath[1]
    else:
        return None

def getUserPass(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'IU' or tokenizedPath[0] == 'U' or tokenizedPath[0] == 'UPU':
        return tokenizedPath[2];
    else:
        return None
      

def getUserToken(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'UTU':
        return tokenizedPath[2];
    else:
        return None
    
def getRoomID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'RD' or tokenizedPath[0] == 'RT' or tokenizedPath[0] == 'DD' or tokenizedPath[0] == 'BR' or tokenizedPath[0] == 'UR' or tokenizedPath[0] == 'UD':
        return tokenizedPath[2]
    elif (tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'CL') and len(tokenizedPath) > 3:
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
        return tokenizedPath[6]
    elif tokenizedPath[0] == 'D' or tokenizedPath[0] == 'R' or tokenizedPath[0] == 'BD':
        return tokenizedPath[2]
    elif (tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C'):
        return tokenizedPath[4]
    else:
        return None

def getDeviceID(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'DD' or tokenizedPath[0] == 'UD':
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CI':
        return tokenizedPath[4]
    elif tokenizedPath[0] == 'A':
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'D':
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'C':
        return tokenizedPath[5]
    elif tokenizedPath[0] == 'BD':
        return tokenizedPath[3]
    else:
        return None

def getDeviceType(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'HT':
        return tokenizedPath[2]
    elif tokenizedPath[0] == 'RT': 
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'CT':
        return tokenizedPath[4]
    elif tokenizedPath[0] == 'D':
        return tokenizedPath[3]
    elif tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C':
        return tokenizedPath[6]
    else:
        return None

def getTimeFrame(path):
    tokenizedPath = path.strip('/').split('/')
    if tokenizedPath[0] == 'A' or tokenizedPath[0] == 'C':
        return tokenizedPath[2]
    elif tokenizedPath[0] == 'AL' or tokenizedPath[0] == 'AT' or tokenizedPath[0] == 'AI' or tokenizedPath[0] == 'CL' or tokenizedPath[0] == 'CT' or tokenizedPath[0] == 'CI':
        return [tokenizedPath[2], tokenizedPath[3]]
    else:
        return None 

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
