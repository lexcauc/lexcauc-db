#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly=TRUE)

library("readODS")
library("tidyverse")

lapply(args, read_ods, col_types = cols_only(lex.id = col_number(), 
                                            colex.id = col_number(),
                                            lc.id = col_number(),
                                            concepticon.id = col_number(),
                                            subentry = col_character(),
                                            aux = col_character(),
                                            opt = col_character(),
                                            excl = col_character(),
                                            orthographic = col_character(),
                                            phonemic = col_character(),
                                            gloss = col_character(),
                                            ipa = col_character(),
                                            cx1 = col_character(),
                                            cx1.ru = col_character(),
                                            cx1.en = col_character(),
                                            cx2 = col_character(),
                                            cx2.ru = col_character(),
                                            cx2.en = col_character(),                                            
                                            cx3 = col_character(),
                                            cx3.ru = col_character(),
                                            cx3.en = col_character(),                                            
                                            gender = col_character(),
                                            notes = col_character(),
                                            lang = col_character()
                                            )) %>% bind_rows %>% rowid_to_column("form.id") %>% write_csv("forms.csv", na = "")
