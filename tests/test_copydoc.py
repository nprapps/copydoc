#!/usr/bin/env python

import unittest

from copydoc import CopyDoc

TOKENS = (
    ('HEADLINE', 'headline'),
    ('SUBHED', 'subhed'),
    ('LIVEAUDIOHEADLINE', 'live_audio_headline'),
    ('LIVEAUDIOSUBHED', 'live_audio_subhed'),
    ('BANNER', 'banner'),
    ('PHOTOCREDIT', 'credit'),
    ('MOBILEPHOTOCREDIT', 'mobile_credit'),
    ('PREVIEWPHOTOCREDIT', 'preview_credit'),
    ('PREVIEWMOBILEPHOTOCREDIT', 'preview_mobile_credit'),
    ('AUDIOURL', 'audio_url'),
    ('BACKGROUNDIMAGE', 'image'),
    ('MOBILEIMAGE', 'mobile_image'),
    ('PREVIEWBACKGROUNDIMAGE', 'preview_image'),
    ('PREVIEWMOBILEIMAGE', 'preview_mobile_image'),
    ('STORYURL', 'story_url'),
)


class CopyDocTestCase(unittest.TestCase):
    """
    Test bootstrapping postgres database
    """
    def setUp(self):
        with open('tests/testdoc.html') as f:
            html_string = f.read()

        self.parser = CopyDoc(html_string, TOKENS)
        self.contents = self.parser.soup.body.contents

    def test_num_lines(self):
        self.assertEqual(len(self.contents), 19)

    def test_h1(self):
        self._is_tag(self.contents[0], 'h1')

    def test_h1_has_no_children(self):
        child_length = len(self.contents[0].find_all())
        self.assertEqual(child_length, 0)

    def test_h2(self):
        self._is_tag(self.contents[1], 'h2')

    def test_h3(self):
        self._is_tag(self.contents[2], 'h3')

    def test_p(self):
        self._is_tag(self.contents[3], 'p')

    def test_strong(self):
        self._contains_tag(self.contents[4], 'strong')

    def test_em(self):
        self._contains_tag(self.contents[5], 'em')

    def test_u(self):
        self._contains_tag(self.contents[6], 'u')

    def test_ignore_html(self):
        self._contains_tag(self.contents[7], 'strong', 0)

    def test_a(self):
        self._contains_tag(self.contents[8], 'a')

    def test_a_count(self):
        tags = self.parser.soup.body.findAll('a')
        self.assertEqual(len(tags), 2)

    def test_ahref(self):
        href = self.contents[8].a.attrs['href'][0]
        self.assertEqual(href, 'http://npr.org')

    def test_ul(self):
        self._is_tag(self.contents[9], 'ul')

    def test_ul_li(self):
        count_li = len(self.contents[9].find_all('li'))
        self.assertEqual(count_li, 3)

    def test_ol(self):
        self._is_tag(self.contents[10], 'ol')

    def test_ol_li(self):
        count_li = len(self.contents[10].find_all('li'))
        self.assertEqual(count_li, 3)

    def test_img(self):
        self._contains_tag(self.contents[11], 'img')

    def test_strange_has_no_children(self):
        child_length = len(self.contents[12].find_all())
        self.assertEqual(child_length, 0)

    def test_strange_has_extra_space_bug(self):
        clean_string = self.parser.clean_linebreaks(self.contents[12])
        expected_string = '<p>Strange formatting</p>'
        self.assertEqual(clean_string, expected_string)

    def test_tabletag(self):
        self._is_tag(self.contents[13], 'table')

    def test_tabletd(self):
        self._contains_tag(self.contents[13], 'td', 4)

    def test_tabletr(self):
        self._contains_tag(self.contents[13], 'tr', 2)

    def test_anchortag_combination(self):
        self._contains_tag(self.contents[15], 'a')

    def test_headline_extraction(self):
        self.assertEqual(self.parser.headline, 'this is a headline')

    def test_subhed_extraction(self):
        self.assertEqual(self.parser.subhed, 'this is a subhed')

    def test_banner_extraction(self):
        self.assertEqual(self.parser.banner, 'this is a banner')

    def test_image_extraction(self):
        self.assertEqual(self.parser.image, 'http://media.npr.org/assets/img/2015/12/29/gettyimages-477258926_wide-s700-c85.jpg')

    def test_mobile_image_extraction(self):
        self.assertEqual(self.parser.mobile_image, 'https://media.giphy.com/media/3oEdv5FXteGY8iS8CY/giphy.gif')

    def test_audio_url_extraction(self):
        self.assertEqual(self.parser.audio_url, 'http://play.podtrac.com/npr-510310/npr.mc.tritondigital.com/NPR_510310/media/anon.npr-mp3/npr/nprpolitics/2016/02/20160205_nprpolitics_roundup.mp3?orgId=1&d=2261&p=510310&story=465741966&t=podcast&e=465741966&ft=pod&f=510310')

    def test_credit_extraction(self):
        self.assertEqual(self.parser.credit, 'this is a photo credit')

    def test_mobile_credit_extraction(self):
        self.assertEqual(self.parser.mobile_credit, 'this is a mobile photo credit')

    def test_iframe_markup(self):
        self.assertTrue('<iframe width="560" height="315" src="https://www.youtube.com/embed/659pppwniXA" frameborder="0" allowfullscreen></iframe>' in self.parser.__unicode__())

    def test_nbsp_markup(self):
        self.assertTrue('This is a paragraph with a non-breaking&nbsp;space.' in self.parser.__unicode__())

    def spaces_stripped(self):
        clean_string = self.parser.clean_linebreaks(self.contents[17])
        expected_string = '<p>This is a paragraph with multiple spaces.</p>'
        self.assertEqual(child_length, 0)

    def _is_tag(self, tag, tag_name):
        self.assertEqual(tag.name, tag_name)

    def _contains_tag(self, tag, tag_name, count=1):
        child_length = len(tag.findAll(tag_name))
        self.assertEqual(child_length, count)


