{ pkgs }:
pkgs.stdenv.mkDerivation {
  pname = "riscv-rv64gc-toolchain";
  version = "2025.10.28";
  src = pkgs.fetchFromGitHub {
    owner = "riscv";
    repo = "riscv-gnu-toolchain";
    rev = "13385f4f06d67efe7c204955658cbec166757dce";
    sha256 = "sha256-QTjDc7uqnJP3bUo1h2s++yQGKiuAJVY1j+6BVMWb9gU=";
    fetchSubmodules = true;
  };

  configureFlags = [
    "--with-arch=rv64imafdc"
    "--with-abi=lp64d"
  ];

  installPhase = ":"; # 'make' installs on its own
  hardeningDisable = [ "all" ];
  enableParallelBuilding = true;

  # Stripping/fixups break the resulting libgcc.a archives, somehow.
  # Maybe something in stdenv that does this...
  dontStrip = true;
  dontFixup = true;

  nativeBuildInputs = with pkgs; [
    curl
    gawk
    texinfo
    bison
    flex
    gperf
  ];
  buildInputs = with pkgs; [
    libmpc
    mpfr
    gmp
    expat
  ];
}

