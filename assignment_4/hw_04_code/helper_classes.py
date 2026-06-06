import json


class SubMetrics:
    def __init__(self):
        self.precision = 0.0
        self.recall = 0.0
        self.f1 = 0.0
        self.support = 0.0

    def average(self, n):
        self.precision /= n
        self.recall /= n
        self.f1 /= n
        self.support /= n

    def to_dict(self):
        return {
            "precision": self.precision,
            "recall": self.recall,
            "f1-score": self.f1,
            "support": self.support
        }

class Metrics:
    def __init__(self, java, python, accuracy, macro_avg, weighted_avg):
        self.java = java
        self.python = python
        self.accuracy = accuracy
        self.macro_avg = macro_avg
        self.weighted_avg = weighted_avg


    def average(self, n):
        self.java.average(n)
        self.python.average(n)
        self.accuracy /= n
        self.macro_avg.average(n)
        self.weighted_avg.average(n)

    def to_dict(self):
        return {
            "java": self.java.to_dict(),
            "python": self.python.to_dict(),
            "accuracy": self.accuracy,
            "macro avg": self.macro_avg.to_dict(),
            "weighted avg": self.weighted_avg.to_dict()
        }

