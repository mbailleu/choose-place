with import <nixpkgs> {};
python3.pkgs.buildPythonApplication {
  name = "choose-place";
  src = ./.;
  propagatedBuildInputs = with python3.pkgs; [
    flask numpy
  ];
}
