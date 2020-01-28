import time
from datetime import datetime 
import win32pipe, win32file, pywintypes

def named_pipe_server():
    print("Named_Pipe_Server.")
    # After 3 clients are connected to it, it will automatically stop providing the service. 
    for cnt in range (3): 
        print("Service {} is started.".format(cnt+1))
        # Create named pipe
        pipe = win32pipe.CreateNamedPipe(r'\\.\pipe\ABC', win32pipe.PIPE_ACCESS_DUPLEX, 
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
            1, 65536, 65536, 0, None)
        print("Named Pipe is created. Waiting for Client to connect.")
        # Enable named pipe and wait for client connection
        win32pipe.ConnectNamedPipe(pipe, None)
        print("Client is conencted.")
        for count in range (10):
            # Obtain current date time in predefined format
            now = datetime.now()
            if cnt%2 == 0:
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            else:
                dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
            # Encode the string to ASCII
            some_data = str.encode(dt_string, encoding="ascii")
            # Send the encoded string to client
            err, bytes_written=win32file.WriteFile(
                pipe, 
                some_data
            )
            print(f"Count: {count+1}, Data Sent: {some_data}")
            print(f"WriteFile Return Code: {err}, Number of Bytes Written: {bytes_written}")
            # Pause for 0.2 second
            time.sleep(0.2)
        # Ensure all data read by client
        win32file.FlushFileBuffers(pipe)
        # Disconnect the named pipe
        win32pipe.DisconnectNamedPipe(pipe)
        # CLose the named pipe
        win32file.CloseHandle(pipe)
        print(f"Server {cnt+1} is ended.")
        print("\n")

if __name__ == '__main__':
    named_pipe_server()