class CopyDocLinkItalicCase(unittest.TestCase):
    """
    Test bootstrapping postgres database
    """
    def setUp(self):
        with open('tests/link_italic.html') as f:
            html_string = f.read()

        self.parser = CopyDoc(html_string, TOKENS)
        self.body = self.parser.soup.body

    def test_num_lines(self):
        self.assertEqual(len(self.body.contents), 1)

    def test_em_wrapping_all_text(self):
        self._contains_tag(self.body.contents[0], 'em', 3)

    def test_u_wrapping_link(self):
        self._contains_tag(self.body.p.u, 'a', 1)

    def _is_tag(self, tag, tag_name):
        self.assertEqual(tag.name, tag_name)

    def _contains_tag(self, tag, tag_name, count=1):
        child_length = len(tag.findAll(tag_name))
        self.assertEqual(child_length, count)


class EmptyDocCase(unittest.TestCase):
    """
    Test bootstrapping postgres database
    """
    def setUp(self):
        with open('tests/empty.html') as f:
            html_string = f.read()

        self.parser = CopyDoc(html_string, TOKENS)
        self.body = self.parser.soup.body

    def test_empty_string(self):
        self.assertEqual(str(self.parser), '')


class CopyDocSpaces(unittest.TestCase):
    """
    Test bootstrapping postgres database
    """
    def setUp(self):
        with open('tests/transcript_with_embed.html') as f:
            html_string = f.read()

        self.parser = CopyDoc(html_string, TOKENS)
        self.body = self.parser.soup.body

    def test_num_lines(self):
        self.assertEqual(len(self.body.contents), 4)

    def test_iframe_markup(self):
        self.assertTrue('<iframe width="560" height="315" src="https://www.youtube.com/embed/dZTKOBElkyg" frameborder="0" allowfullscreen></iframe>' in self.parser.__unicode__())


if __name__ == '__main__':
    unittest.main()
