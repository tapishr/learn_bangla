import json

class Questions:
    questionfile = 'questions.json'

    def __init__(self):
        with open(self.questionfile) as f:
            self.questions = json.load(f)['questions']
            self.idx = 0
            self.length = len(self.questions)
    
    def next_question(self):
        if self.idx == self.length:
            self.idx = 0
        q = self.questions[self.idx]["question"]
        self.idx = self.idx + 1
        return q
    
    def validate_answer(self, ans):
        if ans == self.questions[self.idx-1]["answer"]:
            return True
        return False