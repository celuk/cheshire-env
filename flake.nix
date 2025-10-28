{
  description = "The ultimate HDL dev env";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";
  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in
      {
        devShells.default = pkgs.mkShell {
          shellHook = ''
            export PORT_DIR=riscv32-baremetal

            export CSMITH_INCLUDE=${pkgs.csmith}/include/${pkgs.csmith.name}

            export RISCV=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}
            export RISCV_PREFIX=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin/riscv32-unknown-elf-
            export RISCVTYPE=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin/riscv32-unknown-elf
            export PATH=${(pkgs.callPackage ./nix/riscv-gcc.nix { })}/bin:$PATH
          '';
          packages = [
            pkgs.bashInteractive # This is a must

            (pkgs.pkgsCross.riscv32-embedded.buildPackages.gcc)

            pkgs.autoconf
            pkgs.pkgsCross.riscv32-embedded.stdenv.cc
            pkgs.csmith
            (pkgs.spike.overrideAttrs (oldAttrs: {
              configureFlags = oldAttrs.configureFlags or [ ] ++ [ "--enable-commitlog" ];
            }))
            pkgs.dtc
            pkgs.gnumake

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

            pkgs.python311Packages.mypy
            pkgs.python311Packages.pytest
            pkgs.python311Packages.riscof
            pkgs.python311Packages.pyserial

            # QuestaSim
            (pkgs.callPackage ./nix/questa.nix { })
            ## QuestaSim + Quartus
            # (pkgs.quartus-prime-lite.override {
            #   supportedDevices = ["Cyclone V"];
            # })
          ];
        };
      }
    );
}
