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

              # fix `No module named XXX`.
              tomli = super.tomli.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ self.flit-core ];
              });
              typing-extensions = super.typing-extensions.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ self.flit-core ];
              });
              pathspec = super.pathspec.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ self.flit-core ];
              });

              # add missing build tools
              iniconfig = super.iniconfig.overridePythonAttrs (old: {
                buildInputs = (old.buildInputs or [ ]) ++ [ self.setuptools self.hatchling self.hatch-vcs ];
              });
            }
          );
        };
      in
      {
        formatter = pkgs.nixpkgs-fmt;

        devShells.default = apibaraEnv.env.overrideAttrs (old:
          {
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
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
