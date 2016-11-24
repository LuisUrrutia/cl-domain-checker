"""Test module for clChecker"""
import unittest
from clchecker.clchecker import check, domain_checker, whois, _is_valid_domain, _parse_whois_data



class TestClCheckerMethods(unittest.TestCase):

    general_message = 'Testing domain \'{0}\''

    def test_valid_domain(self):
        valid_domains_to_test = [
            'bug.cl',
            'ñato.cl',
            'árbol.cl',
            'entrañas.cl',
            'canción.cl',
            'ñandú.cl',
            'ñandú123.cl',
            '123ñandú.cl',
            '01234567890.cl',
            '0123something7890.cl',
            'SOMETHING.CL',
            'S0meTH1ng.Cl'
        ]

        invalid_domains_to_test = [
            'www.bug.cl',
            'http://bug.cl',
            'https://something.cl'
            'something.cl/',
            'something',
            '123something',
            '123something.cl/dir',
            '//something123.cl',
            '.something.cl',
            'some thing.cl',
            'something .cl'
        ]

        for valid_domain in valid_domains_to_test:
            self.assertTrue(_is_valid_domain(valid_domain), self.general_message.format(valid_domain))

        for invalid_domain in invalid_domains_to_test:
            self.assertFalse(_is_valid_domain(invalid_domain), self.general_message.format(invalid_domain))

    def test_check(self):
        from clchecker.exception import WhoisServerNotResponding, WhoisConnectionError

        registered_domains = [
            'dxpress.cl',
            'bug.cl',
            'hack.cl',
            'programadores.cl',
            'google.cl'
        ]

        not_registered_domains = [
            'dexpres.cl',
            'b8g.cl',
            'h4ck.cl',
            'pr0gramadores.cl',
            'g00000gle.cl'
        ]

        for registered_domain in registered_domains:
            try:
                self.assertTrue(check(registered_domain), self.general_message.format(registered_domain))
            except WhoisServerNotResponding:
                pass
            except WhoisConnectionError:
                pass
            except Exception as e:
                self.fail('Unexpected exception raised: ', e)

        for not_registered_domain in not_registered_domains:
            try:
                self.assertFalse(check(not_registered_domain), self.general_message.format(not_registered_domain))
            except WhoisServerNotResponding:
                pass
            except WhoisConnectionError:
                pass
            except Exception as e:
                self.fail('Unexpected exception raised: ', e)


if __name__ == '__main__':
    unittest.main()