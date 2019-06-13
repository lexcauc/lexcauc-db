# !/bin/bash
csvstack *.csv | csvcut -l -C concepticon.id,concept.ru,concept.en,opt,cx1,cx1.ru,cx1.en,cx2,cx2.ru,cx2.en,cx3,cx3.ru,cx3.en,todo  > ../forms.csv
