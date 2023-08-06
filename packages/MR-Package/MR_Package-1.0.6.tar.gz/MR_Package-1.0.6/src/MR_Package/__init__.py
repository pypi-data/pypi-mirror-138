#imports
import time

global debug_mode
debug_mode = True

global delay
delay = 0.05

global service_mail, admin_mail, password
service_mail = "" 
admin_mail = [""]
password = ""

print("__________________________________________")
time.sleep(delay)
print("  __  __ _____                            ")  
time.sleep(delay)                       
print(" |  \/  |  __ \                           ")  
time.sleep(delay)                      
print(" | \  / | |__) |                          ") 
time.sleep(delay)                   
print(" | |\/| |  _  /                           ")
time.sleep(delay)
print(" | |  | | | \ \                           ")
time.sleep(delay)
print(" |_|__|_|_|  \_\  _                       ")
time.sleep(delay)
print(" |  __ \         | |                      ")
time.sleep(delay)
print(" | |__) |_ _  ___| | ____ _  __ _  ___    ")
time.sleep(delay)
print(" |  ___/ _` |/ __| |/ / _` |/ _` |/ _ \   ")
time.sleep(delay)
print(" | |  | (_| | (__|   < (_| | (_| |  __/   ")
time.sleep(delay)
print(" |_|   \__,_|\___|_|\_\__,_|\__, |\___|   ")
time.sleep(delay)
print("                             __/ |        ")
time.sleep(delay)
print("                            |___/         ")
time.sleep(delay)
print("__________________________________________")


def get_logger():
    from MR_Package import logger
    from MR_Package import mail_log as mail
    global log, crit_log
    log = logger.logging
    crit_log = mail.logger
    logger.run()
    return log, crit_log

