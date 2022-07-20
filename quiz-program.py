import json
from random import shuffle
##from PIL import Image, ImageTk
import tkinter as tk


class Question(object):
    def __init__(self, comment, category, question_type, question, images, answers, options):
        self.comment = comment #the first line the json object
        self.category = category
        self.type = question_type
        self.question = question
        self.images = [Image.open(image) for image in images]
        self.answers = answers
        shuffle(options)
        self.optionKeys = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.options = {}
        self.answerKeys = []
        for i in range(len(options)):
            key, option = self.optionKeys[i], options[i]
            self.options[key] = option
            if option in self.answers:
                self.answerKeys.append(key)
        if self.answerKeys == []:
            self.answerKeys = ['Z'] #if the correct answer is not among the options
        
    def check(self, guess):
        guess = guess.upper()
        if self.type == 'simple_choice':
            if guess == self.answerKeys[0]:
                return True
        elif self.type == 'multiple_choice':
            if len(guess) == len(self.answerKeys):
                i = 0
                for key in guess:
                    if key in self.answerKeys:
                        i += 1
                if i == len(guess):
                    return True
        return False

class QuizProgram(object):
    def __init__(self, window, width, question_objects):
        self.question_objects = question_objects #a list of Question objects
        self.question_objects = {}
        for question in question_objects:
            category = question.category
            if question.category not in list(self.question_objects.keys()):
                self.question_objects[category] = []
                self.question_objects[category].append(question)
            else:
                self.question_objects[category].append(question)
##        print(self.question_objects)
        self.numQuestions = len(question_objects)
        self.actQuestionIndex = 0
        self.actQuestion = None
        self.correct, self.notCorrect = 0, 0

        
        self.window = window
        self.window.columnconfigure(0, weight=1) #column=0 of window expands to the size of window (menuFrame, mainFrame also)
##        self.window.rowconfigure(0, weight=1)
        
        self.menuFrame = tk.Frame(self.window)
        self.menuFrame.grid(row=0, column=0)

        self.startButton = tk.Button(self.menuFrame, text='Start', command=self.test)
        self.startButton.grid(row=0, column=0)
        self.quitButton = tk.Button(self.menuFrame, text='Quit', command=self.quit)
        self.quitButton.grid(row=0, column=1)

        self.mainFrame = tk.Frame(self.window, borderwidth=1, relief='ridge')
        self.mainFrame.grid(row=1, column=0)

        self.wraplLengthForLabels = width

        self.main()
        
    def main(self):
        #delete or empty widgets
        for child in self.mainFrame.winfo_children():
            child.destroy()
        #create and configure widgets
        self.startButton.config(text='Start', command=self.test)
            
        _row = 0
        self.questionSettingAll = tk.IntVar() #for using all categoires
        self.questionSettingAllCheckbutton = tk.Checkbutton(self.mainFrame, variable=self.questionSettingAll, command=self.selectAll)
        self.questionSettingAllCheckbutton.grid(row=_row, column=0)
        tk.Label(self.mainFrame, text='all').grid(row=_row, column=1)
        _row += 1
        self.questionSettingVariables = {}
        for category in list(self.question_objects.keys()): #for specific categories
            cbv = tk.IntVar()
            self.questionSettingVariables[category] = cbv
            tk.Checkbutton(self.mainFrame, variable=cbv).grid(row=_row, column=0)
            tk.Label(self.mainFrame, text=category).grid(row=_row, column=1)
            _row += 1
        self.questionSettingAllCheckbutton.invoke() #this calls the command associated with the checkbutton, in order to check all other categories

    def selectAll(self):
        if self.questionSettingAll.get() == True:
            for variable in self.questionSettingVariables.values():
                variable.set(1)
        else:
            for variable in self.questionSettingVariables.values():
                variable.set(0)
        
    def test(self):
        #check question settings
        self.notCorrectQuestions = [] #self.post() adds question to this
        self.selectedCategories = []
        for category, variable in self.questionSettingVariables.items():
            if variable.get() == True:
                self.selectedCategories.append(category)
        self.questionList = []
        for category in self.selectedCategories:
            self.questionList.extend(self.question_objects[category])
        self.numQuestions = len(self.questionList)
        self.actQuestionIndex = 0
        self.actQuestion = None
        self.correct, self.notCorrect = 0, 0
        #delete or empty widgets
        for child in self.mainFrame.winfo_children():
            child.destroy()
        #create and configure widgets
        self.startButton.config(text='Main menu', command=self.main)
        self.actQuestionIndex = 0
        
        self.questionProgressLabelVar = tk.StringVar()
        self.questionProgressLabelVar.set('Question: ' + str(self.actQuestionIndex) + '/'+ str(self.numQuestions))
        self.questionProgressLabel = tk.Label(self.mainFrame, textvariable=self.questionProgressLabelVar)
        self.questionProgressLabel.grid(row=0, column=0, columnspan=5)

        self.questionLabelVar = tk.StringVar()
        self.questionLabelVar.set('')
        self.questionLabel = tk.Label(self.mainFrame, textvariable=self.questionLabelVar, wraplength=self.wraplLengthForLabels)
        self.questionLabel.grid(row=2, column=0, columnspan=5)

        self.optionsFrame = tk.Frame(self.mainFrame)
        self.optionsFrame.grid(row=3, column=0, columnspan=5)

        self.checkBoxVariables = {}
        self.postButton = tk.Button(self.mainFrame, text='Post answer', command=self.check)
        self.postButton.grid(row=4, column=0)

        self.post()

    def post(self):
        #delete or empty widgets
        self.questionProgressLabelVar.set('')
        self.questionLabelVar.set('')
        for child in self.optionsFrame.winfo_children():
            child.destroy()
        self.checkBoxVariables = {}
        #create and configure widgets
        self.actQuestion = self.questionList[self.actQuestionIndex]
        self.actQuestionIndex += 1
        if self.actQuestionIndex == self.numQuestions:
            self.postButton.config(text='Post answer and see results')#, command=self.result) #answering the last question leads to results
        self.questionProgressLabelVar.set('Question: ' + str(self.actQuestionIndex) + '/'+ str(self.numQuestions))
        self.questionLabelVar.set(self.actQuestion.question)
        _row = 0
        for key, option in self.actQuestion.options.items():
            cbv = tk.IntVar()
            self.checkBoxVariables[key] = cbv
            tk.Checkbutton(self.optionsFrame, variable=cbv).grid(row=_row, column=0)
            tk.Label(self.optionsFrame, text=key).grid(row=_row, column=1)
            tk.Label(self.optionsFrame, text=option, wraplength=self.wraplLengthForLabels).grid(row=_row, column=2, columnspan=5)
            _row += 1
