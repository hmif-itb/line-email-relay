import os
import sys


config = dict()
config_keys = ['secret', 'access_token', 'email_domain', 'chat_timeout', 'smtp_host', 'smtp_port', 'smtp_user', 'smtp_password', 'recipient_email', 'recipient_name', 'enquiry_received_reply']

if ('--dev' in sys.argv):
    with open('.env', 'r') as envfile:
        envs = envfile.read()
        for env in envs.split('\n'):
            keypair = env.split('=')
            config[keypair[0]] = keypair[1]
    for key in config_keys:
        if (key not in config):
            raise Exception('{} not found in .env'.format(key))
else:
    for key in config_keys:
        config[key] = os.environ[key]
