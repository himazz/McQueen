import logging 
from functools import wraps 


def create_logger(): 	
	#create a logger object 
	logger = logging.getLogger('log') 
	logger.setLevel(logging.INFO) 
	#create a file to store all the 
	# logged exceptions 
	logfile = logging.FileHandler('log.log') 
	fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
	formatter = logging.Formatter(fmt) 
	logfile.setFormatter(formatter) 
	logger.addHandler(logfile) 
	
	return logger 

def exception(logger): 
	
	# logger is the logging object 
	# exception is the decorator objects 
	# that logs every exception into log file 
	def decorator(func): 		
		@wraps(func) 
		def wrapper(*args, **kwargs): 
			
			try: 
				return func(*args, **kwargs) 
			
			except: 
				issue = "exception in "+func.__name__+"\n"
				issue = issue+"-------------------------------------------------------------------------\n" 
				logger.exception(issue) 			
		return wrapper 
	return decorator 
