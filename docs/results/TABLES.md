# Tables détaillées des observations historiques

Générées par `scripts/analyze_results.py`. Voir la [méthode et les limites](../BENCHMARK_RESULTS.md).

Les valeurs sont des médianes après retrait des lignes numériquement invalides. Les séries signalées restent visibles ici, même lorsqu’elles sont exclues des croisements exploratoires. Un même langage peut regrouper plusieurs blocs de mesures non datés. Aucun classement global n’est calculé.

## binary-trees

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L11) | 20/20 | 112.100 | 2.821 | 39.433 | 1.7 | aucun filtre déclenché |
| [C](../../C/C.csv#L11) | 20/20 | 47.377 | 1.123 | 41.782 | 2.2 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L11) | 20/20 | 47.986 | 1.106 | 42.553 | 3.0 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L11) | 10/10 | 273.056 | 10.825 | 25.197 | 1.3 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L11) | 20/20 | 281.318 | 7.265 | 38.650 | 2.5 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L11) | 20/20 | 398.168 | 17.144 | 23.202 | 2.1 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L11) | 10/10 | 314.853 | 7.306 | 42.998 | 0.9 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L11) | 30/30 | 313.194 | 15.620 | 21.107 | 384.6 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L11) | 20/20 | 85.573 | 2.104 | 39.989 | 4.0 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L11) | 20/20 | 750.029 | 16.297 | 45.916 | 2.3 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L61) | 10/10 | 184.793 | 4.502 | 40.947 | 0.8 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L11) | 10/10 | 341.873 | 11.589 | 29.566 | 1.2 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L11) | 20/20 | 816.997 | 19.302 | 42.219 | 4.0 | aucun filtre déclenché |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L2) | 30/30 | 74.628 | 4.146 | 18.280 | 6.6 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L11) | 10/10 | 455.668 | 21.340 | 21.293 | 1.0 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L11) | 10/10 | 220.718 | 10.564 | 20.879 | 0.4 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L11) | 18/20 | 3 795.035 | 207.809 | 18.292 | 1.8 | invalid_rows_removed |
| [OCaml](../../OCaml/OCaml.csv#L11) | 20/20 | 123.968 | 3.545 | 34.768 | 4.7 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L11) | 20/20 | 1 677.902 | 42.222 | 39.659 | 1.6 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L11) | 10/10 | 325.227 | 16.050 | 20.238 | 1.0 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L11) | 19/20 | 4 189.326 | 95.444 | 43.838 | 1.3 | invalid_rows_removed |
| [Python](../../Python/Python.csv#L11) | 10/10 | 2 098.627 | 44.835 | 46.793 | 0.6 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L11) | 20/20 | 227.277 | 11.240 | 20.178 | 0.7 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L11) | 10/10 | 1 041.056 | 26.621 | 38.988 | 1.1 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L11) | 10/10 | 56.358 | 1.254 | 44.925 | 0.8 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L11) | 10/10 | 0.010 | 0.001 | 10.291 | 6.6 | short_time |
| [TypeScript](../../TypeScript/TypeScript.csv#L11) | 10/10 | 459.344 | 21.642 | 21.214 | 1.0 | aucun filtre déclenché |

## fannkuch-redux

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L41) | 20/20 | 311.699 | 7.350 | 42.331 | 1.4 | aucun filtre déclenché |
| [C](../../C/C.csv#L41) | 20/20 | 259.206 | 6.081 | 42.504 | 1.0 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L41) | 20/20 | 129.102 | 3.050 | 27.730 | 201.6 | short_time, block_shift |
| [CSharp](../../CSharp/CSharp.csv#L41) | 10/10 | 477.461 | 10.792 | 44.270 | 0.3 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L41) | 20/20 | 337.304 | 7.854 | 42.934 | 0.8 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L41) | 20/20 | 756.003 | 38.679 | 19.545 | 0.5 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L31) | 10/10 | 4 872.406 | 102.435 | 47.940 | 1.8 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L41) | 20/20 | 231.369 | 5.477 | 31.529 | 201.9 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L31) | 20/20 | 378.638 | 8.661 | 43.696 | 1.5 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L31) | 19/20 | 376.342 | 8.486 | 44.350 | 0.4 | invalid_rows_removed |
| [Hack](../../Hack/Hack.csv#L81) | 10/10 | 6 149.192 | 115.388 | 53.054 | 1.7 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L31) | 10/10 | 564.670 | 16.335 | 35.189 | 23.2 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L41) | 19/20 | 9 217.058 | 218.654 | 42.432 | 11.0 | invalid_rows_removed |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L82) | 10/10 | 172.374 | 8.834 | 19.465 | 1.1 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L41) | 10/10 | 654.783 | 33.668 | 19.448 | 0.0 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L31) | 10/10 | 368.302 | 9.006 | 40.721 | 0.4 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L31) | 19/20 | 12 801.871 | 633.695 | 20.209 | 0.4 | invalid_rows_removed |
| [OCaml](../../OCaml/OCaml.csv#L41) | 20/20 | 333.050 | 7.880 | 42.168 | 0.9 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L91) | 8/10 | 6 667.744 | 126.026 | 52.941 | 0.4 | invalid_rows_removed |
| [Pascal](../../Pascal/Pascal.csv#L41) | 10/10 | 404.794 | 9.805 | 41.227 | 1.4 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L41) | 17/20 | 12 977.523 | 249.254 | 52.039 | 0.8 | invalid_rows_removed |
| [Python](../../Python/Python.csv#L41) | 10/10 | 14 777.476 | 279.851 | 53.123 | 1.5 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L41) | 19/20 | 2 226.389 | 43.768 | 51.005 | 1.9 | invalid_rows_removed |
| [Ruby](../../Ruby/Ruby.csv#L81) | 9/10 | 16 409.203 | 314.892 | 52.267 | 0.5 | invalid_rows_removed |
| [Rust](../../Rust/Rust.csv#L41) | 10/10 | 283.186 | 6.650 | 42.755 | 0.9 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L41) | 10/10 | 0.009 | 0.001 | 7.563 | 9.7 | short_time |
| [Swift](../../Swift/Swift.csv#L31) | 10/10 | 288.106 | 6.692 | 42.996 | 0.8 | aucun filtre déclenché |
| [TypeScript](../../TypeScript/TypeScript.csv#L31) | 10/10 | 10 767.114 | 516.182 | 20.861 | 2.3 | aucun filtre déclenché |

## fasta

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L81) | 20/20 | 62.559 | 2.746 | 22.738 | 2.4 | aucun filtre déclenché |
| [C](../../C/C.csv#L91) | 20/20 | 33.314 | 0.933 | 35.092 | 6.2 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L81) | 20/20 | 43.014 | 1.153 | 37.365 | 1.0 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L81) | 10/10 | 57.345 | 1.554 | 36.918 | 1.2 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L71) | 20/20 | 49.993 | 1.382 | 36.292 | 1.2 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L71) | 20/20 | 96.128 | 4.744 | 20.149 | 1.9 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L71) | 10/10 | 720.929 | 27.842 | 25.881 | 0.6 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L81) | 20/20 | 67.066 | 2.714 | 22.953 | 200.3 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L61) | 20/20 | 38.420 | 1.656 | 23.088 | 4.4 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L71) | 20/20 | 53.058 | 1.844 | 28.849 | 1.3 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L31) | 20/20 | 324.116 | 15.355 | 21.124 | 22.8 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L51) | 10/10 | 246.377 | 5.725 | 43.064 | 0.7 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L81) | 20/20 | 1 292.777 | 49.689 | 25.862 | 2.6 | aucun filtre déclenché |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L92) | 10/10 | 25.823 | 1.284 | 19.880 | 15.3 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L71) | 10/10 | 101.376 | 5.098 | 19.923 | 2.9 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L51) | 10/10 | 344.946 | 15.763 | 21.876 | 0.3 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L61) | 20/20 | 519.807 | 24.534 | 21.177 | 1.7 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L71) | 20/20 | 62.993 | 3.169 | 19.860 | 1.8 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L31) | 20/20 | 640.969 | 29.475 | 21.548 | 3.3 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L71) | 10/10 | 104.192 | 5.474 | 19.051 | 1.6 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L61) | 20/20 | 1 931.726 | 50.959 | 36.322 | 112.7 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L71) | 9/10 | 1 569.750 | 74.029 | 21.200 | 1.2 | invalid_rows_removed |
| [Racket](../../Racket/Racket.csv#L81) | 20/20 | 180.760 | 8.247 | 21.972 | 2.0 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L61) | 10/10 | 1 284.347 | 61.039 | 21.024 | 2.4 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L81) | 10/10 | 32.461 | 0.917 | 35.411 | 0.5 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L81) | 9/10 | 0.010 | 0.001 | 10.849 | 16.0 | invalid_rows_removed, short_time |
| [Swift](../../Swift/Swift.csv#L61) | 10/10 | 46.017 | 1.407 | 32.740 | 0.4 | aucun filtre déclenché |
| [TypeScript](../../TypeScript/TypeScript.csv#L41) | 10/10 | 131.003 | 6.905 | 18.970 | 0.3 | aucun filtre déclenché |

## k-nucleotide

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L51) | 20/20 | 190.225 | 6.804 | 27.794 | 7.3 | aucun filtre déclenché |
| [C](../../C/C.csv#L51) | 20/20 | 108.961 | 2.827 | 38.501 | 3.1 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L51) | 20/20 | 126.321 | 3.681 | 34.519 | 6.8 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L51) | 10/10 | 265.187 | 7.210 | 36.765 | 1.8 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L51) | 20/20 | 309.256 | 7.904 | 39.105 | 0.9 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L51) | 20/20 | 521.614 | 14.471 | 36.019 | 1.1 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L41) | 9/10 | 3 152.098 | 86.829 | 36.388 | 1.4 | invalid_rows_removed |
| [FSharp](../../FSharp/FSharp.csv#L51) | 20/20 | 245.387 | 7.053 | 27.687 | 203.6 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L41) | 20/20 | 783.063 | 41.589 | 18.852 | 0.7 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L41) | 20/20 | 324.125 | 8.006 | 40.697 | 1.5 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L21) | 20/20 | 998.821 | 24.020 | 41.169 | 18.7 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L51) | 20/20 | 3 085.154 | 87.200 | 35.417 | 2.7 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L51) | 10/10 | 1 326.837 | 34.392 | 38.636 | 1.2 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L41) | 20/20 | 1 827.242 | 87.993 | 20.806 | 0.8 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L51) | 20/20 | 424.362 | 13.705 | 31.329 | 1.8 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L101) | 10/10 | 1 129.637 | 29.277 | 38.588 | 1.4 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L51) | 20/20 | 1 566.990 | 35.652 | 43.942 | 0.5 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L51) | 10/10 | 1 852.066 | 38.939 | 47.580 | 0.9 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L51) | 20/20 | 940.558 | 44.178 | 21.282 | 1.9 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L41) | 10/10 | 2 766.155 | 60.698 | 45.471 | 1.0 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L51) | 10/10 | 87.039 | 2.349 | 36.917 | 0.7 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L51) | 10/10 | 0.009 | 0.001 | 7.484 | 68.7 | short_time |
| [Swift](../../Swift/Swift.csv#L41) | 10/10 | 328.321 | 8.487 | 38.611 | 0.7 | aucun filtre déclenché |

## mandelbrot

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L61) | 20/20 | 117.938 | 3.188 | 36.937 | 0.4 | aucun filtre déclenché |
| [C](../../C/C.csv#L71) | 20/20 | 42.324 | 1.142 | 36.814 | 3.4 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L61) | 20/20 | 34.188 | 0.857 | 39.951 | 0.3 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L61) | 10/10 | 180.910 | 3.965 | 45.660 | 0.7 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L61) | 20/20 | 114.204 | 2.448 | 46.769 | 1.5 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L61) | 20/20 | 275.273 | 10.076 | 27.391 | 1.0 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L51) | 10/10 | 10 658.085 | 194.791 | 54.691 | 0.2 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L61) | 20/20 | 119.617 | 3.464 | 28.072 | 198.9 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L51) | 20/20 | 221.538 | 8.635 | 25.647 | 1.6 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L51) | 20/20 | 137.521 | 3.453 | 39.622 | 1.3 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L101) | 10/10 | 807.367 | 15.262 | 52.883 | 0.8 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L41) | 10/10 | 205.224 | 6.024 | 34.142 | 0.5 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L61) | 18/20 | 9 275.679 | 217.230 | 42.699 | 2.0 | invalid_rows_removed |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L32) | 10/10 | 69.677 | 3.580 | 19.467 | 2.4 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L61) | 10/10 | 285.596 | 8.269 | 34.514 | 0.3 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L41) | 10/10 | 112.417 | 3.379 | 33.274 | 1.4 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L51) | 19/20 | 4 416.517 | 99.945 | 44.097 | 1.4 | invalid_rows_removed |
| [OCaml](../../OCaml/OCaml.csv#L61) | 20/20 | 255.749 | 6.863 | 37.270 | 0.6 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L111) | 10/10 | 3 959.661 | 73.759 | 53.700 | 0.4 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L51) | 10/10 | 255.979 | 7.188 | 35.615 | 0.2 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L71) | 33/40 | 19 968.497 | 391.780 | 50.942 | 97.8 | invalid_rows_removed |
| [Python](../../Python/Python.csv#L61) | 9/10 | 9 003.674 | 162.933 | 55.293 | 1.0 | invalid_rows_removed |
| [Racket](../../Racket/Racket.csv#L61) | 20/20 | 836.184 | 44.508 | 18.795 | 0.4 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L51) | 9/10 | 12 993.213 | 245.675 | 52.959 | 1.2 | invalid_rows_removed |
| [Rust](../../Rust/Rust.csv#L61) | 10/10 | 48.333 | 1.174 | 41.106 | 0.4 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L61) | 10/10 | 0.010 | 0.001 | 8.579 | 4.5 | short_time |
| [Swift](../../Swift/Swift.csv#L51) | 10/10 | 83.833 | 1.799 | 46.601 | 0.1 | aucun filtre déclenché |

## n-body

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L1) | 20/20 | 79.561 | 4.085 | 19.468 | 2.5 | aucun filtre déclenché |
| [C](../../C/C.csv#L1) | 20/20 | 74.811 | 4.191 | 17.795 | 3.0 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L1) | 20/20 | 70.363 | 3.770 | 18.662 | 3.6 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L1) | 10/10 | 113.463 | 6.110 | 18.563 | 2.5 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L1) | 20/20 | 95.329 | 5.201 | 18.079 | 4.4 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L1) | 20/20 | 128.830 | 6.825 | 18.846 | 4.4 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L1) | 10/10 | 3 075.779 | 150.143 | 20.290 | 2.3 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L1) | 30/30 | 127.030 | 7.104 | 18.356 | 100.4 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L1) | 20/20 | 64.548 | 3.571 | 18.070 | 5.6 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L1) | 20/20 | 105.746 | 5.899 | 17.926 | 1.6 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L1) | 19/20 | 5 744.862 | 276.828 | 20.976 | 12.7 | invalid_rows_removed |
| [Haskell](../../Haskell/Haskell.csv#L1) | 10/10 | 195.235 | 10.046 | 19.473 | 1.4 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L1) | 19/20 | 2 423.475 | 97.975 | 24.680 | 1.4 | invalid_rows_removed |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L72) | 10/10 | 64.751 | 3.930 | 16.477 | 11.5 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L1) | 10/10 | 126.240 | 6.762 | 18.659 | 0.4 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L1) | 10/10 | 119.451 | 6.685 | 17.870 | 0.0 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L1) | 20/20 | 4 412.315 | 176.923 | 23.899 | 36.3 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L1) | 20/20 | 109.368 | 5.858 | 18.671 | 5.3 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L1) | 19/20 | 3 758.207 | 179.018 | 21.007 | 1.9 | invalid_rows_removed |
| [Pascal](../../Pascal/Pascal.csv#L1) | 10/10 | 102.359 | 5.701 | 17.954 | 0.5 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L1) | 19/20 | 6 853.087 | 325.311 | 21.065 | 0.5 | invalid_rows_removed |
| [Python](../../Python/Python.csv#L1) | 9/10 | 11 779.833 | 559.663 | 21.050 | 0.4 | invalid_rows_removed |
| [Racket](../../Racket/Racket.csv#L1) | 30/30 | 451.323 | 22.442 | 19.809 | 47.7 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L1) | 10/10 | 5 929.687 | 281.297 | 21.073 | 0.8 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L1) | 10/10 | 61.992 | 3.329 | 18.580 | 0.6 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L1) | 8/10 | 0.012 | 0.001 | 16.029 | 4.3 | invalid_rows_removed, short_time |
| [Swift](../../Swift/Swift.csv#L1) | 10/10 | 117.067 | 6.026 | 19.416 | 1.4 | aucun filtre déclenché |
| [TypeScript](../../TypeScript/TypeScript.csv#L1) | 10/10 | 128.146 | 6.856 | 18.671 | 0.3 | aucun filtre déclenché |

## pidigits

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L71) | 20/20 | 11.483 | 0.545 | 21.033 | 1.5 | aucun filtre déclenché |
| [C](../../C/C.csv#L81) | 20/20 | 11.451 | 0.547 | 20.968 | 2.2 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L71) | 20/20 | 11.623 | 0.549 | 21.138 | 0.6 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L71) | 10/10 | 20.819 | 0.943 | 22.072 | 0.6 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L61) | 10/10 | 167.374 | 7.360 | 22.773 | 2.7 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L71) | 20/20 | 10.692 | 0.501 | 21.468 | 187.5 | block_shift |
| [Go](../../Go/Go.csv#L61) | 20/20 | 18.565 | 0.759 | 24.538 | 8.1 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L71) | 20/20 | 199.461 | 8.127 | 24.698 | 7.2 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L71) | 10/10 | 50.005 | 2.465 | 20.283 | 0.2 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L61) | 10/10 | 11.683 | 0.547 | 21.293 | 1.1 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L91) | 20/20 | 29.181 | 1.313 | 21.819 | 4.8 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L91) | 10/10 | 25.861 | 1.178 | 21.967 | 0.9 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L71) | 20/20 | 15.223 | 0.732 | 20.775 | 1.0 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L71) | 10/10 | 12.013 | 0.553 | 21.763 | 2.9 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L71) | 10/10 | 0.009 | 0.001 | 8.431 | 12.9 | short_time |

## regex-redux

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L31) | 20/20 | 184.127 | 5.105 | 36.082 | 2.2 | aucun filtre déclenché |
| [C](../../C/C.csv#L31) | 20/20 | 30.408 | 0.805 | 37.369 | 1.6 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L31) | 20/20 | 249.873 | 10.575 | 23.610 | 2.9 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L31) | 9/10 | 631.244 | 14.710 | 42.987 | 1.2 | invalid_rows_removed |
| [Chapel](../../Chapel/Chapel.csv#L31) | 20/20 | 126.580 | 4.527 | 27.775 | 1.6 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L31) | 19/20 | 290.570 | 13.489 | 21.577 | 1.2 | invalid_rows_removed |
| [FSharp](../../FSharp/FSharp.csv#L31) | 30/30 | 962.947 | 46.685 | 20.905 | 101.9 | block_shift |
| [Hack](../../Hack/Hack.csv#L11) | 20/20 | 53.190 | 2.042 | 26.103 | 6.2 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L31) | 20/20 | 441.030 | 13.515 | 32.657 | 0.8 | aucun filtre déclenché |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L22) | 9/10 | 0.006 | 0.001 | 7.029 | 12.7 | invalid_rows_removed, short_time |
| [JavaScript](../../JavaScript/JavaScript.csv#L31) | 10/10 | 40.410 | 2.089 | 19.346 | 0.3 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L31) | 20/20 | 264.408 | 12.982 | 20.338 | 1.2 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L81) | 10/10 | 46.425 | 1.667 | 27.853 | 0.5 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L31) | 10/10 | 50.694 | 2.281 | 22.213 | 0.4 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L31) | 20/20 | 286.111 | 7.172 | 39.939 | 0.7 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L31) | 10/10 | 214.212 | 7.114 | 29.908 | 6.1 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L31) | 20/20 | 539.777 | 26.115 | 20.669 | 1.1 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L31) | 10/10 | 295.652 | 14.233 | 20.718 | 1.4 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L31) | 10/10 | 56.599 | 2.295 | 24.680 | 0.6 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L31) | 10/10 | 0.008 | 0.001 | 7.529 | 1.3 | short_time |
| [Swift](../../Swift/Swift.csv#L21) | 10/10 | 833.371 | 41.731 | 19.977 | 0.6 | aucun filtre déclenché |
| [TypeScript](../../TypeScript/TypeScript.csv#L21) | 10/10 | 38.729 | 1.995 | 19.413 | 0.2 | aucun filtre déclenché |

## reverse-complement

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L21) | 20/20 | 10.806 | 0.365 | 29.535 | 2.4 | aucun filtre déclenché |
| [C](../../C/C.csv#L21) | 20/20 | 7.947 | 0.232 | 34.376 | 4.1 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L21) | 20/20 | 7.305 | 0.221 | 32.657 | 4.8 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L21) | 10/10 | 17.104 | 0.589 | 29.046 | 2.1 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L21) | 20/20 | 21.591 | 0.911 | 23.491 | 3.7 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L21) | 20/20 | 243.257 | 10.626 | 22.804 | 1.6 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L21) | 10/10 | 182.046 | 6.501 | 28.001 | 0.9 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L21) | 40/40 | 111.547 | 5.634 | 19.962 | 51.5 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L21) | 20/20 | 19.184 | 0.939 | 20.122 | 4.4 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L21) | 20/20 | 11.757 | 0.368 | 31.903 | 1.8 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L21) | 10/10 | 18.994 | 0.806 | 23.552 | 0.7 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L21) | 20/20 | 158.847 | 4.486 | 35.370 | 8.9 | aucun filtre déclenché |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L52) | 9/10 | 0.005 | 0.001 | 5.744 | 22.5 | invalid_rows_removed, short_time |
| [JavaScript](../../JavaScript/JavaScript.csv#L21) | 10/10 | 46.148 | 1.932 | 23.928 | 3.2 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L21) | 10/10 | 25.028 | 1.137 | 22.022 | 2.5 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L21) | 20/20 | 211.307 | 9.162 | 23.030 | 2.8 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L21) | 20/20 | 10.539 | 0.286 | 36.482 | 2.0 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L21) | 20/20 | 34.227 | 1.208 | 28.045 | 3.2 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L21) | 10/10 | 21.484 | 0.909 | 23.575 | 3.3 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L21) | 20/20 | 30.638 | 1.193 | 25.657 | 4.0 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L21) | 10/10 | 42.611 | 1.490 | 28.531 | 1.0 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L21) | 20/20 | 44.770 | 2.116 | 21.126 | 0.5 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L21) | 10/10 | 55.617 | 1.966 | 28.225 | 1.3 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L21) | 10/10 | 8.675 | 0.284 | 30.346 | 3.7 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L21) | 10/10 | 0.009 | 0.001 | 7.487 | 90.7 | short_time |
| [Swift](../../Swift/Swift.csv#L11) | 10/10 | 11.949 | 0.410 | 29.177 | 1.7 | aucun filtre déclenché |

## spectral-norm

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [Ada](../../Ada/Ada.csv#L91) | 20/20 | 32.577 | 0.773 | 42.160 | 0.3 | aucun filtre déclenché |
| [C](../../C/C.csv#L101) | 20/20 | 23.229 | 0.672 | 34.167 | 2.1 | aucun filtre déclenché |
| [C++](../../C++/C++.csv#L91) | 20/20 | 21.348 | 0.665 | 32.086 | 0.2 | aucun filtre déclenché |
| [CSharp](../../CSharp/CSharp.csv#L91) | 10/10 | 45.722 | 1.374 | 33.292 | 0.3 | aucun filtre déclenché |
| [Chapel](../../Chapel/Chapel.csv#L81) | 20/20 | 44.949 | 1.352 | 33.118 | 1.1 | aucun filtre déclenché |
| [Dart](../../Dart/Dart.csv#L81) | 20/20 | 90.304 | 5.115 | 17.757 | 1.8 | aucun filtre déclenché |
| [Erlang](../../Erlang/Erlang.csv#L81) | 10/10 | 902.758 | 17.999 | 50.147 | 1.0 | aucun filtre déclenché |
| [FSharp](../../FSharp/FSharp.csv#L91) | 20/20 | 29.543 | 0.732 | 30.435 | 195.6 | block_shift |
| [Fortran](../../Fortran/Fortran.csv#L71) | 20/20 | 22.200 | 0.667 | 33.244 | 0.5 | aucun filtre déclenché |
| [Go](../../Go/Go.csv#L81) | 20/20 | 43.859 | 1.332 | 32.844 | 1.2 | aucun filtre déclenché |
| [Hack](../../Hack/Hack.csv#L41) | 20/20 | 399.441 | 9.171 | 44.772 | 44.9 | aucun filtre déclenché |
| [Haskell](../../Haskell/Haskell.csv#L61) | 10/10 | 43.328 | 1.373 | 31.573 | 0.2 | aucun filtre déclenché |
| [JRuby](../../JRuby/JRuby.csv#L91) | 20/20 | 1 870.260 | 79.310 | 23.487 | 1.3 | aucun filtre déclenché |
| [Java-GraalVM](../../Java-GraalVM/GraalVM.csv#L62) | 10/10 | 26.983 | 1.385 | 19.474 | 0.7 | aucun filtre déclenché |
| [JavaScript](../../JavaScript/JavaScript.csv#L81) | 10/10 | 86.281 | 5.040 | 17.105 | 0.5 | aucun filtre déclenché |
| [Lisp](../../Lisp/Lisp.csv#L61) | 10/10 | 51.789 | 1.370 | 37.799 | 0.2 | aucun filtre déclenché |
| [Lua](../../Lua/Lua.csv#L71) | 20/20 | 1 940.023 | 95.433 | 20.301 | 0.6 | aucun filtre déclenché |
| [OCaml](../../OCaml/OCaml.csv#L81) | 20/20 | 51.961 | 1.682 | 30.756 | 0.8 | aucun filtre déclenché |
| [PHP](../../PHP/PHP.csv#L41) | 20/20 | 1 011.260 | 19.032 | 53.054 | 2.6 | aucun filtre déclenché |
| [Pascal](../../Pascal/Pascal.csv#L81) | 10/10 | 46.350 | 1.349 | 34.336 | 0.3 | aucun filtre déclenché |
| [Perl](../../Perl/Perl.csv#L101) | 20/20 | 998.473 | 19.801 | 50.384 | 2.3 | aucun filtre déclenché |
| [Python](../../Python/Python.csv#L81) | 10/10 | 7 386.979 | 137.600 | 53.554 | 0.7 | aucun filtre déclenché |
| [Racket](../../Racket/Racket.csv#L91) | 20/20 | 100.675 | 2.340 | 43.029 | 0.2 | aucun filtre déclenché |
| [Ruby](../../Ruby/Ruby.csv#L71) | 10/10 | 3 643.508 | 71.614 | 50.824 | 0.8 | aucun filtre déclenché |
| [Rust](../../Rust/Rust.csv#L91) | 10/10 | 29.010 | 0.675 | 43.012 | 0.2 | aucun filtre déclenché |
| [Smalltalk](../../Smalltalk/Smalltalk.csv#L91) | 10/10 | 0.009 | 0.001 | 9.207 | 18.4 | short_time |
| [Swift](../../Swift/Swift.csv#L71) | 10/10 | 43.645 | 1.345 | 32.457 | 0.1 | aucun filtre déclenché |
| [TypeScript](../../TypeScript/TypeScript.csv#L51) | 10/10 | 103.191 | 5.750 | 17.947 | 0.2 | aucun filtre déclenché |

## thread-ring

| Configuration | n valides/brut | PKG (J) | Temps (s) | Puissance PKG (W) | IQR énergie (%) | Signalements |
|---|---:|---:|---:|---:|---:|---|
| [C](../../C/C.csv#L61) | 10/10 | 1 238.367 | 65.953 | 18.744 | 1.3 | aucun filtre déclenché |
