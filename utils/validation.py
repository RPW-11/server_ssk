import re
def validate_user(username, password):
    pattern = "^[a-zA-Z0-9_]+$"
    pattern2 = "^(?=.*[a-zA-Z])(?=.*[0-9])[a-zA-Z0-9_]+$"
    match = re.search(pattern, username)
    match2 = re.search(pattern2, password)
    if match and match2:
        return True
    return False


def count_trials(iptrials, ip):
    e = iptrials.get(ip)
    if e:
        iptrials[ip] += 1
        return
    iptrials[ip] = 1
    return


    
    
    