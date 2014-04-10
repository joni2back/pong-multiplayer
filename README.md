#### Pong multiplayer is a Table-Tennis game that support lan multiplayer (and singleplayer)

* Written in python with pyglet
* Using socket connections to share data with the server

##### TODO
* Game pause
* GUI to define server
* Mouse support


**Running server**
```bash
sudo pip install pyglet
git clone https://github.com/joni2back/pong-multiplayer.git
cd pong-multiplayer/src
vim lib/settings.py #in order to define the server ip and port
python server.py
```

**Running client**
```bash
sudo pip install pyglet
git clone https://github.com/joni2back/pong-multiplayer.git
cd pong-multiplayer/src
vim lib/settings.py #in order to define server connection ip and port
python client.py
```
