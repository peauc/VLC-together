# VLC-together
###### A straightforward way to link multiple VLC client together

## Description
This is a fun project started from the [blog post of Marios Zindilis](https://zindilis.com/blog/2016/10/23/control-vlc-with-python.html). There is two binaries, a client and a server.   
The server is hosting rooms for users to connect on. While in a room all the user's VLC input are synchronised.
**The media file must be local to clients** (for now).

## Technical information
I wanted to do a project as barebone as possible, using the least amount of libraries possible to improve my python skills.

Python 3.7+  
Google Protobuf on a custom protocol

##Usage
There is a `Common` package in the project. 
To start the scripts please add the project root directory to your `PYTHONPATH` env variable.
The examples below assume your current directory is the project root directory.  

#### Client
add `env PYTHONPATH=.` to your environment variables and execute `python3 Client/main.py`
The client will ask you for the ip and port
#### Server
add `env PYTHONPATH=.` to your environment variables and execute `python3 Server/main.py`
You can define on which host and port the server will listen on
