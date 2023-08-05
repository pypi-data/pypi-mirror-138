from d51_dirsync import sync
import argparse
import json
import ssl
import getpass
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def deploy(args):

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.load_cert_chain('..\\certificates\certificate.pem', '..\\certificates\\key.pem')

    with open('deploy.json') as json_file:
        deploy = json.load(json_file)

    for task in deploy[args.target]:
        if task['action'] == 'sync':
            if 'prompt' in task:
                prompt = task['prompt']
            else:
                prompt = False
            if prompt:
                do = input('Copy {} y or n: '.format(task['data']['source'])).lower()
            else:
                do = 'y'
            if do == 'y':
                if 'exclude' in task['options']:
                    task['options']['exclude'].append('config.js')
                    task['options']['exclude'].append('.env')
                else:
                    task['options']['exclude'] = ['config.js','.env']
                for server in task['data']['servers']:
                    if 'source' in task['data']:
                        sync(task['data']['source'],'\\\\' + server + '\\' + task['data']['dest'],'sync',**task['options'])
                    if 'env' in task['data']:
                        f = open('\\\\' + server + '\\' + task['data']['dest'] + '\\.env', "w+")
                        for key,value in task['data']['env'].items():
                            f.write('{key}={value}\r\n'.format(key=key,value=value))
                        f.close()
                    if 'config' in task['data']:
                        f = open('\\\\' + server + '\\' + task['data']['dest'] + '\\config.js', "w+")
                        json_formatted_str = "var config = " + json.dumps(task['data']['config'],indent=4) 
                        f.write(json_formatted_str)
                        f.write("\n")
                        f.write("\n")
                        f.write("var __config = {...config}")
                        f.close()
                    if 'local' in task['data']:
                        f = open('\\\\' + server + '\\' + task['data']['dest'] + '\\local.js', "w+")
                        json_formatted_str = "var local = " + json.dumps(task['data']['local'],indent=4) 
                        f.write(json_formatted_str)
                        f.write("\n")
                        f.write("\n")
                        f.write("var __local = {...local}")
                        f.close()
                    if 'global' in task['data']:
                        f = open('\\\\' + server + '\\' + task['data']['dest'] + '\\global.js', "w+")
                        json_formatted_str = "var global = " + json.dumps(task['data']['global'],indent=4) 
                        f.write(json_formatted_str)
                        f.write("\n")
                        f.write("\n")
                        f.write("var __global = {...global}")
                        f.close()
                
                    
        elif task['action'] == 'restart':
            for server in task['data']['servers']:

                username = input('Username: ')
                password = getpass.getpass('Password: ')

                headers = {'Content-Type': 'application/json','Accept': 'application/json','username':username,'password':password}

                response=requests.post('{ssos}/login'.format(ssos=task['data']['ssos']), headers=headers, verify=False)

                auth = response.headers['auth']

                body = {'servicename':task['data']['appname']}

                headers = {'Content-Type': 'application/json','Accept': 'application/json','auth':auth}

                response = requests.post('https://{server}:{port}/restartservice'.format(server=server,port=task['data']['port']), json=body, headers=headers, verify=False)

                print('restarting', task['data']['appname'],'on',server)



