Visual Studio Debugging Parameters
----------------------------------

"C:\Dev\Ling571\hw4 - PCKY\examples\data\parses.train"
"C:\Dev\Ling571\hw4 - PCKY\examples\data\toy_output.txt"

"C:\Dev\Ling571\hw4 - PCKY\examples\data\toy.pcfg" "C:\Dev\Ling571\hw4 - PCKY\examples\data\toy_sentences.txt"
"C:\Dev\Ling571\hw4 - PCKY\source\hw4_trained.pcfg" "C:\Dev\Ling571\hw4 - PCKY\examples\data\sentences.txt"

svm_classify ..\examples\libSVM_test ..\examples\libSVM_model sys_output

Copying Files
-------------

lcd C:\Dev\Ling571
cd /home2/ericmcl/571/hw4/
mput -r *.sh
mput *.cmd
lcd "C:\Dev\Ling571\hw4 - PCKY\source"
mput -r *.py
mput -r *.sh
chmod a+x *.sh
lcd C:\Dev\Ling571


# lcd C:\Development\git\Portfolio\source
# mkdir /home2/ericmcl/571/hw4/source
# cd /home2/ericmcl/571/hw4/source
# mput -r *.cs
# lcd C:\Development\git\Portfolio\
# cd /home2/ericmcl/571/hw4


Run Scripts
-----------

cd /home2/ericmcl/571/hw4
clear
./fly.sh


Get Output
----------

cd /home2/ericmcl/571/hw4
lcd C:\Development\git\
mget -r model.*
mget -r sys.*
mget -r acc.*



