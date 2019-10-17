#!/bin/bash
for i in *.xlsx
do
    soffice --invisible --nofirststartwizard --headless --norestore "macro:///LexCauc.LexCauc.convertAllData(\"file://$(realpath $i)\")"
done

Rscript --vanilla makedb.R *.processed.ods

rm *.ods

mv -f ./forms.csv ../forms.csv
