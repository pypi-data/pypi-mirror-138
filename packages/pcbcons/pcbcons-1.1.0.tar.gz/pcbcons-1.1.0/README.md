# pcbcons: Create footprints faster

pcbcons is a python library for creating PCB footprints.  It
allows footprints to be created using geometric constraints, rather
than through specifying absolute coordinates.

Currently pcbcons only supports outputting to gEDA pcb footprints.

## How to install

~~~
pip install pcbcons
~~~

## How to  use

Documentation is thin on the ground at this point, but some
introductory information is available on the
[original blog](https://xgoat.com/wp/2011/08/08/playing-with-footprints-and-constraints/)
post about the creation of pcbcons.

## Limitations

 * At the moment the constraint solver used by pcbcons is very basic.
   There are a huge number of constraint arrangements that it will not
   be able to solve.


