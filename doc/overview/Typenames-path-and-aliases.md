# Typenames, `path` and `alias`

## What is a Typename?

A _Typename_  identifies a Python class in a class section.

Typenames are BiblioPixel's mechanism for importing and reusing Python code.
Each Class Section in a Project (`animation`, `controls`, `drivers`, or
`layout`) represents a Python class and therefore has a `typename` field.

Typenames allow several formats for convenience.

**Example 1**: typename formats

* Absolute: `bibliopixel.animation.tests.StripChannelTest`
* Relative: `.tests.StripChannelTest`
* File: `/home/pi/Documents/myAnimation.py`
* Git Repo: `https://github.com/ManiacalLabs/BiblioPixelAnimations/blob/master/BiblioPixelAnimations/matrix/MatrixRain.py`

WARNING:

Git Repo Typenames allow you to load arbitrary code from the internet and
execute it.  Malicious code could do anything, including erasing all your data
or stealing money from your accounts.  ONLY use Git Repo Typenames if you
_completely and 100%_  trust the repo that you are loading from.

## Using Typenames in a Project.

**Example 2**:  Simple animation, Absolute Typename

```
    animation:
      typename: bibliopixel.animation.tests.StripChannelTest
```

For convenience, if the whole class section is a string, it's the `typename`:

**Example 3**:  Same animation as in Example 1

```
    animation: bibliopixel.animation.tests.StripChannelTest
```

**Example 4**:  Relative Typename

```
    animation: .tests.StripChannelTest
```


## The `path` Project Section.

The optional Project Section `path` is a list of external directories that
contain extra Python code used by the Project.

The `path` is represented either by a list of strings, or by a single string
which is a list of directories separated by colons (like the `PATH` and
`PYTHONPATH` environment variables).

When Typenames in a Project are resolved to a class, these directories are
searched for code, in this order:

1. The local directory
2. The directory local to the Project .json file
3. Directories in the  `path` Project Section, in order given in the project
4. Directories in the `PYTHONPATH` environment variable
5 The Python installation directory

[TODO: make sure this is really true.]

**Example 5**: Using `path`

```
    path: [/home/pi/my-library, /var/stuff/some-library]

    # Equivalent using colon separated strings would be
    # path: "/home/pi/my-library:/var/stuff/some-library"
```

## The `alias` Project Section.

The optional Project Section `alias` is a dictionary of aliases to Typenames or
parts of Typenames that can be put together to save typing in your project.

The `$` character is used to introduce an alias into a typename.  Aliases are
terminated by the characters `.`,  `/` or `#`.

**Example 6**: Using `alias`

```
    alias:
      bpa: BiblioPixelAnimations.matrix
      fade: christmas_lights.Fade

    animation:
        typename: sequence
        length: 2
        animations:
            - $bpa.ImageAnim
            - $fade
            - $bpa.ImageShow
            - $fade
            - $bpa.ImageDissolve
            - $fade
```
