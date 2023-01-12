import uuid
from core.core import WordField
from core.word import Word


class Wordflow:
    def __init__(self, validators=None) -> None:
        self._id = uuid.uuid4().hex
        self._label = "Base Wordflow"
        self._validators = []
        if validators is not None:
            self._validators = validators
        self._results = []

    def run_stages(self, word: Word):

        # TRANSLATEDWORD
        self._stage_translatedword(word)

        options = {
            "IS_ROOT": None}

        if self._split__has_parents(word) is False:
            self._results.append(("WORD IS ROOT"))
            options["IS_ROOT"] = True

            # NO - TRANSLATEDCOMPONENTS
            # NO - IN LANGUAGE COMPONENTS
            # YES - ETYMOLOGICAL SYMBOLOGY
        else:
            self._results.append(("WORD IS COMBINED"))
            options["IS_ROOT"] = False

        self._stage_translatedcomponents(word=word, options=options)
        # YES - TRANSLATEDCOMPONENTS
        # YES - IN LANGUAGE COMPONENTS
        # YES - ETYMOLOGICAL SYMBOLOGY

        # COMPILEDSYMBOLOGY = auto()
        # SYMBOLMAPPING = auto()
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
        return [x for x in self._results if isinstance(x, tuple)]

    def count_checks(self) -> int:
        """Returns count of result stages have have a pass or fail status."""
        return len(self._select_stage_results())

    def failed_stages(self) -> int:
        """Returns count of False values in stage results."""
        return self._select_stage_results().count(False)

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

    def _stage_translatedcomponents(self, word: Word, options: bool):
        """Stage Requirements for TRANSLATEDCOMPONENTS"""
        translated_components = word.find_data_on(WordField.TRANSLATEDCOMPONENTS)
        if options["IS_ROOT"] is False:
            for component in translated_components:
                if not component:
                    self._results.append(("Translated Components: COMBINED FAILED", False))
                    return
            self._results.append(("Translated Components: COMBINED PASSED", True))
