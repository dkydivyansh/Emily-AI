import subprocess
import re
from dta import *
import time
def funappopen(input_string,play_sound,voice,main):
    to_return = 0
    play_sound(r'assets\sounds\msg_out.wav')
    try:
        if 'OPENCAM3453' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENCAM3453', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "microsoft.windows.camera:"], shell=True)
        if 'OPENCALCULATOR3432' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENCALCULATOR3432', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "calc.exe"], shell=True)
        if 'OPENGALLERY345' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENGALLERY345', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run('powershell.exe start ms-photos:', check=True)
        if 'OPENBROUSER5456' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENBROUSER5456', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(['start', 'https://www.google.com/'], shell=True, check=True)
        if 'OPENYOUTUBE3443' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENYOUTUBE3443', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(['start', 'https://www.youtube.com/'], shell=True, check=True)
        if 'OPENSETTINGS67346' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENSETTINGS67346', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "ms-settings:"], shell=True)
        if 'OPENSPOTIFY4543' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENSPOTIFY4543', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "spotify:"], shell=True)
            time.sleep(1)
            result = subprocess.run('tasklist | findstr /i "Spotify.exe"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                pass
            else:
                subprocess.run(['start', 'https://open.spotify.com/'], shell=True, check=True)
                pass
        if 'OPENWHATSAPP343' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENWHATSAPP343', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "whatsapp:"], shell=True)
            time.sleep(1)
            result = subprocess.run('tasklist | findstr /i "WhatsApp.exe"', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                pass
            else:
                subprocess.run(['start', 'https://web.whatsapp.com/'], shell=True, check=True)
                pass
        if 'OPENEMAIL78474' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENEMAIL78474', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["start", "mailto:"], shell=True)
        if 'OPENFILEMANAGRE345' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENFILEMANAGRE345', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["explorer", "shell:MyComputerFolder"], shell=True)

        if 'OPENNOTEPAD3433' in input_string:
            to_return = 1
            input_string = input_string.replace('OPENNOTEPAD3433', '')
            input_string = re.sub(r'[^\w\s,.!?\'\":-]', '', input_string)
            input_string = ' '.join(input_string.split())
            subprocess.run(["notepad.exe"], shell=True)


        if to_return == 1:
            print(con_ai+bgreen+'Emily : '+bcyan+input_string+nc)
            voice(input_string)
            main()
        else:
            return
    except:
        pass
