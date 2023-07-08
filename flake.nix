{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  inputs.poetry2nix = {
    url = "github:nix-community/poetry2nix?ref=1.42.1";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        apibara-sdk = pkgs.poetry2nix.mkPoetryEnv {
          python = pkgs.python310;
          projectDir = ./.;
          editablePackageSources = {
            apibara = if builtins.getEnv "PROJECT_DIR" == "" then ./src else builtins.getEnv "PROJECT_DIR";
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

        devShells.default = apibara-sdk.env.overrideAttrs (oldAttrs: {
          LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";
          buildInputs = with pkgs; [
            stdenv.cc.cc.lib
            protobuf
            poetry
          ];
        });
      }
    );
}
