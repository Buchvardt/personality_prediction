import wget
import os
import zipfile
from typing import Dict, List


class BigFive():
    """BigFive class that accesses open source data and makes them available as python objects.

    The ressource 'http://openpsychometrics.org/_rawdata/BIG5.zip' contains:
    - codebook
    - data
    The code book contains questionare with personality trade as ID to eac question.
    The data contains answers to the questionare.
    """

    def __init__(self, data_folder: str = './data') -> None:
        """Initialize the BigFive class.

        Arguments:
            data_folder (str): A string representing the folder to download ressources, if they do not exist.
        """

        self.data_folder = './data'
        self.file_name = os.path.join(self.data_folder, 'big5.zip')

        # Ressource url.
        self.url = 'http://openpsychometrics.org/_rawdata/BIG5.zip'

        # Check if file exists.
        if not os.path.exists(self.file_name):

            # Make directory if it does not exist.
            os.makedirs(data_folder, exist_ok=True)
            
            # Download file.
            wget.download(self.url, self.file_name)
            
            # Unzip.
            with zipfile.ZipFile(self.file_name, 'r') as zip_ref:
    
                zip_ref.extractall(self.data_folder)

    
    def get_codebook(self) -> List[str]:
        """Get the Big5 codebook.txt as lines in a list.

        The Big5 codebook contains:
        - An introduction
        - The questions
        - Method 

        Returns:
            List: List of text lines in the codebook.
        """

        file_path = os.path.join(self.data_folder, 'big5', 'codebook.txt')

        with open(file_path) as fp:
            lines = list()
            for line in fp:
                lines.append(line)

        return lines

    def get_questionare_sentences(self) -> Dict[str, List[str, int]]:

        # The questions are in lines 4 - 54.
        lines = self.get_codebook()[4:54]

        questionare_sentences = {}

        scores = self.__get_question_scores()

        for line, score in zip(lines, scores):
            # Split [Category + Number] ID from question and strip \n character.
                # Ex:
                # E6\tI have little to say.\n
                # ['E6', 'I have little to say.]
            split_line = line.strip('\n').split('\t')

            # Insert Dict[key = Question ID, value = [Question, Score]]
            questionare_sentences[split_line[0]] = [split_line[1], score]

        return questionare_sentences


    def __get_question_scores(self) -> List[int]:
        """
        
        Go To https://ipip.ori.org/newBigFive5broadTable.htm
        
        Based on this, we can se that a statemnet either contributes positively or negatively 
        to a personality trade score.
        """

        scores = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1,
                 -1, 1, -1, 1, -1, -1, -1, -1, -1, -1,
                 -1, 1, -1, 1, -1, 1, -1, 1, 1, 1,
                  1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 
                  1, -1, 1, -1, 1, -1, 1, 1, 1, 1]

        return scores

if __name__ == '__main__':

    bf = BigFive()

    questionare_sentences = bf.get_questionare_sentences()

    print(questionare_sentences)