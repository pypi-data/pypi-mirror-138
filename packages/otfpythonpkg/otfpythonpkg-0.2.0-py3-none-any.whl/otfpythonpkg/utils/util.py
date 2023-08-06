import sys
import os
import getopt
import configparser
import logging
import json

from datetime import datetime
from Amazon import S3Client

import SMTPMailer 
import Amazon
from sys import stdout


def read_file(filename):
	file = open(filename, "r")

	str = file.read()

	file.close()
 
	return str

#########################################################################
#
# get_configuration:
#
# This function will return the configuration stored in the 
# configuration file "config.ini" located in the same directory
# as the script
#
# Returns:
#
# 	Instance of a two dimension array containing the configuration 
# 	values with first dimension the section and the second dimension 
# 	is the key
#
#########################################################################
def get_configuration(filename):
	config = configparser.ConfigParser()

	config.read(filename)

	return config


############################################################################
#
# get_environment:
#
# Retrieves the environment from configuration file
#
# Arguments:
#
#   None
#
# Returns:
#
# 	Name of the environment
#
############################################################################
def get_environment(config, appsection):
	configenv = config[appsection]["environment"].lower()

	if configenv == "dev" or configenv == "staging" or configenv == "sit" or configenv == "prod" or configenv == "prodread":
		environ = configenv
	else:
		raise Exception("Invalid configuration value [{}] for environment. Valid values are: 'dev', 'staging', 'sit', 'prod', or 'prodread'".format(configenv))

	return environ

def get_db_environment(config, appsection):
	configenv = config[appsection]["dbenvironment"].lower()

	if configenv == "dev" or configenv == "staging" or configenv == "sit" or configenv == "prod" or configenv == "prodread":
		environ = configenv
	else:
		raise Exception("Invalid configuration value [{}] for dbenvironment. Valid values are: 'dev', 'staging', 'sit', 'prod', or 'prodread'".format(configenv))

	return environ

def get_s3_environment(config, appsection):
	configenv = config[appsection]["s3environment"].lower()

	if configenv == "dev" or configenv == "staging" or configenv == "prod":
		environ = configenv
	else:
		raise Exception("Invalid configuration value [{}] for s3environment. Valid values are: 'dev', 'staging', or 'prod'".format(configenv))

	return environ

def get_snowflake_environment(config, appsection):
	configenv = config[appsection]["snowflakeenvironment"].lower()

	if configenv == "dev" or configenv == "staging" or configenv == "prod":
		environ = configenv
	else:
		raise Exception("Invalid configuration value [{}] for snowflakeenvironment. Valid values are: 'dev', 'staging', or 'prod'".format(configenv))

	return environ

def get_commandline_arguments(longargs):

	myopts, args = getopt.getopt(sys.argv[1:], '', longargs)

	args = {}

	for k,v in myopts:
		args.update({ k.replace('--', '') : v})

	return args
      
def get_default_config_filename():
	return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "config" + os.path.sep + "config.ini"		

def get_default_config_path():
	return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "config" + os.path.sep	


############################################################################
#
# get_config_filename:
#
# Retrieves the configuration filename from the command line arguments
#
# Arguments:
#
#   None
#
# Returns:
#
# 	Configuration filename
#
############################################################################
def get_config_filename():
	default_cfilename = get_default_config_filename()		
 
	if len(sys.argv) == 1:
		cfilename = default_cfilename
	else:
		cfilename = sys.argv[1]

	return cfilename

"""
def send_email(mailHost, mailUsername, mailPassword, mailPort, mailFrom, mailTo, mailCC, mailSubject, msg):
	mail = MAIL.SMTPMailer()
 
	mail.send(mailHost, mailUsername, mailPassword, mailPort, mailFrom, mailTo, mailCC, mailSubject, msg)
"""

def get_dbconfig(config, env):
	return config[env + "-rds-database"]

def create_logger(logdir, logginglevel, fileprefix):
	d = datetime.today()

	logfilename = "{}{}_{}{}{}.log".format(logdir, fileprefix, d.year, str(d.month).rjust(2, '0'), str(d.day).rjust(2, '0'))

	logging.basicConfig(filename=logfilename, level=logginglevel, format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
															datefmt='%Y-%m-%d %H:%M:%S' )

def get_log_directory(config, scriptSectionName):
	logdirectory = config[scriptSectionName]["logdir"]

	if (logdirectory.endswith(os.path.sep) == False):
		logdirectory = logdirectory + os.path.sep

	return logdirectory
    
def get_logging_level(config, scriptSectionName):
	if config[scriptSectionName]["loglevel"].lower() == "debug":
		loglevel = logging.DEBUG
	elif config[scriptSectionName]["loglevel"].lower() == "info":
		loglevel = logging.INFO
	elif config[scriptSectionName]["loglevel"].lower() == "warning":
		loglevel = logging.WARNING
	else:
		loglevel = logging.ERROR

	return loglevel

    
