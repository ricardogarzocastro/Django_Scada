from variables import OpenOPC

def read(server,name):
    try:
        opc = OpenOPC.open_client('localhost')
        opc.connect(server) 
        value, quality, time = opc.read(name)
        access_rights=opc.properties(name, id=5)
        opc.close()
        value=str(value)
        return value,quality,access_rights,time
    except Exception:
        opc.close()
        return None,'Error',None,None
    
def write(server,name,value,response_array):
    try:
        opc = OpenOPC.open_client('localhost')
        opc.connect(server) 
        #Write operation returns "success" if write is sucessful
        if value:
            a=opc.write((name,value))
        else:
            a=''#if user enters no value, no written operation is done
        response_array.append(a.lower())
        return response_array
    except Exception:
        response_array.append('error')
        return (response_array)
    
    
    
    