##        for image in self.actQuestion.images:
##            #img = ImageTk.PhotoImage(image)
##            #self.questionImageLabel.config(image=img)
##            image.show()
        
    def check(self):
        #check if the answer is correct
        answerKey = ''
        for key, variable in self.checkBoxVariables.items():
            if variable.get() == 1:
                answerKey += key
        isCorrect = self.actQuestion.check(answerKey)
##        print(isCorrect)
        if isCorrect:
            self.correct += 1
        else:
            self.notCorrect += 1
            self.notCorrectQuestions.append(self.actQuestion)
        if self.actQuestionIndex < self.numQuestions:
            #post the next question
            self.post()
        else:
            self.result()

    def result(self):
        #delete or empty widgets
        for child in self.mainFrame.winfo_children():
            child.destroy()
        self.performance = self.correct / self.numQuestions
        performancLabelText = f'Performance: {self.performance:{1}.{4}}'
##        print(performancLabelText)
        performancLabel = tk.Label(self.mainFrame, text=performancLabelText)
        performancLabel.grid(row=0, column=0, columnspan=5)

        self.nextFailedQuestionButton = tk.Button(self.mainFrame, text='Show next failed question', command=self.showNextFailed)
        self.nextFailedQuestionButton.grid(row=1, column=0)
        self.failedFrame = tk.Frame(self.mainFrame)
        self.failedFrame.grid(row=2, column=0, columnspan=5)
        self.notCorrectIndex = 0
        self.showNextFailed()

    def showNextFailed(self):
        for child in self.failedFrame.winfo_children():
            child.destroy()
        question = self.notCorrectQuestions[self.notCorrectIndex]
        self.notCorrectIndex += 1
##        print(self.notCorrectIndex, self.notCorrect)
        if self.notCorrectIndex == self.notCorrect:
            self.nextFailedQuestionButton.config(text='Main menu', command=self.main)
        tk.Label(self.failedFrame, text=question.question, wraplength=self.wraplLengthForLabels).grid(row=0, column=0, columnspan=5)
        _row = 1
        for answer in question.answers:
            tk.Label(self.failedFrame, text='- ' + answer, wraplength=self.wraplLengthForLabels).grid(row=_row, column=0, columnspan=5)
            _row += 1
        
    def quit(self):
        self.window.destroy()


file = open("questions.json", "r", encoding='utf-8')
questions = json.load(file)
##print(questions[0])
question_objects = []
for question in questions:
    if question['question'] != "":
        Q = Question(*question.values())
        question_objects.append(Q)
shuffle(question_objects)

window = tk.Tk()
##screen_width = window.winfo_screenwidth()
##screen_height = window.winfo_screenheight()
##print(screen_width, 'x', screen_height)
screen_width, screen_height = 500, 500
window.geometry(str(screen_width) + 'x' + str(screen_height))
quizProgram = QuizProgram(window, screen_width, question_objects)
window.mainloop()
