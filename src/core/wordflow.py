"""Library for measuring validity of Word entries in a Lexicon"""
import uuid
import re
from core.core import WordField, split_string_into_groups
from core.word import Word


class Wordflow:
    """Pipeline integrating stages to provide validity statistics."""
    def __init__(self, validators=None) -> None:
        self._id = uuid.uuid4().hex
        self._label = "Base Wordflow"
        self._validators = []
        if validators is not None:
            self._validators = validators
        self._results = []

    def __update_results(
            self,
            stage_description: str,
            stage_result: bool,
            stage_field: WordField = None) -> None:

        result_text = {True: "PASSED", False: "FAILED"}
        self._results.append(
            (stage_description + " " + result_text[stage_result], stage_field, stage_result))

    def run_stages(self, word: Word) -> list:
        """Calculates validity of word with regards to predefined conditions."""
        # TRANSLATEDWORD
        self._stage_translatedword(word)

        options = {
            "IS_ROOT": None}

        if self._split__has_parents(word) is False:
            self._results.append(("WORD IS ROOT"))
            options["IS_ROOT"] = True
            # NO - IN LANGUAGE COMPONENTS
            # YES - ETYMOLOGICAL SYMBOLOGY
        else:
            self._results.append(("WORD IS COMBINED"))
            options["IS_ROOT"] = False

        # TRANSLATED COMPONENTS
        self._stage_translatedcomponents(word=word, options=options)

        # IN LANGUAGE COMPONENTS
        self._stage_inlanguagecomponents(word=word, options=options)

        # ETYMOLOGICAL SYMBOLOGY
        self._stage_etymologicalsymbology(word=word)

        # COMPILEDSYMBOLOGY = auto()
        self._stage_compiledsymbology(word=word)

        # SYMBOLMAPPING = auto()
        self._stage_symbolmapping(word=word, options=options)

        # SYMBOLSELECTION = auto()
        # SYMBOLPATTERNSELECTED = auto()
        # RULESAPPLIED = auto()
        # INLANGUAGEWORD = auto()
        # VERSIONHISTORY = auto()
        # HASBEENMODIFIED = auto()
        # HASMODIFIEDANCESTOR = auto()
        # RESOLVEDHISTORYITEMS = auto()
        # ISRELATEDTO = auto()
        # UID = auto()

        return self._results

    def _select_stage_results(self) -> list:
        return [x[-1] for x in self._results if isinstance(x, tuple)]

    def count_checks(self) -> int:
        """Returns count of result stages have have a pass or fail status."""
        return len(self._select_stage_results())

    def count_failed_stages(self) -> int:
        """Returns count of False values in stage results."""
        return self._select_stage_results().count(False)

    def list_failed_stages(self) -> list:
        """Returns list of strings associated with False values in stage results."""
        return [x[0] for x in self._results if x[-1] is False]

    def list_failed_fields(self) -> list:
        """Returns an ordered list of Wordfield members that failed stages."""
        return [x[-2] for x in self._results if x[-1] is False]

    def _stage_translatedword(self, word: Word):
        """Stage Requirements for TRANSLATEDWORD"""
        translated_word = word.find_data_on(WordField.TRANSLATEDWORD)
        validated = False
        if translated_word is not None:
            if len(translated_word) > 0:
                validated = True
        self.__update_results(
            stage_description="Translated Word: VALIDATION",
            stage_result=validated,
            stage_field=WordField.TRANSLATEDWORD)

    def _split__has_parents(self, word: Word):
        if len(word.find_data_on(WordField.TRANSLATEDCOMPONENTS)) > 0:
            return True
        return False

    def _stage_translatedcomponents(self, word: Word, options: dict) -> None:
        """Stage Requirements for TRANSLATEDCOMPONENTS
            IS_ROOT is True  -> No Check
            IS_ROOT is False -> Check
        """
        translated_components = word.find_data_on(WordField.TRANSLATEDCOMPONENTS)
        if options["IS_ROOT"] is False:
            components_valid = True
            for component in translated_components:
                if not component:
                    components_valid = False
                    break
            self.__update_results(
                stage_description="Translated Components: COMBINED",
                stage_result=components_valid,
                stage_field=WordField.TRANSLATEDCOMPONENTS)

    def _stage_inlanguagecomponents(self, word: Word, options: dict) -> None:
        """Stage Requirements for INLANGUAGECOMPONENTS
            IS_ROOT is True  -> No Check
            IS_ROOT is False -> Check
        """
        in_language_components = word.find_data_on(WordField.INLANGUAGECOMPONENTS)
        if options["IS_ROOT"] is False:
            components_valid = True
            for component in in_language_components:
                if not component:
                    components_valid = False
                    break
            self.__update_results(
                stage_description="In Language Components: COMBINED",
                stage_result=components_valid,
                stage_field=WordField.INLANGUAGECOMPONENTS)

    def __character_validator(self, text_to_validate: str, acceptable_characters: str) -> bool:
        characters = set(text_to_validate)
        if characters.issubset(acceptable_characters):
            return True
        return False

    def __group_validator(self, text_to_validate: str) -> bool:
        string_set = split_string_into_groups(text_to_validate)
        for group in [x for x in string_set if x]:
            single_consonants = re.match(
                "^[aeioué]{0,2}[bcdfghjklmnpqrstvwxyz][aeioué]{0,2}$",
                group)
            double_consonants = re.match(
                "(^[aeioué]?(th|sh|ch){1}[aeioué]?$)",
                group)
            if single_consonants is None and double_consonants is None:
                return False
        return True

    def _stage_etymologicalsymbology(self, word: Word) -> None:
        """Stage Requirements for ETYMOLOGICALSYMBOLOGY:"""
        etymological_symbology = word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY)
        passed_character_validation = self.__character_validator(
            etymological_symbology,
            'abcdeéfghijklmnopqrstuvwxyz|[]+ ')
        self.__update_results(
            stage_description="Etymological Symbology - Characters:",
            stage_result=passed_character_validation,
            stage_field=WordField.ETYMOLOGICALSYMBOLOGY)

        passed_group_validation = self.__group_validator(etymological_symbology)
        self.__update_results(
            stage_description="Etymological Symbology - Groups:",
            stage_result=passed_group_validation,
            stage_field=WordField.ETYMOLOGICALSYMBOLOGY)

    def _stage_compiledsymbology(self, word: Word) -> None:
        """Stage Requirements for COMPILEDSYMBOLOGY:
            - (Y) Characters have to be valid (so will be continuous except for group breaks).
            - (Y) Groups have to be valid.
            - (Y) The alpha character sequence has to match those present in etymological symbology.
        """
        compiled_symbology = word.find_data_on(WordField.COMPILEDSYMBOLOGY)
        passed_character_validation = self.__character_validator(
            compiled_symbology,
            'abcdeéfghijklmnopqrstuvwxyz|')
        self.__update_results(
            "Compiled Symbology - Characters:",
            passed_character_validation,
            stage_field=WordField.COMPILEDSYMBOLOGY)

        passed_group_validation = self.__group_validator(compiled_symbology)
        self.__update_results(
            "Compiled Symbology - Groups:",
            passed_group_validation,
            stage_field=WordField.COMPILEDSYMBOLOGY)

        etymological_symbology = word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY)
        cleaned_etym = [x for x in etymological_symbology if str.isalpha(x)]
        cleaned_comp = [x for x in compiled_symbology if str.isalpha(x)]
        passed_sequence_validation = True if cleaned_etym == cleaned_comp else False
        self.__update_results(
            "Compiled Symbology - Sequence:",
            passed_sequence_validation,
            stage_field=WordField.COMPILEDSYMBOLOGY)

    def _stage_symbolmapping(self, word: Word, options: dict) -> None:
        """Stage Requirements for SYMBOLMAPPING:
            - IS_ROOT -> TRUE
                (Y) CANNOT include combination character (no '+')
                (Y) Symbol count matches ETYMOLOGICALSYMBOLOGY
            - IS_ROOT -> FALSE
                (Y) Combined words MUST include combination character ('+')
                (Y) The number of etymological symbol groups must match symbol mapping groups
                (Y) In each combination element mapping symbols must match group count
        """
        symbol_mapping: str = word.find_data_on(WordField.SYMBOLMAPPING)
        etymological_symbology: str = word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY)
        unique_characters = set(symbol_mapping)
        if options["IS_ROOT"] is True:
            combinator_present = False if '+' in unique_characters else True
            self.__update_results(
                stage_description="Symbol Mapping - Combination Character",
                stage_result=combinator_present,
                stage_field=WordField.SYMBOLMAPPING)
            groups = [x for x in split_string_into_groups(etymological_symbology) if len(x) > 0]
            symbols = [x for x in symbol_mapping.split(sep=" ") if (len(x) > 0 and x != '+')]
            group_and_symbols_match = True if len(groups) == len(symbols) else False
            self.__update_results(
                stage_description="Symbol Mapping - Member Count Match",
                stage_result=group_and_symbols_match,
                stage_field=WordField.SYMBOLMAPPING)
        else:
            combinator_present = True if '+' in unique_characters else False
            self.__update_results(
                stage_description="Symbol Mapping - Combination Character",
                stage_result=combinator_present,
                stage_field=WordField.SYMBOLMAPPING)
            elements = etymological_symbology.split(sep='+')
            element_counts = []
            for element in elements:
                element_counts.append(
                    len([x for x in split_string_into_groups(element) if len(x) > 0]))
            symbols_groups = symbol_mapping.split(sep='+')
            symbol_counts = []
            for group in symbols_groups:
                symbol_counts.append(len([x for x in group.split(sep=' ') if len(x) > 0]))
            group_counts_match = True if len(element_counts) == len(symbol_counts) else False
            self.__update_results(
                stage_description="Symbol Mapping - Total Group Count",
                stage_result=group_counts_match,
                stage_field=WordField.SYMBOLMAPPING)
            group_lengths_match = True
            for ind, counts in enumerate(element_counts):
                if counts != symbol_counts[ind]:
                    group_lengths_match = False
            self.__update_results(
                stage_description="Symbol Mapping - Individual Group Lengths",
                stage_result=group_lengths_match,
                stage_field=WordField.SYMBOLMAPPING)
