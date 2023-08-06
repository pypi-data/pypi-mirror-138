import MR_Package
debug_mode = MR_Package.debug_mode

if debug_mode: print(__name__ + " loading")

from math import acos, asin, atan, cos, radians, sin, tan

vars = {}
operators = ["+", "-", "*", "/"]
winkelfunktionen = ["sin", "cos", "tan"]

def winkel(eval_string):
    print(eval_string)
    buffer = []
    for element in winkelfunktionen:
        if  element in eval_string:
            if element == "sin":
                print("sinus")
                replacement = eval_string.split("sin(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = sinus(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)
                
                #print("Replacement: " + str(replacement) + einheit)
            if element == "cos":
                print("cosinus")
                replacement = eval_string.split("cos(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = cosinus(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)

            if element == "tan":
                print("tangens")
                replacement = eval_string.split("tan(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = tangens(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)

            if element == "asin":
                print("arcus-sinus")
                replacement = eval_string.split("asin(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = arcus_sinus(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)

            if element == "acos":
                print("arcus-cosinus")
                replacement = eval_string.split("acos(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = arcus_cosinus(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)

            if element == "atan":
                print("arcus-tangens")
                replacement = eval_string.split("atan(")
                buffer.append(replacement[0])
                replacement = replacement[1]
                strbuff = replacement.split(")")
                replacement = strbuff[0]
                end = strbuff[1]
                print(replacement)
                result = arcus_tangens(float(replacement))
                print(result)
                buffer.append(result)
                buffer.append(end)

    print(buffer)
        
    return eval_string

def debug_check(printout=False):
    if debug_mode and printout:
        print("---------------CHECK_PASS----------------------")
    else:
        pass


def var(name, value):
    global vars
    vars[name] = value

def clear_var():
    global vars
    vars = {}

def get_var(name, printout=False):
    if debug_mode and printout:
        print(name + ": " + str(vars[name]))
    return vars[name]

def set_logger(logger, crit):
    global log, mail
    log = logger
    mail = crit

def error(function = "", params = ""):
    if debug_mode:
        print("An error occured in function: " + str(function))
    #mail.critical("Error in function: " + str(function) + "\nparameters: " + str(params))

def shorten(result):
    result = str(result)
    if len(result) > 10:
        return result
    else:
        return result
        

def calc(eval_string):
    if eval_string:
        if "/0" in eval_string:
           error("calc", eval_string)
           return "Devide by 0 Error"
        try:
            result = eval(eval_string)
            return shorten(result)
        except:
            try:
                new_eval = eval_string[:-1]
                new_res = eval(new_eval)    
                return new_res
            except:
                try:
                    new_eval = eval_string[:-2]
                    new_res = eval(new_eval)    
                    return new_res
                except:
                    error("calc", eval_string)

def change_eval(eval_string, var, mode="calc", printout=False):
    #modes: return / calc
    global vars
    list_new = []
    l = list(eval_string)
    if debug_mode and printout: 
        print(l)
    counter = 0
    for element in l:
        if var in element:
            if debug_mode and printout:
                print("Found!")
                print(vars[var])
            counter += 1
            try:
                if counter >= 1:
                    if debug_mode and printout:
                            print("--------L[cnt]------------ : " + l[counter])
                    if "+" == l[counter]:
                        debug_check()
                    elif "-" == l[counter]:
                        debug_check()
                    elif "*" == l[counter]:
                        debug_check()
                    elif "/" == l[counter]:
                        debug_check()
                    else:
                        if debug_mode and printout:
                            print("---------CHECK NOT PASSED---------------")
                        list_new.append("*")
            except:
                pass
            element = str(vars[var])
            
        list_new.append(element)
    eval_string = "".join(list_new)
    if debug_mode and printout:
        print(eval_string)
    if mode == "return":
        return eval_string
    if mode == "calc":
        try:
            result = calc(eval_string)
            return result
        except:
            error("change_eval", eval_string)

def multi_var_eval(eval_string, vars, mode="calc", printout=False):
    new_eval = ""
    if debug_mode and printout:
        print("[multi_var_eval] Eval_String:")
        print(str(eval_string))
        print("[multi_var_eval] Vars: " + str(vars)  )  
    new_eval = eval_string
    for element in vars:
        if debug_mode and printout:
            print("[multi_var_eval] Element: " + str(element))
        new_eval = change_eval(new_eval, element, "return")
        if debug_mode and printout:
            print("[multi_var_eval] new_eval: " + str(new_eval))
    if list(new_eval)[0] in operators:
       for element in operators:
           if new_eval.startswith(element):
               new_eval = new_eval.strip(element)
    for i in range(len(new_eval)):
        try:
            if list(new_eval)[i] in operators and list(new_eval)[i+1] in operators:
                l = list(new_eval)
                l.pop(i+1)
            new_eval = "".join(l)
        except:
            pass
    if debug_mode and printout:
        print(new_eval)
    if mode == "calc":
        return calc(new_eval)
    elif mode == "return":
        return new_eval
    else:
        error(multi_var_eval, new_eval)


def Matrix(x11=0, x12=0, x13=0, x21=0, x22=0, x23=0, x31=0, x32=0, x33=0, size="2x2"):
    if size == "2x2":
        x22 = x21
        x21 = x13
        Det = x11 * x22 - x12 * x21
        return Det
    elif size == "3x3":
        Det = (x11 * x22 * x33) + (x12 * x23 * x31) + (x13 * x21 * x32) - (x31 * x22 * x13) - (x32 * x23 * x11) - (x33 * x21 * x12)
        return Det
    else:
        error("matrix", params="Error in Matrix... Check input!")

def sinus(value):
    return sin(radians(value))

def cosinus(value):
    return cos(radians(value))

def tangens(value):
    return tan(radians(value))

def arcus_sinus(value):
    return asin(radians(value))

def arcus_cosinus(value):
    return acos(radians(value))

def arcus_tangens(value):
    return atan(radians(value))

if debug_mode: print(__name__ + " loaded!")