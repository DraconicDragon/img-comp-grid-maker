# Image Comparison Grid Maker Tool Thing.

Works on Linux AND Windows! (woohoo cross platform <sub>yay!</sub>)
<sub>Disclaimer or whatever this is: this program will only add the images next to each other in a row. It also isn't actually needed if you have Forge, SwarmUI, a1111 sd webui because they have it builtin (xyz plot). For a fully full fullings fledged grid see the [infinity grid](https://sd.mcmonkey.org/megagrid/) or others</sub>

### Simple Application

* Drag and Drop any amount of images into the app
* Caption the images 
* Click the funny generate button and... profit!

### Prebuilt Binaries

Prebuilt binaries for Windows and Linux can be found in the [releases section](https://github.com/DraconicDragon/img-comp-grid-maker/releases/latest)
There is also binaries built on every commit to the repo at the [actions tab](https://github.com/DraconicDragon/img-comp-grid-maker/actions) which includes MacOS 13 non ARM which i can't test (i also dont know why the linux build is 10mb larger than mine)

### Script

#### Requirements

* `pillow tkinterdnd2-universal` <sub><sub>tkinterdnd2 works too but not on linux</sub></sub>
* `nuitka` if you want to build the script to an executable
* <sub>`sudo apt install python3-tk` if on linux because tkinter doesn't come bundled (shocker, I know.)</sub>
* <sub>some TrueType font if you are on linux and DeJavuSans font isn't available. otherwise the pillow default will be used which is just a bitmapped font with no size regulations</sub>


**App preview:** <sub>(Linux preview images available in assets folder)</sub>
![app_preview](/assets/app_preview.png)

**Result:**
![result_preview](/assets/result_preview.jpg)

<sub><sub>the font currently doesnt get math'd into the white space correctly, especially when its a very long caption :\/</sub></sub>
