from datetime import datetime

string = 'Tokyo | 17 Dec 2004 '

dt_obj = datetime.strptime(string, '%d %b %Y')
print(dt_obj.timestamp())


