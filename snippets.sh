Visual Studio Debugging Parameters
----------------------------------

"C:\Dev\Ling571\hw6 - Computational Semantics\examples\semantics_example_grammar.fcfg" "C:\Dev\Ling571\hw6 - Computational Semantics\examples\semantics_example_sentences.txt"
"C:\Dev\Ling571\hw6 - Computational Semantics\source\hw6_semantic_grammar.fcfg" "C:\Dev\Ling571\hw6 - Computational Semantics\examples\sentences.txt"
"C:\Dev\Ling571\hw6 - Computational Semantics\source\hw6_semantic_grammar.fcfg" "C:\Dev\Ling571\hw6 - Computational Semantics\examples\sentences.txt"
"C:\Dev\Ling571\hw6 - Computational Semantics\source\hw6_semantic_grammar.fcfg" "C:\Dev\Ling571\hw6 - Computational Semantics\examples\test_sentence.txt"

Copying Files
-------------

lcd C:\Dev\Ling571
cd /home2/ericmcl/571/hw6/
mput -r *.sh
mput *.cmd
lcd "C:\Dev\Ling571\hw6 - Computational Semantics\source"
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



