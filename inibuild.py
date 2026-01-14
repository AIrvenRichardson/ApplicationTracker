import configparser

# First time making an ini file so I was just building one programmatically to see what it end up as in vscode

config = configparser.ConfigParser()
config['DEFAULT'] = {'dbdir': ''}
with open('cfg.ini', 'w') as configfile:
    config.write(configfile)