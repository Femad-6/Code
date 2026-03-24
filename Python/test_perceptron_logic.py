import unittest
from perceptron_logic import Perceptron, logic_dataset


class TestPerceptronLogic(unittest.TestCase):
    def test_and_gate(self):
        X, y = logic_dataset("AND")
        clf = Perceptron(lr=0.2, epochs=20, verbose=False).fit(X, y)
        self.assertEqual(clf.predict(X), y)

    def test_or_gate(self):
        X, y = logic_dataset("OR")
        clf = Perceptron(lr=0.2, epochs=20, verbose=False).fit(X, y)
        self.assertEqual(clf.predict(X), y)


if __name__ == "__main__":
    unittest.main(verbosity=2)
