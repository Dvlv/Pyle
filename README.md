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

See the examples folder for a detailed example

##Importing
- Pyle requires a main.pyle file with a list of .pyle files to parse
- You can create multiple files and import them all in your main.pyle file with `@import filename.pyle` (one per line)
- Your main.pyle file is only for importing other files, do not write any styling info in main.pyle

##Output
- Pyle renders all styles to style.css
- Include style.css in your html as usual

##Running
`python3 pyle.py main.pyle`

##Advanced syntax
- `@media mobile`, `@media tablet`, `@media <number>` allow for mobile (max-width 420) and tablet (max-width 800) selectors, or a custom number.
- `::before` and `::after` allow for before and after pseudo-elements

###TODO
- Arbitrary css filename
- Loops
- Animation keyframe creating
