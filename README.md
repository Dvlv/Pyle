A Less/Sass replacer with Python syntax

##Syntax Basics
- Selectors end with a colon
- No need for a colon in style declarations
- End chains of selectors with a blank line
- Whitespace is significant, just like python
- Use & to concatenate selectors

###Example Code
```
example.pyle


html:
  body:
    div:
      background red  
    span:
      color orange
      &.red:
        color red
```


Becomes:
```
style.css 


html body div {
  background: red;
}
html body span {
  color: orange;
}
html body span.red {
  color: red;
}
```

See the examples folder for detailed examples

To compile the examples, use `python3 pyle.py -m examples/main.pyle -c examples/style.css`

##Importing
- Pyle requires a main.pyle (or equivolent) file with a list of .pyle files to parse
- Files are imported with `@import test.pyle`
- You can create multiple .pyle files and import them all in your main.pyle file with `@import filename.pyle` (one per line)
- Variables can be declared in your main.pyle file with `def orange #ff6600` (see *Advanced Syntax* below)
- Your main.pyle file is only for importing other files and defining variables, do not write any styling info in main.pyle

##Output
- Pyle renders all styles to style.css, unless you specify a custom output file with `-c filename.css`
- Include the generated css file in your html as usual

##Running
`python3 pyle.py`

Or mark it as executable `chmod +x pyle.py`

Then you can just run

`./pyle.py`

###Optional Arguments
- `-m <filename>.pyle` The name of your main file (with all of your imports, defaults to `main.pyle`)
- `-c <filename>.css` custom output file for the css (defaults to style.css)

####Examples 
- `python3 pyle.py` Imports stylesheets and variables listed in `main.pyle` and writes to `style.css`
- `python3 pyle.py -m imports.pyle` Imports stylesheets and variables listed in `imports.pyle` and writes to `style.css`
- `python3 pyle.py -c site.css` Imports stylesheets and variables in `main.pyle` (as default) and writes to `site.css`
- `python3 pyle.py -m imports.pyle -c site.css` Imports stylesheets and variables in `imports.pyle` and writes to `site.css`

##Advanced syntax
####Media queries
- `@media mobile:`, `@media tablet:`, `@media <number>:` allow for mobile (max-width 420) and tablet (max-width 800) selectors, or a custom number.

####Before and after
- `::before:` and `::after:` allow for before and after pseudo-elements

####Defining variables
- `def orange #ff6600` allows you to define a variable, accessed by `@orange` in your pyle stylesheets, which will be replaced with `#ff6600` in the generated css file.
- The file is read top-down, so if you need to override styles between stylesheets simply redefine them before the `@import`
- e.g.
```
main.pyle
def yellow #ffff00
@import bright-yellow.pyle
def yellow #dddd00
@import darker-yellow.pyle
```
above, `bright-yellow` and `darker-yellow` can both use the `@yellow` variable, but its replacement will be different in each

###TODO
- Loops
- Animation keyframe creating
- Minified CSS
