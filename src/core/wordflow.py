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
        self._stage_etymologicalsymbology(word=word, options=options)

        # COMPILEDSYMBOLOGY = auto()
        self._stage_compiledsymbology(word=word, options=options)

        # SYMBOLMAPPING = auto()
        # Number of symbols matches number of groups

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

    def _stage_translatedword(self, word: Word):
        """Stage Requirements for TRANSLATEDWORD"""
        translated_word = word.find_data_on(WordField.TRANSLATEDWORD)
        if translated_word is not None:
            if len(translated_word) > 0:
                self._results.append(("Translated Word: VALIDATION PASSED.", True))
                return
        self._results.append(("Translated Word: VALIDATION FAILED.", False))
        return

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
            for component in translated_components:
                if not component:
                    self._results.append(("Translated Components: COMBINED FAILED", False))
                    return
            self._results.append(("Translated Components: COMBINED PASSED", True))

    def _stage_inlanguagecomponents(self, word: Word, options: dict) -> None:
        """Stage Requirements for INLANGUAGECOMPONENTS
            IS_ROOT is True  -> No Check
            IS_ROOT is False -> Check
        """
        in_language_components = word.find_data_on(WordField.INLANGUAGECOMPONENTS)
        if options["IS_ROOT"] is False:
            for component in in_language_components:
                if not component:
                    self._results.append(("In Language Components: COMBINED FAILED", False))
                    return
            self._results.append(("In Language Components: COMBINED PASSED", True))

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

    def _stage_etymologicalsymbology(self, word: Word, options: dict) -> None:
        """Stage Requirements for ETYMOLOGICALSYMBOLOGY:"""
        fill = {True: "ROOT", False: "COMBINED"}[options["IS_ROOT"]]
        etymological_symbology = word.find_data_on(WordField.ETYMOLOGICALSYMBOLOGY)
        passed_character_validation = self.__character_validator(
            etymological_symbology,
            'abcdeéfghijklmnopqrstuvwxyz|[]+ ')
        if passed_character_validation:
            self._results.append((f"Etymological Symbology - Characters: {fill} PASSED", True))
        else:
            self._results.append((f"Etymological Symbology - Characters: {fill} FAILED", False))

        passed_group_validation = self.__group_validator(etymological_symbology)
        if passed_group_validation:
            self._results.append((f"Etymological Symbology - Groups: {fill} PASSED", True))
        else:
            self._results.append((f"Etymological Symbology - Groups: {fill} FAILED", False))

    def _stage_compiledsymbology(self, word: Word, options: dict) -> None:
        """Stage Requirements for COMPILEDSYMBOLOGY:
            - Characters have to be continuous except for group breaks.
            - The alpha character sequence has to match those present in etymological symbology.
            - Character groups have to be valid.
        """
        fill = {True: "ROOT", False: "COMBINED"}[options["IS_ROOT"]]
        compiled_symbology = word.find_data_on(WordField.COMPILEDSYMBOLOGY)
        passed_character_validation = self.__character_validator(
            compiled_symbology,
            'abcdeéfghijklmnopqrstuvwxyz|')
        if passed_character_validation:
            self._results.append((f"Compiled Symbology - Characters: {fill} PASSED", True))
        else:
            self._results.append((f"Compiled Symbology - Characters: {fill} FAILED", False))

        passed_group_validation = self.__group_validator(compiled_symbology)
        if passed_group_validation:
            self._results.append((f"Compiled Symbology - Groups: {fill} PASSED", True))
        else:
            self._results.append((f"Compiled Symbology - Groups: {fill} FAILED", False))
