TIME_TO_RESEND = 3000 # 3s
TIME_TO_READ = 100 # old value 5000
TIME_SLEEP = 10000 # 10s
MAX_NUM_OF_SLEEP = 3
MAX_NUM_OF_RESEND = 5
TIME_TO_RE_READ_SERIAL = 200

lastSendOk = True
isReSend = False
isGotData = True

data = ""
savedData = ""
isComConnected = False
isReadOk = False

GOT_MSG = '!1#'
START_CHAR = '!'
END_CHAR = '#'
SEPARATE = ':'