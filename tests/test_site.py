"""Check published site metadata and actual static content against analysis artifacts."""
import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.canonical = []
        self.h1_count = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'h1':
            self.h1_count += 1
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical.append(attrs['href'])
        for name in ['href', 'src']:
            if name in attrs:
                self.links.append(attrs[name])


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temp.name)
        subprocess.run([sys.executable, str(ROOT / 'scripts/build_site.py'),
                        '--output', str(cls.output)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_each_page_has_unique_metadata_and_resolvable_links(self):
        for path in self.output.glob('*.html'):
            with self.subTest(page=path.name):
                page = Page()
                page.feed(path.read_text())
                self.assertEqual(page.lang, 'fr')
                self.assertEqual(page.h1_count, 1)
                self.assertEqual(len(page.ids), len(set(page.ids)))
                suffix = '' if path.name == 'index.html' else path.name
                self.assertEqual(page.canonical, [
                    'https://institut-du-numerique-responsable.github.io/Energy-Languages/' + suffix])
                for link in page.links:
                    parts = urlsplit(link)
                    if parts.scheme or parts.netloc:
                        continue
                    target = self.output / (parts.path or path.name)
                    self.assertTrue(target.is_file(), link)
                    if parts.fragment and target.suffix == '.html':
                        other = Page()
                        other.feed(target.read_text())
                        self.assertIn(parts.fragment, other.ids, link)

    def test_all_series_are_readable_without_javascript(self):
        with (ROOT / 'docs/results/series.csv').open() as stream:
            series = list(csv.DictReader(stream))
        html = (self.output / 'resultats.html').read_text()
        self.assertEqual(html.count('data-series='), len(series))
        for item in series:
            self.assertIn(item['benchmark'], html)
            self.assertIn(item['language'], html)
        self.assertIn('historiques', html)
        self.assertIn('numériquement invalides', html)

    def test_dataset_metadata_has_real_download_and_provenance(self):
        text = (self.output / 'resultats.html').read_text()
        schemas = [json.loads(value) for value in re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', text, re.S)]
        dataset = next(node for schema in schemas for node in schema['@graph']
                       if node['@type'] == 'Dataset')
        self.assertIn('historiques', dataset['description'])
        self.assertIn('greensoftwarelab', dataset['isBasedOn'])
        self.assertEqual(dataset['creator']['name'], 'Green Software Lab')
        for download in dataset['distribution']:
            name = download['contentUrl'].rsplit('/', 1)[-1]
            self.assertTrue((self.output / 'data' / name).is_file())

    def test_sitemap_lists_all_canonical_pages(self):
        text = (self.output / 'sitemap.xml').read_text()
        for suffix in ['', 'resultats.html', 'methode.html']:
            self.assertIn('https://institut-du-numerique-responsable.github.io/Energy-Languages/' + suffix + '</loc>', text)


if __name__ == '__main__':
    unittest.main()
