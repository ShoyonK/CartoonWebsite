import sys, os
sys.path.append(os.path.abspath(os.path.join('../..', 'backend')))
import anilistquery
import unittest

class TestAnilistQuery(unittest.TestCase):

    def test_parentheses_remover_basic(self):
        test_string = "Hello (Remove whatever is inside the parentheses) World!"
        actual = anilistquery.parentheses_remover(test_string)
        expected = "Hello  World!"
        self.assertEqual(expected, actual)

    def test_parentheses_remover_links(self):
        test_string = "Hello (https://www.google.com/) World!"
        actual = anilistquery.parentheses_remover(test_string)
        expected = "Hello  World!"
        self.assertEqual(expected, actual)

    def test_parentheses_remover_multiple_links(self):
        test_string = "Hello (https://www.google.com/) World (https://www.youtube.com/) Again!"
        actual = anilistquery.parentheses_remover(test_string)
        expected = "Hello  World  Again!"
        self.assertEqual(expected, actual)

    def test_tilde_remove_basic(self):
        test_string = "Hello ~~~Remove whatever is enclosed here~~~ World!"
        actual = anilistquery.tilde_remover(test_string)
        expected = "Hello  World!"
        self.assertEqual(expected, actual)

    def test_tilde_remove_multiple(self):
        test_string = "Hello ~~~Remove whatever is enclosed here~~~ World ~~~And here~~~ Again!"
        actual = anilistquery.tilde_remover(test_string)
        expected = "Hello  World  Again!"
        self.assertEqual(expected, actual)

    def test_tag_remove_basic(self):
        test_string = "Hello <br> World!"
        actual = anilistquery.tag_remover(test_string)
        expected = "Hello  World!"
        self.assertEqual(expected, actual)

    def test_tag_remove_multiple(self):
        test_string = "</p>Hello <br><br> World<p>!"
        actual = anilistquery.tag_remover(test_string)
        expected = "Hello  World!"
        self.assertEqual(expected, actual)

    def test_square_brackets_remove_basic(self):
        test_string = "Hello [My] World!"
        actual = anilistquery.square_brackets_remover(test_string)
        expected = "Hello My World!"
        self.assertEqual(expected, actual)

    def test_square_brackets_remove_multiple(self):
        test_string = "Hello [My] World [Yet] Again!"
        actual = anilistquery.square_brackets_remover(test_string)
        expected = "Hello My World Yet Again!"
        self.assertEqual(expected, actual)

    def test_links_remover_basic(self):
        test_string = 'I want to keep all of this text <a href="https://anilist.co/anime/18897/">including this</a> except the tags'
        actual = anilistquery.links_remover(test_string)
        expected = 'I want to keep all of this text including this except the tags'
        self.assertEqual(expected, actual)

    def test_links_remover_multiple(self):
        test_string = 'I want to keep all of this text <a href="https://anilist.co/anime/18897/">including this</a> as well <a href="https://anilist.co/anime/20019/">as this</a> except the tags'
        actual = anilistquery.links_remover(test_string)
        expected = 'I want to keep all of this text including this as well as this except the tags'
        self.assertEqual(expected, actual)

    def test_links_remover_multiple_diverse(self):
        test_string = 'I want to keep all of this text <a href="https://anilist.co/anime/18897/">including this</a> as well <a href="https://anilist.co/anime/20019/">as this</a> except the tags but I want to keep this <a href="https://twitter.com/hanazawa_staff">link</a>'
        actual = anilistquery.links_remover(test_string)
        expected = 'I want to keep all of this text including this as well as this except the tags but I want to keep this <a href="https://twitter.com/hanazawa_staff">link</a>'
        self.assertEqual(expected, actual)

    def test_find_spoiler_basic(self):
        test_string = "Hello my name is Naruto ~!and this is a spoiler!~"
        actual = anilistquery.find_spoiler(test_string)
        expected = ("Hello my name is Naruto ", "and this is a spoiler")
        self.assertEqual(expected, actual)

    def test_find_spoiler_multiple(self):
        test_string = "Hello my name is Naruto ~!and this is a spoiler!~ ~!and this is more spoilers!~"
        actual = anilistquery.find_spoiler(test_string)
        expected = ("Hello my name is Naruto ", "and this is a spoiler and this is more spoilers")
        self.assertEqual(expected, actual)

    def test_find_HTML_spoiler_basic(self):
        test_string = "Hello my name is Naruto <span class='markdown_spoiler'><span>and this is a spoiler.</span></span>"
        actual = anilistquery.find_HTML_spoiler(test_string)
        expected = ("Hello my name is Naruto ", "<span class='markdown_spoiler'><span>and this is a spoiler.</span></span>")
        self.assertEqual(expected, actual)

    def test_find_HTML_spoiler_multiple(self):
        test_string = "Hello my name is Naruto <span class='markdown_spoiler'><span>and this is a spoiler.</span></span> <span class='markdown_spoiler'><span>and this is more spoilers.</span></span>"
        actual = anilistquery.find_HTML_spoiler(test_string)
        expected = ("Hello my name is Naruto ", "<span class='markdown_spoiler'><span>and this is a spoiler.</span></span> <span class='markdown_spoiler'><span>and this is more spoilers.</span></span>")
        self.assertEqual(expected, actual)

    def test_char_desc_parser_short_description(self):
        test_string = "__Attribute1:__ Something1 __Attribute2:__ Something2"
        actual = anilistquery.char_desc_parser(test_string)
        expected = [("Attribute1:", " Something1 "), ("Attribute2:", " Something2")]
        self.assertEqual(expected, actual)

    def test_char_desc_parser_longer_description(self):
        test_string = "__Date of Birth:__ October 24, 1986 __Hometown:__ Tokyo, Japan __Blood Type:__ B __Awards:__ Best New Actor , Best Supporting Actor __Music:__ - Palette - Enjoy Full Revealed as the sixth member of Kiramune on October 24, 2011."
        actual = anilistquery.char_desc_parser(test_string)
        expected = [("Date of Birth:", " October 24, 1986 "), ("Hometown:", " Tokyo, Japan "), ("Blood Type:"," B "), ("Awards:", " Best New Actor , Best Supporting Actor "), ("Music:", " - Palette - Enjoy Full Revealed as the sixth member of Kiramune on October 24, 2011.")]
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()