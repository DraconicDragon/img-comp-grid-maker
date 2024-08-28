# Image Comparison Grid Maker Tool Thing.

Works on Linux AND Windows! (woohoo cross platform <small><small><sub>yay!</sub></small></small>)
<small>Disclaimer or whatever this is: this program will only add the images next to each other in a row. For a full fledged grid see the [infinity grid](https://sd.mcmonkey.org/megagrid/) or others</small>

### Simple Application

* Drag and Drop any amount of images into the app
* Caption the images 
* Click the funny generate button and... profit!

### Prebuilt Binaries

Prebuilt binaries for Windows and Linux can be found in the [releases section](https://github.com/DraconicDragon/img-comp-grid-maker/releases/latest)

### Script

#### Requirements

* `pillow tkinterdnd2-universal` <sub><sub>tkinterdnd2 works too but not on linux</sub></sub>
* `nuitka` if you want to build the script to an executable
* <small>`sudo apt install python3-tk` if on linux because tkinter doesn't come bundled (shocker, I know.)</small>
* <small>some TrueType font if you are on linux and DeJavuSans font isn't available. otherwise the pillow default will be used which is just a bitmapped font with no size regulations</small>


<u>**App preview:**</u> <small><small><small>(Linux preview images available in assets folder)</small></small></small>
![app_preview](/assets/app_preview.png)

<u>**Result:**</u>
![result_preview](/assets/result_preview.jpg)

<small><small><small>the font currently doesnt get math'd into the white space correctly, especially when its a very long caption :\/</small></small></small>