let sources = import ./nix/sources.nix { }; in
{ nixpkgs ? sources.nixpkgs or <nixpkgs>, pkgs ? import nixpkgs {} }:

let
  inherit (import sources.niv { inherit pkgs; }) niv;

  python = pkgs.python3;
  pyPkgs = python.pkgs;
in
pkgs.mkShell {
  nativeBuildInputs = [
    niv
  ];

  buildInputs = [
    pyPkgs.pyglet
    python
    pyPkgs.simplejson
  ];
}
