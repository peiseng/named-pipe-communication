import time
import win32pipe, win32file, pywintypes

def named_pipe_client():
    print("Named_Pipe_Client.")
    # After connected to server for 3 times, it will automatically stop. 
    for cnt in range (3): 
        print(f"Service {cnt+1} is started.")
        while True:
            try:
                # Open the named pipe 
                handle = win32file.CreateFile(r'\\.\pipe\ABC',win32file.GENERIC_READ | win32file.GENERIC_WRITE, 
                    0, None, win32file.OPEN_EXISTING, win32file.FILE_ATTRIBUTE_NORMAL, None)
                # Set the read or blocking mode of the named pipe
                res = win32pipe.SetNamedPipeHandleState(handle, win32pipe.PIPE_READMODE_MESSAGE, None, None)
                if res == 0:
                    print(f"SetNamedPipeHandleState Return Code: {res}")   # if function fails, the return value will be zero
                while True:
                    # Read the data from the named Pipe
                    resp = win32file.ReadFile(handle, 65536)
                    print(f"Data Received: {resp}")   # if function fails, the return value will be zero
            except pywintypes.error as e:
                if e.args[0] == 2:   # ERROR_FILE_NOT_FOUND
                    print("No Named Pipe")
                elif e.args[0] == 109:   # ERROR_BROKEN_PIPE
                    print("Named Pipe is broken")
                break
        print("Service {} is ended.\n".format(cnt+1))
        # Pause for 0.2 second
        time.sleep(0.2)

if __name__ == '__main__':
    named_pipe_client()