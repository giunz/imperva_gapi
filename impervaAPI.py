#!/usr/bin/python3.5
from requests import get
import os
import json
import logging
import sys
import urllib3
import ssl
import certifi
import configparser
import requests

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
headers = {'content-type': 'application/json'}
config = configparser.ConfigParser()
try:
  config.read('settings.ini')
  host = config['DEFAULT']['host']
  user = config['DEFAULT']['user']
  password= (config['DEFAULT']['password'])
except KeyError:
  logging.info("No configurations file found.")

logging.debug("Using Hostname "+host)
logging.debug("Using Username "+user)
logging.debug("Using Password "+password)

def login():
 logging.info('Logging in.')
 r = requests.post(host+'/SecureSphere/api/v1/auth/session', headers=headers ,auth=(user, password),verify=False)
 c = r.cookies['JSESSIONID']
 if (r.status_code == 200):
  logging.info('Successfully logged in.')
 else:
  logging.error('An error occured. Status code is '+r.status_code)
 return c

def logout(b):
 logging.info('Logging out')
 r = requests.delete(host+'/SecureSphere/api/v1/auth/session', headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  logging.info('Logged out successfully.')
 else:
  logging.error('An error occured. Status code is '+r.status_code)

def getAllSites(b):
 logging.info('Getting Sites.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/sites', headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  sites = r.json()
  logging.info('Retrieved the sites successfully.')
  logging.debug(str(sites))
  return sites
 else:
  logging.error('An error occured. Status code is '+r.status_code)

def getAllServerGroups(b,site):
 logging.info('Getting Server Groups.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/serverGroups/'+site, headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  server_groups = r.json()
  logging.info('Retrieved the Server Groups successfully.')
  logging.debug(str(server_groups))
  return server_groups
 else:
  logging.error('An error occured. Status code is '+r.status_code)

def getAllWebServices(b,site,server_group):
 logging.info('Getting Web Services.')
 r = requests.get(host+'/SecureSphere/api/v1/conf/webServices/'+site+'/'+server_group, headers=headers, cookies=b,verify=False)
 if (r.status_code == 200):
  ws = r.json()
  logging.info('Retrieved the Web Services successfully.')
  logging.debug(str(ws))
  return ws
 else:
  logging.error('An error occured. Status code is '+r.status_code)

cookies=login()
logging.debug('JSESSIONID is '+cookies)
c = {'JSESSIONID':cookies}
sites = getAllSites(c)
logging.debug('First site\'s name is.... '+sites['sites'][0])
site=sites['sites'][0]
server_groups = getAllServerGroups(c,site)
logging.debug('First Server Group\'s name for site '+site+' is.... '+server_groups['server-groups'][0])
sg=server_groups['server-groups'][0]
ws=getAllWebServices(c,site,sg)
logging.debug('First service\'s name for site '+site+' and Server Group '+sg+' is '+ws['web-services'][0])
logout(c)
