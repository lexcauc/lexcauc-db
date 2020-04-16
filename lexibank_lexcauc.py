import attr
from pathlib import Path

from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar, getEvoBibAsBibtex

import lingpy
from clldutils.misc import slug
from unidecode import unidecode


@attr.s
class CustomConcept(Concept):
    Russian_Gloss = attr.ib(default=None)
    Number = attr.ib(default=None)


#@attr.s
#class CustomLanguage(Language):
#    Latitude = attr.ib(default=None)
#    Longitude = attr.ib(default=None)
#    ChineseName = attr.ib(default=None)
#    SubGroup = attr.ib(default="Bai")
#    Family = attr.ib(default="East Caucasian")
#    DialectGroup = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "lexcauc"
    concept_class = CustomConcept
    #language_class = CustomLanguage

    form_spec = FormSpec(
        brackets={"(": ")"},
        separators=";/,|",
        missing_data=("?", "-", "*", "---"),
        strip_inside_brackets=True,
        #replacements=[(" || ", ",")],
        first_form_only=True,
    )

    def cmd_download(self, **kw):
        #self.raw_dir.write("sources.bib", getEvoBibAsBibtex("Allen2007", **kw))
        pass

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("forms.csv", dicts=True)
        args.writer.add_sources()

        # TODO: add concepts with `add_concepts`
        concept_lookup = {}
        for concept in self.concepts:
            idx = concept['sort'] + "_" + slug(concept['eng'])
            args.writer.add_concept(
                ID=idx,
                Name=concept['eng'],
                Number=concept['sort'],
                Russian_Gloss=concept['rus'],
                Concepticon_ID=concept['СС_no'] if concept['СС_no'] != '0' else '',
                #Concepticon_Gloss=concept['eng'] if concept['eng'] else '',
            )
            concept_lookup[concept['sort']] = idx
        language_lookup = {}
        for language in self.languages:
            args.writer.add_language(
                    ID=language['lang.id'],
                    Name=language['lang.name'],
                    Glottocode=language['glottocode'],
                    Latitude=language['latitude'],
                    Longitude=language['longitude']
                    )
            language_lookup[language['lang.name']] = language['lang.id']

        for k in progressbar(data, desc="wl-to-cldf"):
            if (not k['subentry'] or k['subentry'] == 'sg') and k['lc.id'] in concept_lookup:
                args.writer.add_forms_from_value(
                    Language_ID=k['lang'],
                    Parameter_ID=concept_lookup[k["lc.id"]],
                    Value=k["orthographic"],
                    Source="lexcauc"
                )
            elif not k['lc.id'] in concept_lookup:
                print(k['lc.id'])
