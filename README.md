# RenParse
tl;dr check for typos in file paths

A solution to lazy-test your renpy project for broken file paths

On first launch, will drop a .json config:  
  "skip comments" true/false to skip commented-out lines  
  "jump one directory upwards" true/false to chdir up once, in case you'll set it up like game/devtools or game/renparse  
  "misc extensions" is a list of all non-image file extensions we'll check for  
  "image extensions" is a list of image-specific ones. Reason it's split from misc is, for images we check at both game/path and game/images/path  
  "strings to skip" is whatever substrings or symbols you want to filter path-likes out by, ex. ** that build.classify uses  

Meant to be used as a one-stop .exe, can be found in releases