def getJsonConfig(fileName):
	with open(fileName)  as f:
		jsonConfig = json.load(f)
  
	return jsonConfig

def getS3Configuration(config, env):
	return config[env + "-s3"]

def getBaseFilename(filename, separator = "/"):
	parts = filename.split(separator)
	return parts[len(parts) - 1]

def getCommandLineArguments(shortOpts, longOpts):
	try:
		opts, args = getopt.getopt(sys.argv[1:], shortOpts, longOpts)
	except getopt.GetoptError as err:
		print(str(err))
		return None

	args = {}

	for o, a in opts:
		args[o] = a

	return args

def pandas_to_csv_file(df, filename):
	csvdata = df.to_csv(index=False, line_terminator="\n")

	try:
		fh = open(filename, "w")
		fh.write(csvdata)
		fh.close()
	except Exception as e:
		print("Error writing to file {}: {}".format(filename, e))
		sys.exit(2)

def set_library_log_level(libname, loggingLevel):
	root = logging.getLogger(libname)
	root.setLevel(loggingLevel)
#	handler = logging.StreamHandler(sys.stdout)
#	handler.setLevel(loggingLevel)
#	formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s - %(message)s')
#	handler.setFormatter(formatter)
#	root.addHandler(handler)

def init_logging_to_screen(loggingLevel):
	root = logging.getLogger()
	root.setLevel(loggingLevel)

	handler = logging.StreamHandler(sys.stdout)
	handler.setLevel(loggingLevel)
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s:%(lineno)s - %(message)s')
	handler.setFormatter(formatter)
	root.addHandler(handler)

def get_filenames_to_process(s3Client, appConfig, interactive=False):
    try:
        filenames = s3Client.getFilenames(appConfig["s3"]["source_bucket"],
                                            appConfig["s3"]["source_incoming_path"],
                                            appConfig["s3"]["source_file_prefix"], None)
    except Exception as e:
        raise Exception(f"Error retriving S3 files names: {e}")

    if len(filenames) == 0:
        return []

    fileNamesToProcess = []

    if len(filenames) > 1 and interactive:
        choices = []

        print("")
        print("Possible files to process:\n")

        maxLen = 0

        for file in filenames:
            f = file['filename'].split("/")
            fname = f[len(f) - 1]
            if len(fname) > maxLen:
                maxLen = len(fname)

        print("{}  {}     File Date".format(" ".rjust(len(str(len(filenames)))),
                                            "Filename".ljust(maxLen)))
        print("{}  {}     ===================".format("=".rjust(len(str(len(filenames)))),
                                                        "=".ljust(maxLen, "=")))

    #        print("  " + "=".ljust(maxLen, "=") + "     ===================")

        choiceNum = 1

        for file in filenames:
            f = file['filename'].split("/")
            fname = f[len(f) - 1]
            choices.append(fname)
            print("{}  {}     {}".format(str(choiceNum).rjust(len(str(len(filenames)))),
                                            fname.ljust(maxLen),
                                            file['moddate'].strftime("%Y-%m-%d %H:%M:%S")))
            choiceNum = choiceNum + 1

        while True:
            c = input("\nEnter choice (1 to {}  0 to Quit): ".format(len(filenames)))
            if c.isnumeric() and int(c) >= 0 and int(c) <= len(filenames):
                break
        if int(c) == 0:
            os._exit(0)

        fileToProcess = choices[int(c) - 1]

        fileNamesToProcess.append(fileToProcess)
    else:
        for i, filename in enumerate(filenames):
            f = filenames[i]['filename'].split("/")
            fileNamesToProcess.append(f[len(f) - 1])

    return fileNamesToProcess

def get_input_from_user(prompt, required, possibleValues=None, convertToLower=True):
    while True:
        if not possibleValues is None:
            s = ""

            for str in possibleValues:
                if s != "":
                    s += ","
                s += str
    
            promptText = "{} (" + s + "): "
        else:
            promptText = "{} : "

        c = input(promptText.format(prompt)).strip()

        if convertToLower:
            c = c.lower()

        if required:
            if c == "":
                continue
        if possibleValues is not None:
            if c not in possibleValues:
                continue

        break

    return c


def get_boolean_input_from_user(prompt):
    while True:
        c = input("{}: ".format(prompt)).strip().lower()

        if c == "y" or c == "n":
            break

    if c == "y":
        return True

    return False


def get_int_input_from_user(prompt, required, defaultValue):
    while True:
        c = input("{}: ".format(prompt)).strip().lower()

        if required and c == "":
            c = int(defaultValue)
        else:
            if not c.isnumeric():
                continue

            c = int(c)

        break

    return c

def get_date_yyyymmddhhmmss():
    return datetime.now().strftime("%Y%m%d%H%M%S")

def log(msg, msgtype="INFO"):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  {msgtype}  {msg}")
    stdout.flush()
    


