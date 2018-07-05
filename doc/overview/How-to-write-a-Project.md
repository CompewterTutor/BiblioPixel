# How to write a BiblioPixel Project

A BiblioPixel Project is a text file that describes the parts of a BiblioPixel
Light Programming System Project in a form that humans can easily read,
understand and edit.

## Projects are text files written in either [YAML](https://yaml.org)
      or [JSON](https://json.org)

BiblioPixel Projects are data files, written in one of two human-readable
formats: YAML or JSON.

In this document, we use YAML for most of the examples.

**Example 1**: a simple Project file written in YAML

```
    shape: 50
    animation: BiblioPixelAnimations.strip.Wave
```

**Example 2**: a slightly larger Project file, written in JSON

```
    {
        "shape": [32, 32]

        "run": {
            "fps": 60
        },

        "animation": {
            "typename": "BiblioPixelAnimations.matrix.ImageAnim",
            "imagePath": "/Users/tom/Documents/giphy-zoom.gif"
        }
    }
```

**Example 3**: the same Project file, written in YAML

```
    shape: [32, 32]

    run:
      fps: 60

    animation:
      typename: BiblioPixelAnimations.matrix.ImageAnim
      imagePath: /Users/tom/Documents/giphy-zoom.gif
```

## A Project file is made up of _Sections_, which have _Fields_.

In the Project files above, there are three Sections - `shape`, `run`,
and `animation`.  Sections can have Fields - for example, the `run` Section
above has the Field `fps: 60`.

Project files have nine Sections, many of them optional.  The most important
Sections are `animation`, `shape`, and `driver`, which appear in almost every
Project:

* `animation` describes how your lights are animated
* `shape` shows how your lights are laid out in 1, 2, or 3 dimensions
* `driver` configures the hardware driver that controls the actual lights

_Class Sections_ are Python objects.  There are four Class Sections:
`animation`, `controls`, `drivers` and `layout`.

Each Class Section has a special _Typename_ which defines what the Python object
in that Section does, and which Fields can be set on it.  Typenames let you
load not just BiblioPixel code, but your own code


Nearly all the excitement in BiblioPixel is in the Class Sections!  BiblioPixel
comes with a large number of predefined Animations, Controls, Drivers and
Layouts, and you can put them together and customize them simply by writing a
Project, without any programming.

More, if you know a little Python you can extend them or modify a copy, or just
write your own from scratch.


_Value Sections_ contain simple things like strings, numbers, lists, or
dictionaries.  The five Value Sections are `aliases`, `numbers`, `path`, `run`,
and `shape`.

# Fields

Each Section has a list of _Fields_ - values that you can set.

In Example 2 and 3 above, the `run` Section has the Field `fps` with value
`60` (fps meaning "frames per second"), and the `animation` Section has the
Field `imagePath` with value `/Users/tom/Documents/giphy-zoom.gif `.

A Value Section always has the same Fields - for example, the `run` Section
always has the `fps` Field in any Project.

Each Class Section has a special Field named `typename` which is the name
of its Python class.

And then each Class Section has _different_ Fields depending on that
Typename.

For example, many Animations have no Fields at all and do exactly one thing.

An example is the Animation with the Typename `.tests.StripChannelTest`.


**Example 4**:  An Animation that runs a simple test on a strip of 10 pixels

```
    shape: 10
    animation:
      typename: .tests.StripChannelTest
```

On the other hand, the `sequence` Animation requires a Field `animations`,
a list of Animations that are played in sequence.  It also has an optional
Field `length` which sets the length of each subsequence.

**Example 5**:  This Animation runs four Animations, each for two seconds, in a
  loop, and displays the result on a 32x32 pixel display.

```
    shape: [32, 32]

    animation:
        typename: .sequence
        length: 2
        animations:
            - BiblioPixelAnimations.matrix.ImageAnim
            - BiblioPixelAnimations.matrix.ImageShow
            - BiblioPixelAnimations.matrix.ImageDissolve
            - BiblioPixelAnimations.matrix.ScreenGrab
```

# A summary of the Sections

## Class Sections

* `driver`: The output Driver for the hardware or simulator
* `drivers`: Used if there's more than one Driver.  If the `drivers` Section is
  non-empty, the `driver` Section becomes a template for `drivers`.
* `layout`: How the lights are laid out geometrically.
* `animation`: The class that actually animates the lights.
* `controls`: Classes that use external input to control parts of
  the Project.

## Value Sections

* `aliases`: Aliases are a shorthand to save typing.
* `numbers`: Select between plain old Python lists and faster, more powerful
numpy lists.
* `path`: `path` is added to the `PYTHONPATH` to allow loading of custom
  libraries.
* `run`: `run` controls how the topmost Animation is executed - how fast it
  runs, for how lon or for how many times, etc.
* `shape`: The shape of the layout - `length` for strips, `[width, height]` for
matrices and `[x, y, z]` for cubes.
