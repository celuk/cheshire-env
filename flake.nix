{
  description = "The ultimate HDL dev env";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        #riscv_symlinks = pkgs.runCommand "riscv-unknown-elf-symlinks" {
        #  nativeBuildInputs = [ riscv_toolchain.gcc riscv_toolchain.binutils ];
        #} ''
        #  mkdir -p $out/bin
        #  GCC_BIN=${riscv_toolchain.gcc}/bin
        #  BINUTILS_BIN=${riscv_toolchain.binutils}/bin
        #  for tool in gcc g++; do
        #    ln -s "$GCC_BIN/riscv64-none-elf-$tool" "$out/bin/riscv64-unknown-elf-$tool"
        #  done
        #  for tool in as ar ld objcopy objdump ranlib readelf strip; do
        #    ln -s "$BINUTILS_BIN/riscv64-none-elf-$tool" "$out/bin/riscv64-unknown-elf-$tool"
        #  done
        #'';

        #markdown_grid_tables = pkgs.python311Packages.buildPythonPackage rec {
        #  pname = "markdown-grid-tables";
        #  version = "0.6.0";
#
        #  src = pkgs.fetchPypi {
        #    inherit pname version;
        #    sha256 = "sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
        #  };
#
        #  propagatedBuildInputs = [
        #    pkgs.python311Packages.markdown
        #  ];
        #};
        
        bender = pkgs.rustPlatform.buildRustPackage {
          pname = "bender";
          version = "0.27.1";
          src = pkgs.fetchCrate {
            pname = "bender";
            version = "0.27.1";
            sha256 = "sha256-Ofy1HW+xaGyEJ62L2+H5mZCPCBOn8AYbm4AoQkdpDt8=";
          };
          cargoSha256 = "sha256-JY5w27f+0tC6jN+9Wht1TDF+GfwxOEo1Xu0IWDhvKF4=";
        };

        #tclint = pkgs.python311Packages.buildPythonPackage rec {
        #  pname = "tclint";
        #  version = "0.4.2";
        #  format = "pyproject";
        #  
        #  src = pkgs.fetchPypi {
        #    inherit pname version;
        #    sha256 = "sha256-J9xD9oBKVg8IE70Lyjthc2n5kJ6duNYJkGZgs2fvFYM=";
        #  };
#
        #  nativeBuildInputs = [
        #    pkgs.python311Packages.setuptools
        #    pkgs.python311Packages.setuptools-scm
        #  ];
#
        #  propagatedBuildInputs = [
        #    pkgs.python311Packages.rich
        #    pkgs.python311Packages.tree-sitter
        #    pkgs.python311Packages.ply
        #    pkgs.python311Packages.schema
        #    pkgs.python311Packages.pathspec
        #    (pkgs.python311Packages.importlib-metadata.overridePythonAttrs (old: {
        #      version = "6.8.0";
        #      src = pkgs.fetchPypi {
        #        pname = "importlib-metadata";
        #        version = "6.8.0";
        #        sha256 = "1ea3a758782a200a0e2831818b6284f18ee0a57a052822a10f77977a45a16315";
        #      };
        #    }))
        #  ];
#
        #};

      in
      {
        devShells.default = pkgs.mkShell {
          shellHook = ''
            export CSMITH_INCLUDE=${pkgs.csmith}/include/${pkgs.csmith.name}
            export RISCV=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}
            export RISCV_PREFIX=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin/riscv64-unknown-elf-
            export RISCVTYPE=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin/riscv64-unknown-elf
            export BENDER=bender
            export CXX_PATH=g++
            export CHS_SW_GCC_BINROOT=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin
            export CHS_SW_DTC=dtc
            export NIX_PYTHONPATH=$PYTHONPATH
            export PATH=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin:$PATH
          '';
          packages = [
            pkgs.bashInteractive

            (pkgs.pkgsCross.riscv64-embedded.buildPackages.gcc)

            pkgs.pkgsCross.riscv64-embedded.stdenv.cc

            #riscv_linux_toolchain.gcc

            #riscv_symlinks

            pkgs.autoconf
            pkgs.csmith
            (pkgs.spike.overrideAttrs (oldAttrs: {
              configureFlags = oldAttrs.configureFlags or [ ] ++ [ "--enable-commitlog" ];
            }))
            pkgs.dtc
            pkgs.gnumake
            pkgs.cmake
            pkgs.unzip
            pkgs.cargo
            pkgs.rustc
            bender
            #tclint

            pkgs.verilator
            pkgs.verilog
            pkgs.gtkwave
            pkgs.yosys
            pkgs.xdot
            pkgs.netlistsvg
            pkgs.inkscape
            pkgs.sioyek
            pkgs.symbiyosys
            pkgs.boolector
            pkgs.yices
            pkgs.z3
            pkgs.avy
            pkgs.python311
            (pkgs.python311Packages.cocotb.overrideAttrs (oldAttrs: {
              patches = oldAttrs.patches or [ ] ++ [ ./nix/cocotb_pre_cmd.patch ];
            }))

            pkgs.python311Packages.requests
            pkgs.python311Packages.hjson
            pkgs.python311Packages.mako
            pkgs.python311Packages.pyyaml
            pkgs.python311Packages.tabulate
            pkgs.python311Packages.yapf
            pkgs.python311Packages.mkdocs
            pkgs.python311Packages.mkdocs-material
            pkgs.python311Packages.flatdict
            #markdown_grid_tables

            pkgs.python311Packages.mypy
            pkgs.python311Packages.pytest
            pkgs.python311Packages.riscof
            pkgs.python311Packages.pyserial
            
            (pkgs.callPackage ./nix/questa.nix { })
          ];
        };
      });
}
