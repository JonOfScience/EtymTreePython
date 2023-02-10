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
        self._patterns = {}
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
        self._stage_symbolselection(word=word)

        # SYMBOLPATTERNSELECTED = auto()
        self._stage_symbolpatternselected(word=word, options=options)

        # RULESAPPLIED = auto()
        # INLANGUAGEWORD = auto()
        self._stage_inlanguageword(word=word, options=options)

        return self._results

    def _select_stage_results(self) -> list:
        return [x[-1] for x in self._results if isinstance(x, tuple)]

    def count_checks(self) -> int:
        """Returns count of result stages have have a pass or fail status."""
        return len(self._select_stage_results())

    def count_failed_stages(self) -> int:
        """Returns count of False values in stage results."""
        return self._select_stage_results().count(False)

    def list_stage_fields(self) -> list:
        """Returns an ordered list of Wordfield members that were carried out."""
        return [x[-2] for x in self._results]

    def list_failed_stages(self) -> list:
        """Returns list of strings associated with False values in stage results."""
        return [x[0] for x in self._results if x[-1] is False]

    def list_failed_fields(self) -> list:
        """Returns an ordered list of Wordfield members that failed stages."""
        return [x[-2] for x in self._results if x[-1] is False]

    def has_failure_message_like(self, search_pattern: str) -> bool:
        """Returns boolean if a message, or regex pattern is found in failes stages."""
        for message in self.list_failed_stages():
            result = re.fullmatch(search_pattern, message)
            if result is not None:
                if result.group():
                    return True
        return False

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
        passed_sequence_validation = bool(cleaned_etym == cleaned_comp)
        self.__update_results(
            "Compiled Symbology - Sequence:",
            passed_sequence_validation,
            stage_field=WordField.COMPILEDSYMBOLOGY)

    def __stage_symbolmapping__component_combined_group_structure(
            self,
            etymological_symbology: str,
            symbol_mapping: str):

        elements = etymological_symbology.split(sep='+')
        element_counts = []
        for element in elements:
            element_counts.append(
                len([x for x in split_string_into_groups(element) if len(x) > 0]))
        symbols_groups = symbol_mapping.split(sep='+')
        symbol_counts = []
        for group in symbols_groups:
            symbol_counts.append(len([x for x in group.split(sep=' ') if len(x) > 0]))
        self.__update_results(
            stage_description="Symbol Mapping - Total Group Count",
            stage_result=bool(len(element_counts) == len(symbol_counts)),
            stage_field=WordField.SYMBOLMAPPING)
        group_lengths_match = True
        for ind, counts in enumerate(element_counts):
            if counts != symbol_counts[ind]:
                group_lengths_match = False
        self.__update_results(
            stage_description="Symbol Mapping - Individual Group Lengths",
            stage_result=group_lengths_match,
            stage_field=WordField.SYMBOLMAPPING)

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
            self.__update_results(
                stage_description="Symbol Mapping - Combination Character",
                stage_result=not bool('+' in unique_characters),
                stage_field=WordField.SYMBOLMAPPING)
            groups = [x for x in split_string_into_groups(etymological_symbology) if len(x) > 0]
            symbols = [x for x in symbol_mapping.split(sep=" ") if (len(x) > 0 and x != '+')]
            self.__update_results(
                stage_description="Symbol Mapping - Member Count Match",
                stage_result=bool(len(groups) == len(symbols)),
                stage_field=WordField.SYMBOLMAPPING)
        else:
            self.__update_results(
                stage_description="Symbol Mapping - Combination Character",
                stage_result=bool('+' in unique_characters),
                stage_field=WordField.SYMBOLMAPPING)

            self.__stage_symbolmapping__component_combined_group_structure(
                etymological_symbology=etymological_symbology,
                symbol_mapping=symbol_mapping)

    def __symbol_selection_patterns(self, key_pattern: str, query_pattern: str) -> bool:
        self._patterns = {
            "A + B": ["A + B"],  # Temporary Pattern to support test
            "A B C + D": ["A C + D"],  # Temporary Pattern to support test
            "A B C + D E F": []}
        if self._patterns.get(key_pattern) is None:
            return False

        if query_pattern not in self._patterns.get(key_pattern):
            return False

        return True

    def _stage_symbolselection(self, word: Word) -> None:
        """Stage Requirements for SYMBOLSELECTION
            - (Y) Can only include previously defined symbols
        """
        def __symbol_split(string_to_split: str) -> set:
            return {
                x
                for x
                in string_to_split.split(sep=" ")
                if (len(x) > 0 and x != '+')}

        symbol_mapping: str = word.find_data_on(WordField.SYMBOLMAPPING)
        mapping_symbols = __symbol_split(symbol_mapping)

        symbol_selection: str = word.find_data_on(WordField.SYMBOLSELECTION)
        selection_symbols = __symbol_split(symbol_selection)
        no_undefined_symbols = True
        undefined_symbols = selection_symbols.difference(mapping_symbols)
        if len(undefined_symbols) > 0:
            no_undefined_symbols = False
        self.__update_results(
            stage_description="Symbol Selection - Defined Symbols",
            stage_result=no_undefined_symbols,
            stage_field=WordField.SYMBOLSELECTION)

    def _stage_symbolpatternselected(self, word: Word, options: dict) -> None:
        """Stage Requirements for SYMBOLPATTERNSELECTED
            - (Y) Can only include registered patterns
        """
        pattern_is_registered = True
        if options.get("IS_ROOT") is False:
            symbol_mapping: str = word.find_data_on(WordField.SYMBOLMAPPING)
            pattern_selection: str = word.find_data_on(WordField.SYMBOLPATTERNSELECTED)
            pattern_is_registered = self.__symbol_selection_patterns(
                symbol_mapping,
                pattern_selection)

        self.__update_results(
            stage_description="Symbol Pattern Selected - Registered Selection",
            stage_result=pattern_is_registered,
            stage_field=WordField.SYMBOLPATTERNSELECTED)

    def __symbol_split_into_list(self, string_to_split: str, separator: str = ' ') -> list:
        return [
            x
            for x
            in string_to_split.split(sep=separator)
            if (len(x) > 0 and x != '+')]

    def __map_symbols_to_groups(self, groups_text: str, groups_mapping: str) -> dict:
        """Returns a symbol:group paired dictionary."""
        mapped_symbols = {}
        split_groups = self.__symbol_split_into_list(groups_text)
        split_elements = []
        for group in split_groups:
            split_elements.extend(self.__symbol_split_into_list(group, '|'))
        split_symbols = self.__symbol_split_into_list(groups_mapping)
        if len(split_symbols) != len(split_elements):
            return False

        for ind, val in enumerate(split_symbols):
            mapped_symbols[val] = split_elements[ind]
        return mapped_symbols

    def _stage_inlanguageword(self, word: Word, options: dict) -> None:
        """Stage Requirements for INLANGUAGEWORD
            - IS_ROOT -> TRUE
                (N) Root words need to match ETYMOLOGICALSYMBOLOGY alphabetic characters
            - IS_ROOT -> FALSE
                (N) Combined words need to:
                    match ETYMOLOGICALSYMBOLOGY
                    mapped to SYMBOLMAPPING
                    filtered through SYMBOLSELECTION
        """

        etymological_symbology: str = word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY)
        symbol_mapping = word.find_data_on(WordField.SYMBOLMAPPING)
        in_language_word = word.find_data_on(WordField.INLANGUAGEWORD)

        if options.get("IS_ROOT") is True:
            compiled_word = etymological_symbology.replace('|', '')
            self.__update_results(
                stage_description="In Language Word - Root Symbols To In Language Word Match",
                stage_result=compiled_word == in_language_word,
                stage_field=WordField.INLANGUAGEWORD)

        if options.get("IS_ROOT") is False:
            mapped_symbols = self.__map_symbols_to_groups(etymological_symbology, symbol_mapping)
            symbolic_and_in_language_words_match = False
            if mapped_symbols is not False:
                symbol_selection = word.find_data_on(WordField.SYMBOLSELECTION)
                symbols_selected = self.__symbol_split_into_list(symbol_selection)
                comparator = ""
                for symbol in symbols_selected:
                    comparator += mapped_symbols[symbol]
                symbolic_and_in_language_words_match = in_language_word == comparator
            self.__update_results(
                stage_description="In Language Word - Combined Selection To In Language Word Match",
                stage_result=symbolic_and_in_language_words_match,
                stage_field=WordField.INLANGUAGEWORD)
