rm -r -fo target -erroraction silentlycontinue
rm library.blb -erroraction silentlycontinue

# beet -c .\config.yaml move
beet -c .\config.yaml import '.\from'