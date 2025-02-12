from . import InputExample
import gzip


class PairedFilesReader(object):
    """
    Reads in the a Pair Dataset, split in two files
    """

    def __init__(self, filepaths:list):
        """
        Initializes the PairedFilesReader.

        Parameters
        ----------
        filepaths : list
            A list of file paths for the paired dataset files.
        """
        self.filepaths = filepaths

    def get_examples(self, max_examples:int=0) -> list:
        """
        Reads examples from paired files.

        Parameters
        ----------
        max_examples : int, optional
            Maximum number of examples to read. Default is 0, meaning read all examples.

        Returns
        -------
        examples : list
            A list of InputExample objects.
        """
        fIns = []
        for filepath in self.filepaths:
            fIn = (
                gzip.open(filepath, "rt", encoding="utf-8")
                if filepath.endswith(".gz")
                else open(filepath, encoding="utf-8")
            )
            fIns.append(fIn)

        examples = []

        eof = False
        while not eof:
            texts = []
            for fIn in fIns:
                text = fIn.readline()

                if text == "":
                    eof = True
                    break

                texts.append(text)

            if eof:
                break

            examples.append(InputExample(guid=str(len(examples)), texts=texts, label=1))
            if max_examples > 0 and len(examples) >= max_examples:
                break

        return examples
