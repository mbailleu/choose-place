with import <nixpkgs> {};
python3.pkgs.buildPythonApplication {
  name = "choose-place";
  src = ./.;
  propagatedBuildInputs = with python3.pkgs; [ flask ];

  shellHook = ''
    export PATH=$PATH:${python3.pkgs.gunicorn}/bin
  '';
}
