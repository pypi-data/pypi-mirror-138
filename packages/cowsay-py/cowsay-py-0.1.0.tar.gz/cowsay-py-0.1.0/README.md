cowsay-py
=========


[![PyPI version info](https://img.shields.io/pypi/v/cowsay-py.svg)](https://pypi.python.org/pypi/cowsay-py)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/cowsay-py.svg)](https://pypi.python.org/pypi/cowsay-py)

````
 __________________
< srsly dude, why? >
 ------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||
````

Please note that this is a new package and there will be bugs. Please report them to the [issue page.](https://github.com/Ovlic/cowsay_py/issues)


Cowsay is a configurable talking cow, originally written in Perl by [Tony Monroe](https://github.com/tnalpgge/rank-amateur-cowsay)

This project uses code from [cowsay2](https://github.com/johnnysprinkles/cowsay), the node.js moderenized version of cowsay.


Installing
----------

```sh

# Linux/macOS
python3 -m pip install -U cowsay-py

# Windows
py -3 -m pip install -U cowsay-py
```

Usage (Coming Soon!)
-----

~~cowsay Python FTW!~~

~~or~~

~~cowthink python is cool~~


~~It acts in the same way as the original cowsay, so consult `cowsay(1)` or run `cowsay -h`~~

````
 ________
< indeed >
 --------
    \
     \
                                   .::!!!!!!!:.
  .!!!!!:.                        .:!!!!!!!!!!!!
  ~~~~!!!!!!.                 .:!!!!!!!!!UWWW$$$
      :$$NWX!!:           .:!!!!!!XUWW$$$$$$$$$P
      $$$$$##WX!:      .<!!!!UW$$$$"  $$$$$$$$#
      $$$$$  $$$UX   :!!UW$$$$$$$$$   4$$$$$*
      ^$$$B  $$$$\     $$$$$$$$$$$$   d$$R"
        "*$bd$$$$      '*$$$$$$$$$$$o+#"
             """"          """""""
````

Quick Example
-------------

```py
import cowsay

print(cowsay.say(
    'Moooooo!',
    eyes="oO",
    tongue="U"
))

# or cowsay.think()
```
````
 ___________
< Moooooo!  >
 -----------
           \   ^__^
            \  (oO)\_______
               (__)\       )\/\
                U ||----w |
                  ||     ||
````

getting a list of cow names:
```py
from cowsay import cows

print(dir(cows))
```

### Function options

```py
say(
  text: 'hello',
  cow: cowsay.Cow, # Template for a cow, get inspiration from `./cows`
  eyes: 'oo', # Select the appearance of the cow's eyes, equivalent to cowsay -e
  tongue: 'L|', # The tongue is configurable similarly to the eyes through -T and tongue_string, equivalent to cowsay -T
  wrap: True, # Specifies if the given message will be word-wrapped. equivalent to cowsay -n
  wrapLength: 40, # Specifies roughly where the message should be wrapped. equivalent to cowsay -W
  mode: 'b', # One of 	"b", "d", "g", "p", "s", "t", "w", "y"
)
```
