{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-22.11";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };
        apibaraEnv = pkgs.poetry2nix.mkPoetryEnv {
          projectDir = ./.;
          editablePackageSources = {
            apibara = ./src;
          };
          overrides = pkgs.poetry2nix.overrides.withDefaults (
            self: super: {
              grpcio = super.grpcio.override {
                preferWheel = false;
              };
            }
          );
        };
      in
        {
          devShells.default = apibaraEnv.env.overrideAttrs (old:
            {
              LD_LIBRARY_PATH= "${pkgs.stdenv.cc.cc.lib}/lib";
              buildInputs = with pkgs; [
                stdenv.cc.cc.lib
                protobuf
                poetry
              ];
            }
          );
        }
    );
}