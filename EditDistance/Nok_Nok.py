#-*- coding: utf8 -*-
import EditDistance as ed
import unittest

comment_score = {"totally correct":0, "almost right":1, "quite close":2, "a bit confusing":3, "very confusing":4}
error_toast = "Mapping Error"
class SpellingTestCase(unittest.TestCase):
    def test_right(self):
        targeted_score = comment_score["totally correct"]
        assert ed.LevenshteinMethod("Jiang", "Jiang") == targeted_score, error_toast
        assert ed.LevenshteinMethod("Chibin", "Chibin") == targeted_score, error_toast
    def test_almost_right(self):
        targeted_score = comment_score["almost right"]
        assert ed.LevenshteinMethod("flocinaucinihilipilification", "floccinaucinihilipilification") == targeted_score, error_toast
        assert ed.LevenshteinMethod("owll", "owl") == targeted_score, error_toast
        assert ed.LevenshteinMethod("pseudopseudohipoparathyroidism", "pseudopseudohypoparathyroidism") == targeted_score, error_toast
    def test_quite_close(self):
        targeted_score = comment_score["quite close"]
        assert ed.LevenshteinMethod("ples", "please") == targeted_score, error_toast
        assert ed.LevenshteinMethod("reqird", "required") == targeted_score, error_toast
        assert ed.LevenshteinMethod("rnser", "answer") == targeted_score, error_toast
        assert ed.LevenshteinMethod("antidisestablishmentaraniasm", "antidisestablishmentarianism") == targeted_score, error_toast
        assert ed.LevenshteinMethod("wol", "owl") == targeted_score, error_toast
        assert ed.LevenshteinMethod("humuhumunukunukuapuaua‘a", "humuhumunukunukuapua‘a") == targeted_score, error_toast
    def test_a_bit_confusing(self):
        targeted_score = comment_score["a bit confusing"]
        assert ed.LevenshteinMethod("plez", "please") == targeted_score, error_toast
        assert ed.LevenshteinMethod("cnoke", "knock") == targeted_score, error_toast
        assert ed.LevenshteinMethod("reqid", "required") == targeted_score, error_toast
        assert ed.LevenshteinMethod("pneumonoultramicroscopiccilikovolkanokoniosis", "pneumonoultramicroscopicsilicovolcanokoniosis") == targeted_score, error_toast
    def test_very_confusing(self):
        targeted_score = comment_score["very confusing"]
        assert ed.LevenshteinMethod("mispeln", "misspelling") == targeted_score, error_toast
        assert ed.LevenshteinMethod("mestipenk", "mistyping") == targeted_score, error_toast

def classify_comment(rightspelling, *misspellings):
    score_comment = {value:key for key, value in comment_score.items()}
    for mis in misspellings:
        edit_dist = ed.LevenshteinMethod(mis, rightspelling)
        yield mis + "\t" +str(edit_dist) +"\t"+score_comment[edit_dist]

if __name__=="__main__":
    results = classify_comment("typo", "oooo", "opyt", "pyto", "typ", "typa", "typotypo")
    for res in results:
        print(res)
    unittest.main()

