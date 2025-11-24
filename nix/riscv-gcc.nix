{ pkgs }:
pkgs.stdenv.mkDerivation {
  pname = "riscv-rv64gc-toolchain";
  version = "2025.10.28";
  src = pkgs.fetchFromGitHub {
    owner = "riscv";
    repo = "riscv-gnu-toolchain";
    rev = "13385f4f06d67efe7c204955658cbec166757dce";
    sha256 = "sha256-9aHe+2e6W/44Uu4SO2iHbhKRfQ/E7v87gstCN+Iv/yw=";
    fetchSubmodules = true;
  };

  configureFlags = [
    "--with-arch=rv64imafdc"
    "--with-abi=lp64d"
  ];

  preConfigure = ''
    for dir in binutils gcc gdb newlib dejagnu glibc musl qemu spike pkc; do
      if [ -d "$dir" ]; then
        mkdir -p "$dir/.git"
      fi
    done
  '';

  installPhase = ":"; 
  hardeningDisable = [ "all" ];
  enableParallelBuilding = true;

  dontStrip = true;
  dontFixup = true;

  nativeBuildInputs = with pkgs; [
    curl
    gawk
    texinfo
    bison
    flex
    gperf
    git
    util-linux
    perl
  ];
  buildInputs = with pkgs; [
    libmpc
    mpfr
    gmp
    expat
  ];
}
