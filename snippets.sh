Visual Studio Debugging Parameters
----------------------------------

"C:\Dev\Ling571\hw4 - PCKY\examples\data\hw4_trained.pcfg" "C:\Dev\Ling571\hw4 - PCKY\examples\data\test_sentences.txt"
"C:\Dev\Ling571\hw4 - OOV (Extra-Credit)\source\hw4_ec_trained.pcfg.improved" "C:\Dev\Ling571\hw4 - PCKY\examples\data\test_sentences.txt"
"C:\Dev\Ling571\hw4 - OOV (Extra-Credit)\examples\data\parses.train" 0.1
"C:\Dev\Ling571\hw4 - OOV (Extra-Credit)\source\hw4_ec_trained.pcfg.improved" "C:\Dev\Ling571\hw4 - PCKY\examples\data\sentences.txt"

Copying Files
-------------

lcd C:\Dev\Ling571
cd /home2/ericmcl/571/hw4_ec/
mput -r *.sh
mput *.cmd
lcd "C:\Dev\Ling571\hw4 - OOV (Extra-Credit)\source"
mput -r *.py
mput -r *.sh
mput -r *.fcfg
chmod a+x *.sh
lcd C:\Dev\Ling571


# lcd C:\Development\git\Portfolio\source
# mkdir /home2/ericmcl/571/hw5/source
# cd /home2/ericmcl/571/hw5/source
# mput -r *.cs
# lcd C:\Development\git\Portfolio\
# cd /home2/ericmcl/571/hw5


Run Scripts
-----------

cd /home2/ericmcl/571/hw5
clear
./fly.sh


Get Output
----------

cd /home2/ericmcl/571/hw5
lcd C:\Development\git\
mget -r model.*
mget -r sys.*
mget -r acc.*



