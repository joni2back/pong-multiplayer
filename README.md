# Pong multiplayer

Pong multiplayer is a Table-Tennis game that supports LAN multiplayer (and singleplayer).

* Written in python with pyglet
* Using socket connections to share data with the server

## TODO
* Game pause
* GUI to define server
* Mouse support

## Running

Before running anything, clone the repository:
```bash
git clone https://github.com/joni2back/pong-multiplayer
cd pong-multiplayer
```

### Running server
```bash
sudo pip install pyglet
vim src/lib/settings.py # in order to define the server ip and port
python ./src/server.py
```

Alternatively, with [Nix][nix]:
```bash
vim src/lib/settings.py # in order to define the server ip and port
nix-shell --pure --run './src/server.py'
```

### Running client
```bash
vim src/lib/settings.py # in order to define server connection ip and port
python src/client.py
```

Alternatively, with [Nix][nix]:
```bash
vim src/lib/settings.py # in order to define the server ip and port
nix-shell --pure --run './src/client.py'
```


[nix]: https://nixos.org/nix/
