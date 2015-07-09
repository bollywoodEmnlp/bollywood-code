# Bollywood related artists recommendation
recommendating related artists with co-occurrence, degree and spectral mean distance features

REACH

1. Clone using "git clone https://github.com/bollywoodEmnlp/bollywood-code";
2. Download from https://github.com/bollywoodEmnlp/bollywood-code and run
    
    python calcFscore.py standard.txt miOut116.txt degree116.txt spec116.txt id_bollyArtist.map 

3. Download tabulate package for python via 

    pip install tabulate

OUTPUT

1. The output is formatted as follows (via tabulate package)

##==================================================================##
##								    ##
##     =====================  ===========  ========  ==========	    ##
##     names                    precision    recall    F1-score	    ##
##     =====================  ===========  ========  ==========	    ##
##     Daler Mehndi              0.636364  0.7         0.666667	    ##
##     Aditi Singh Sharma        0.727273  0.8         0.761905	    ##
##     Rajkumari                 0.545455  0.6         0.571429	    ##
##     Shailendra Singh          0.636364  0.7         0.666667	    ##
##     Amit Kumar                0.454545  0.416667    0.434783	    ##
##     Shamshad Begum            0.363636  0.4         0.380952	    ##
##     Roop Kumar Rathod         0.727273  0.8         0.761905	    ##
##     Sowmya Raoh               0.545455  0.6         0.571429	    ##
##     Alka Yagnik               0.636364  0.411765    0.5	    ##
##        ....							    ##
##     avg                       0.598746  0.575568    0.570314	    ##
##     ==================================  ========  ==========	    ##
##							            ##
##==================================================================##


FILES

1. There are five files, they are 

  standard.txt          :   gold_standard_set.txt						            
  miOut116.txt          :   co-occurrence results for 116 artists					    
  degree116.txt         :   degree results for 116 artists						    
  spec116.txt           :   spectral mean vector distance for 116 artsts  			            
  id_bollyArtist.map    :   map of artists, integer to string 					   


FILE FORMAT


##----------------------------------------------------------------------##
##    standard.txt :					       	        ##
##   								        ##
##    num   \t  num| ...						##
##    --------------------------------------------------------------	##
##									##
##    10299   6072|67201|2579|10299|8547|9401|9634|9770|10127|106170	##
##    73017   10127|9401|9779|20039|6072|9634|9027|8832|73017|117954	##
##    ....								##
##									##
##    --------------------------------------------------------------	##
##									##
##----------------------------------------------------------------------##


##----------------------------------------------------------------------##
##    miOut116.txt :							##
##									##
##    num  \t  num/float|...						##
##    --------------------------------------------------------------    ##
##   								        ##
##    10299   6072/0.707106781187|67201/0.408248290464|2579/0.408|...	##
##    ....								##
##									##
##    --------------------------------------------------------------	##
##									##
##----------------------------------------------------------------------##



##----------------------------------------------------------------------##
##    degree116.txt :							##
##								        ##
##    num  \t num  \t name					        ##
##    --------------------------------------------------------------    ##
##								        ##
##    7241    32      Kumar Sanu				        ##
##    9401    32      Shreya Ghoshal				        ##
##    4231    27      Udit Narayan				        ##
##    2579    27      Bappi Lahiri				        ##
##    4237    26      Manna Dey					        ##
##    ....							        ##
##								        ##
##    --------------------------------------------------------------    ##
##								        ##
##----------------------------------------------------------------------##



##----------------------------------------------------------------------##
##    id_bollyArtist.map  					        ##
##   								        ##
##    num  \t num \t  name					        ##
##    -------------------------------------------------------------     ##
##   								        ##
##    2461    1       Geeta Dutt				        ##
##    2465    0       Mukesh					        ##	
##    2572    1       Asha Bhosle				        ##
##    2574    0       Hemant Kumar				        ##
##    ....							        ##
##								        ##
##    --------------------------------------------------------------    ##
##								        ##
## note:  the second column is for the gender.  0 - male ; 1 - female   ##
##								        ##
##----------------------------------------------------------------------##
