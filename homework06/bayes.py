import csv
import math
import string
from collections import Counter


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        # коэффициент сглаживания
        self.alpha = alpha
        self.all_labels = []
        self.label_lst = []
        self.words_labels = []
        self.words_lst = []
        # словарик для меток и из вероятностей
        self.label_probability = {}
        # словарик для слов и их вероятностей
        self.word_probability = {}

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.all_labels = dict(Counter(y))
        # для меток в all_lables (списке?)
        for label in self.all_labels:
            # вероятность = кол-во раз, когда метка встречается, делённое на длину y (на кол-во меток всего)
            probability = self.all_labels[label] / len(y)
            self.label_probability.update({label: probability})

        # создаём список с рабочими данными
        working_data = []
        # список слов
        words_lst = []
        #  возвращает словарик из {элемент списка меток, 0}
        self.label_lst = dict.fromkeys(self.all_labels, 0)

        print(self.all_labels)
        # X - предложение, y - метка (объединение)
        for sentence, label in zip(X, y):
            # разделяем слова в предложении
            words = sentence.split()
            for word in words:
                # в список с рабочими данными добавляем
                working_data.append((word, label))
                # добавляем отделённые слова в список слов
                words_lst.append(word)
                # наращиваем метки
                self.label_lst[label] += 1

        # подсчет уникальных слов в каждом лейбле, запис. в словарик
        self.words_labels = dict(Counter(working_data))
        print("words_labels", self.words_labels)
        words_amount = dict(Counter(words_lst))
        self.word_probability.fromkeys(words_amount)

        # для слова в количестве слов (???)
        for word in words_amount:
            current = dict.fromkeys(self.all_labels)
            # сглаживание лапласа - для меток изсписка меток по ф-ле
            for label in self.all_labels:
                n_c = self.label_lst[label]
                n_ic = self.words_labels.get((word, label), 0)
                d = len(words_amount)
                alpha = self.alpha
                current[label] = (n_ic + alpha) / (n_c + alpha * d)

            self.word_probability[word] = current

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """

        print(self.label_probability)

        prediction_labels = []
        # слова получаются разделением предложений по пробелам
        words = X.split()

        for index in self.label_probability:
            current_amount = self.label_probability[index]
            # print("index", index)
            print("current_amount: ", current_amount)

            total_amount = math.log(current_amount, math.e)

            for word in words:
                word_dict = self.word_probability.get(word, None)

                if word_dict:
                    total_amount += (math.log(word_dict[index], math.e))

            # добавляем в список кол-во, высчитанное по формуле и индекс
            prediction_labels.append((total_amount, index))
            print("prediction_labels:", prediction_labels)
        _, answer = max(prediction_labels)

        print("answer:", answer)
        return answer

    def score(self, X_test, y_test) -> float:
        """ Returns the mean accuracy on the given test data and labels. """

        correct = 0
        for i in range(len(X_test)):
            answer = self.predict(X_test[i])
            if answer == y_test[i]:
                correct += 1

        return correct / len(y_test)
        pass


with open("SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))


    def clean(s):
        translator = str.maketrans("", "", string.punctuation)
        return s.translate(translator)

X, y = [], []
for target, msg in data:
    X.append(msg)
    y.append(target)

X = [clean(x).lower() for x in X]

X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = NaiveBayesClassifier(1)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
