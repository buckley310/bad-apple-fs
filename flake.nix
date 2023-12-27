{
  outputs = { nixpkgs, ... }:
    let
      forAllSystems = nixpkgs.lib.genAttrs [ "x86_64-linux" ];
    in
    {
      packages = forAllSystems (system:
        let
          inherit (nixpkgs.legacyPackages.${system}) pkgs;
          py = pkgs.python3.withPackages (p: [ p.opencv4 p.fusepy ]);
        in
        {
          default = pkgs.writeShellScriptBin "play" ''
            ${py}/bin/python play.py "$@"
          '';
          gen = pkgs.writeShellScriptBin "gen" ''
            ${py}/bin/python gen.py "$@"
          '';
        }
      );
    };
}
