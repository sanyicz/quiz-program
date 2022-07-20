Quiz program
written in Python

Question database:
The question are stored in a .json file. You can add questions based on the samples in the file.
_comment:
	just a comment, not used in the program
category:
	you can have a quiz in any combination of the categories
type:
	simple_choice: there is only one correct answer (one element in the answers list)
	multiple_choice: there are more than one correct answers (more elements in the answers list)
question:
	the question itself
images:
	links to images for the question
	currently not available
answers:
	see type
options:
	list of tips to select from

The program:
Importing the necessary modules: PIL import is commented out because images for question are currently not available.
The questions.json file is loaded, then a shuffled list of Question objects is created.
The QuizProgram object is created.
In the main menu you can select the desired categories for the quiz. If ready, click Start.
The questions are displayed one at a time, with answer options in a randomized order. Selecet the answer(s) and click Post answer. You can return to the main menu by clicking Main menu.
After posting the answer to the last question in the quiz, you see your performance (ratio of correct answers to number of questions in the current quiz). You can see the answers to the failed question by clicking Show next faild question.
After that you can return to the main menu.
You can quit the program by clicking Quit.
