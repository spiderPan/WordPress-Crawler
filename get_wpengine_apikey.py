import glob
import re

WP_CONFIG_FILES = glob.glob("x:/sites/*/wp-config.php")
OUTPUT_FILE = './WPEN_site_api.txt'
RESULT = ''


for WP_CONFIG_FILE in WP_CONFIG_FILES:
	searchfile = open(WP_CONFIG_FILE,'r')
	name = api = ""
	for line in searchfile:
		if 'PWP_NAME' in line:
			name = re.findall(r'\'(.*?)\'', line)[1]
		if 'WPE_APIKEY' in line:
			api = re.findall(r'\'(.*?)\'', line)[1]
		
	searchfile.close()
	if name and api:
		RESULT += "{0} {1} \n".format(name,api)


outputfile = open(OUTPUT_FILE,'w')
outputfile.write(RESULT)
outputfile.close()
