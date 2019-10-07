[![Version](https://img.shields.io/badge/version-1.0-brightgreen.svg)](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse/jvci2018/)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](LICENSE)

# Project #

This project is based on the paper [Making a long story short: A multi-importance fast-forwarding egocentric videos with the emphasis on relevant objects](https://www.verlab.dcc.ufmg.br/semantic-hyperlapse/jvci2018/) on the **Special Issue on Egocentric Vision and Lifelogging Tools** at **Journal of Visual Communication and Image Representation** (JVCI 2018). It implements a fast-forward method for first-person videos based on multi-importance approach.

For more information and visual results, please acess the [project page](http://www.verlab.dcc.ufmg.br/fast-forward-video-based-on-semantic-extraction).

## Contact ##

### Authors ###

* Michel Melo da Silva - PhD student - UFMG - michelms@dcc.ufmg.com
* Washington Luis de Souza Ramos - PhD student - UFMG - washington.ramos@dcc.ufmg.br
* Felipe Cadar Chamone - Undergraduate Student - UFMG - cadar@dcc.ufmg.br
* João Pedro Klock Ferreira - Undergraduate Student - UFMG - jpklock@ufmg.br
* Mario Fernando Montenegro Campos - Advisor - UFMG - mario@dcc.ufmg.br
* Erickson Rangel do Nascimento - Advisor - UFMG - erickson@dcc.ufmg.br

### Institution ###

Federal University of Minas Gerais (UFMG)  
Computer Science Department  
Belo Horizonte - Minas Gerais - Brazil 

### Laboratory ###

![VeRLab](https://www.dcc.ufmg.br/dcc/sites/default/files/public/verlab-logo.png)

**VeRLab:** Laboratory of Computer Vision and Robotics
http://www.verlab.dcc.ufmg.br

## Code ##

This project is a two-fold source code. The first fold¹ is composed of MATLAB code to describe the video semantically and to fast-forward it. A stabilizer proper to fast-forwarded video written in C++ using OpenCV is the second fold². You can run each fold separately.

### Dependencies ###

* MATLAB 2015a or higher
* Python 2.7 _(Tested with 2.7.12)_
* MATLAB Engine for Python
* OpenCV 2.4 _(Tested with 2.4.9 and 2.4.13)_
* Armadillo 6 _(Tested with 6.600.5 -- Catabolic Amalgamator)_
* Boost 1 _(Tested with 1.54.0 and 1.58.0)_
* Doxygen 1 _(for documentation only - Tested with 1.8.12)_

### Usage ###

**Before running the following steps, please compile the Optical Flow Estimator and the Accelerated Video Stabilizer. Go back to the project's main folder and execute steps #1 and #7 (just the compiling part).**

If you don't want to read all the steps, feel free to use the **Quick Guide**. To see it, execute the first step and click on *Help Index* in the *Help* menu.

1.  **Running the Code:**

	Into the _PythonScripts_ directory, run the following command:
```
 user@computer:<project_path/PythonScripts>: python main.py
```

2. **Selecting the Video:**
	
	On the main screen, click on *OpenFile* in the *File* menu. Then select the video that you want to accelerate.
```
 The valid formats are: ".mp4" and ".avi"
```

3. **Choosing the Semantic Extractor**:

	After selecting the video, choose the semantic extractor that you want for your video. The extractors available are: _face_ and _pedestrian_.

4. **Choosing the SpeedUp:**

	After selecting the video, choose the speed-up that you want to apply.
```
 The speed-up rate needs to be an integer greater than 1.
```

5. **Speeding-Up the Video:**
	
	After setting everything, click on the `Speed Up and Stabilize` button and check the progress on the screen that'll be opened.