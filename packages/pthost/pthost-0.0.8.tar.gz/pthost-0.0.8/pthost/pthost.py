#!/usr/bin/python3
"""
    pthost - Default vhost tester

    Copyright (c) 2020 HACKER Consulting s.r.o.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of

    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__version__ = "0.0.8"

import argparse
import re
import socket
import sys
import urllib

import requests
import tldextract
from ptlibs import ptjsonlib, ptmisclib


class pthost:
    def __init__(self, args):
        self.ptjsonlib = ptjsonlib.ptjsonlib(args.json)
        self.json_no = self.ptjsonlib.add_json(SCRIPTNAME)
        self.ptjsonlib.add_data(self.json_no, {"tests": []})
        self.use_json = args.json
        self.headers = ptmisclib.get_request_headers(args)
        self.proxy = {"http": args.proxy, "https": args.proxy}
        self.method = "POST"
        self.test_types = args.test

    def run(self, args):
        ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Testing Domain: {self.get_target(args.domain, '')}\n", self.use_json))
        for index, protocol in enumerate(args.protocol):
            self.test(args, protocol=protocol)
            if index != (len(args.protocol)-1): ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json), end="\n")
        if not self.use_json:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
            for test_result in self.ptjsonlib.json_list[0]['data']['tests']:
                self.print_vulnerabilities(test_result)
                if test_result != self.ptjsonlib.json_list[0]['data']['tests'][-1]:
                    ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json), end="\n")
        else:
            ptmisclib.ptprint(ptmisclib.out_if(self.ptjsonlib.get_all_json(), "", self.use_json))


    def test(self, args, protocol):
        self.data = {"protocol": "null", "homepage": "null", "status": "null", "vulnerable": "null", "target_ip": "null", "vulns": {}, "data": {}}
        target_without_subdomain, target_with_subdomain = self.get_target(args.domain, protocol)
        target_ip = args.domain if ptmisclib.is_valid_ip_address(args.domain) else self.get_target_ip(target_with_subdomain)
        self.data.update({"protocol": protocol, "homepage": target_with_subdomain, "target_ip": target_ip})

        ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"PROTOCOL: {protocol.upper()}", self.use_json))

        if 'is-default' in self.test_types or 'open-redirect' in self.test_types or 'host-injection' in self.test_types or ('redir-to-https' in self.test_types and protocol=='http') or ('crlf' in self.test_types and protocol=='http'):
            ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Request to: {target_with_subdomain}", self.use_json))
            try:
                response_1, content_1 = self.get_response_and_content(target_with_subdomain)
                if response_1.is_redirect and ('redir-to-https' in self.test_types or 'crlf' in self.test_types) and protocol=='http':
                    self._test_redir_to_https(response_1)
                    if not self.missing_redirect_http_to_https and 'crlf' in self.test_types:
                        self._test_crlf_injection(target_with_subdomain, "when redirect from HTTP to HTTPS", "http2https")
            except requests.Timeout:
                ptmisclib.end_error("Timeout error", self.json_no, self.ptjsonlib, self.use_json)
            except requests.ConnectionError:
                ptmisclib.end_error("Server not responding", self.json_no, self.ptjsonlib, self.use_json)

        if 'redir-to-sub' in self.test_types or 'crlf' in self.test_types:
            is_redir = self._test_redir_to_sub(target_without_subdomain)
            if is_redir and 'crlf' in self.test_types:
                self._test_crlf_injection(target_without_subdomain, "when redirect to subdomain", "subdomain")
        if 'is-default' in self.test_types:
            self._test_is_default(protocol, target_ip, response_1, content_1)

        if 'subdomain-reflection-no-www' in self.test_types or 'subdomain-reflection-www' in self.test_types:
            self._test_for_reflected_subdomains(target_without_subdomain, protocol)

        if 'open-redirect' in self.test_types or 'host-injection' in self.test_types:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
            ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Request with Host header set to www.example.com", self.use_json))
            try:
                response_3, content_3 = self.get_response_and_content(target_with_subdomain, host='www.example.com')
                data = {"response_3": {'status_code': response_3.status_code}}
                if 'open-redirect' in self.test_types:
                    self._test_open_redirect(response_3)
                if 'host-injection' in self.test_types:
                    self._test_host_injection(response_3)
                self.compare_responses((response_1, content_1), (response_3, content_3))
            except requests.Timeout:
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Request timed out", "ERROR", self.use_json))
                data =  {"response_3": {'status': 'Request timed out'}}
            except requests.ConnectionError:
                data = {"response_3": {'status': 'Server not responding'}}
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Server not responding", "ERROR", self.use_json))
            finally:
                self.data['data'].update(data)
        self.ptjsonlib.json_list[0]["data"]["tests"].append(self.data)

    def _test_crlf_injection(self, url, text_test, test_type=None):
        response_crlf = requests.get(f'{url}/?foo=foo%0D%0Atestfoo:testfoo', proxies=self.proxy, headers=self.headers, allow_redirects=False, verify=False, timeout=15)
        is_vuln = None
        if response_crlf.headers.get('testfoo'):
            is_vuln = True
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Vulnerable to CRLF injection ({text_test})", "INFO", self.use_json))
        else:
            is_vuln = False
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Not vulnerable to CRLF injection ({text_test})", "INFO", self.use_json))
        self.data['vulns'].update({f'crlf_{test_type}': is_vuln})


    def _test_is_default(self, protocol, target_ip, response_1, content_1):
        # (response.status_code, content , title, response)
        ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
        ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Request to IP address: {target_ip}", self.use_json))
        try:
            response_2, content_2 = self.get_response_and_content(f'{protocol}://{target_ip}')
            data = {"response_2": {'status_code': response_2.status_code}}
            is_equal_1 = self.compare_responses((response_1, content_1), (response_2, content_2))
            if is_equal_1 and response_2.status_code == 200:
                self.is_default = True
            else:
                self.is_default = False
            self.data['vulns'].update({'is_default': self.is_default})
        except requests.Timeout:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Request timed out", "ERROR", self.use_json))
            data =  {"response_2": {'status': 'Request timed out'}}
        except requests.ConnectionError:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Server not responding", "ERROR", self.use_json))
            data = {"response_2": {'status': 'Server not responding'}}
        finally:
            self.data['data'].update(data)

    def _test_redir_to_https(self, response_1):
        self.missing_redirect_http_to_https = None
        if not response_1.headers['location'].startswith("https"):
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Missing Redirect from HTTP to HTTPS", "INFO", self.use_json))
            self.missing_redirect_http_to_https = True
        if not self.missing_redirect_http_to_https:
            self.missing_redirect_http_to_https = False
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirect to HTTPS: OK", "INFO", self.use_json))
        self.data['vulns'].update({'missing_redirect_http_to_https': self.missing_redirect_http_to_https})
        self.data['data'].update({"original_response": {'status_code': response_1.status_code}})

    def _test_redir_to_sub(self, url):
        self.missing_redirect_to_subdomain = None
        self.is_available_without_subdomain = None
        ptmisclib.ptprint(ptmisclib.out_ifnot(f" ", "", self.use_json))
        ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Request to: {url}", self.use_json))
        try:
            response_4, content_4 = self.get_response_and_content(url)
            if response_4.is_redirect:
                self.missing_redirect_to_subdomain = False
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirect to subdomain: OK", "INFO", self.use_json))
            else:
                self.missing_redirect_to_subdomain = True
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Missing Redirect to subdomain", "INFO", self.use_json))
            if response_4.status_code >= 400:
                self.is_available_without_subdomain = False
            else:
                self.is_available_without_subdomain = True
            data =  {"response_4": {'status': 'ok'}}
            return response_4.is_redirect
        except requests.Timeout:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Request timed out", "ERROR", self.use_json))
            data =  {"response_4": {'status': 'Request timed out'}}
        except requests.ConnectionError:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Server not responding", "ERROR", self.use_json))
            data = {"response_4": {'status': 'Server not responding'}}
        finally:
            self.data['data'].update(data)
            self.data['vulns'].update({'missing_redirect_to_subdomain': self.missing_redirect_to_subdomain, "is_available_without_subdomain": self.is_available_without_subdomain})

    def _test_open_redirect(self, response):
        self.open_redirect = None
        if response.headers.get('location'):
            if re.search('^(http(s)?:\/\/)?www\.example\.com', response.headers['location']):
                self.open_redirect = True
            else:
                self.open_redirect = False
        self.data['vulns'].update({'open_redirect': self.open_redirect})

    def _test_host_injection(self, response):
        self.host_injection = None
        example_in_content = re.search('(https?\:\/\/)?www\.example\.com\/?', response.text)
        if example_in_content and response.status_code == 200:
            self.host_injection = True
        else:
            self.host_injection = False
        self.data['vulns'].update({'host_injection': self.host_injection})

    def _test_for_reflected_subdomains(self, homepage_without_subdomain, protocol):
        def _test_subdomain_reflection_with_www():
            self.subdomain_reflection_with_www = None
            site_with_www = f'{protocol}://fo0o0o0o.www.{o.domain}.{o.suffix}'
            response = requests.get(site_with_www, proxies=self.proxy, headers=self.headers, allow_redirects=False, verify=False, timeout=15)
            if response.status_code == 200:
                self.subdomain_reflection_with_www = True
            else:
                self.subdomain_reflection_with_www = False
            self.data['vulns'].update({'subdomain_reflection_with_www': self.subdomain_reflection_with_www})
            self.data['data'].update({'url_reflected_subdomains_with_www': site_with_www})

        def _test_subdomain_reflection_without_www():
            self.subdomain_reflection_without_www = None
            site_without_www = f'{protocol}://fo0o0o0o.{o.domain}.{o.suffix}'
            response = requests.get(site_without_www, proxies=self.proxy, headers=self.headers, allow_redirects=False, verify=False, timeout=15)

            if response.status_code == 200:
                self.subdomain_reflection_without_www = True
            else:
                self.subdomain_reflection_without_www = False
            self.data['vulns'].update({'subdomain_reflection_without_www': self.subdomain_reflection_without_www})
            self.data['data'].update({'url_reflected_subdomains_without_www': site_without_www})

        o = tldextract.extract(homepage_without_subdomain)
        try:
            if 'subdomain-reflection-www' in self.test_types:
                _test_subdomain_reflection_with_www()
            if 'subdomain-reflection-no-www' in self.test_types:
                _test_subdomain_reflection_without_www()
        except Exception as e:
            pass

    def print_vulnerabilities(self, test_result):
        ptmisclib.ptprint(ptmisclib.out_title_ifnot(f"Results for {test_result['protocol'].upper()} protocol:", self.use_json))

        if test_result['protocol'] == "http":
            if test_result['vulns'].get('missing_redirect_http_to_https', 'not-included-in-test') == 'not-included-in-test':
                pass
            elif test_result['vulns']['missing_redirect_http_to_https'] is None:
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Could not retrive result: Test for redirect from HTTP to HTTPS", "VULN", self.use_json))
            elif test_result['vulns']['missing_redirect_http_to_https']:
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Missing Redirect from HTTP to HTTPS", "VULN", self.use_json))
            else:
                ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirect to HTTPS: OK", "NOTVULN", self.use_json))

        if test_result['vulns'].get('missing_redirect_to_subdomain', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['missing_redirect_to_subdomain'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Could not retrive result: Test for redirect to subdomain", "VULN", self.use_json))
        elif test_result['vulns']['missing_redirect_to_subdomain']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Missing Redirect to subdomain", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirect to subdomain: OK", "NOTVULN", self.use_json))

        if test_result['vulns'].get('is_default', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['is_default'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Could not retrive result: Test for default domain", "VULN", self.use_json))
        elif test_result['vulns']['is_default']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is default", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is not default", "NOTVULN", self.use_json))

        if test_result['vulns'].get('open_redirect', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['open_redirect'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Could not retrive result: Test for open redirect vulnerability", "VULN", self.use_json))
        elif test_result['vulns']['open_redirect']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Vulnerable to Open redirect", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Not vulnerable to Open redirect", "NOTVULN", self.use_json))

        if test_result['vulns'].get('host_injection', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['host_injection'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Could not retrive result: Test for default vhost", "VULN", self.use_json))
        elif test_result['vulns']['host_injection']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Vulnerable to Host header injection", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Not vulnerable to Host header injection", "NOTVULN", self.use_json))

        if test_result['vulns'].get('subdomain_reflection_with_www', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['subdomain_reflection_with_www'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Test for subdomain reflection (with www): OK", "NOTVULN", self.use_json))
        elif test_result['vulns']['subdomain_reflection_with_www']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Vulnerable to subdomain reflection ({test_result['data']['url_reflected_subdomains_with_www']})", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Not vulnerable to subdomain reflection ({test_result['data']['url_reflected_subdomains_with_www']})", "NOTVULN", self.use_json))

        if test_result['vulns'].get('subdomain_reflection_without_www', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['subdomain_reflection_without_www'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Test for subdomain reflection (without www): OK", "NOTVULN", self.use_json))
        elif test_result['vulns']['subdomain_reflection_without_www']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Vulnerable to subdomain reflection ({test_result['data']['url_reflected_subdomains_without_www']})", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Not vulnerable to subdomain reflection ({test_result['data']['url_reflected_subdomains_without_www']})", "NOTVULN", self.use_json))

        if test_result['vulns'].get('is_available_without_subdomain', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['is_available_without_subdomain'] is None:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is not available without subdomain", "VULN", self.use_json))
        elif test_result['vulns']['is_available_without_subdomain']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is available without subdomain", "NOTVULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is not available without subdomain", "VULN", self.use_json))

        if test_result['vulns'].get('crlf_subdomain', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['crlf_subdomain']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is vulnerable to CRLF (when redirect to subdomain)", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is not vulnerable to CRLF (when redirect to subdomain)", "NOTVULN", self.use_json))

        if test_result['vulns'].get('crlf_http2https', 'not-included-in-test') == 'not-included-in-test':
            pass
        elif test_result['vulns']['crlf_http2https']:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is vulnerable to CRLF (when redirect from HTTP to HTTPS)", "VULN", self.use_json))
        else:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Domain is not vulnerable to CRLF (when redirect from HTTP to HTTPS)", "NOTVULN", self.use_json))

    def get_response_and_content(self, url, host=None):
        if host:
            headers = self.headers.copy()
            headers.update({"Host": host})
        else:
            headers = self.headers
        response = requests.get(url, proxies=self.proxy, headers=headers, allow_redirects=False, verify=False, timeout=15)
        response.encoding = response.apparent_encoding
        ptmisclib.ptprint(ptmisclib.out_ifnot(f"Response status code: {response.status_code}", "INFO", self.use_json))
        if response.is_redirect and response.headers.get('location'):
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Redirect to: {response.headers['location']}", "INFO", self.use_json))
        content = self.get_content(response)
        return response, content

    def get_content(self, response):
        content = re.search(r'<title.*?>([\s\S]*?)</title>', response.text, re.IGNORECASE)
        title = ""
        if content:
            content = content[1]
            title = content
        if not content:
            content = re.search(r'<head.*?>([\s\S]*?)</head>', response.text, re.IGNORECASE)
        if type(content) == type(re.match("", "")):
            content = content[1]
        if not content:
            content = response.text
        if title:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Title: {title}", "INFO", self.use_json))
        return content

    def compare_responses(self, r1: tuple, r2: tuple):
        if r1 == r2:
            return True
        if r1[0].status_code != r2[0].status_code:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Different status code from original request to domain  ({r1[0].status_code}, {r2[0].status_code})", "INFO", self.use_json))
            return False
        if r1[1] != r2[1]:
            ptmisclib.ptprint(ptmisclib.out_ifnot(f"Different response content ({r1[1]}, {r2[1]})", "INFO", self.use_json))
            return False

    def get_target(self, domain, protocol=None):
        parsed_obj = tldextract.extract(domain)
        if not parsed_obj:
            ptmisclib.end_error("Invalid domain", self.json_no, self.ptjsonlib, self.use_json)
        is_ip = ptmisclib.is_valid_ip_address(parsed_obj[1])
        if not is_ip and not parsed_obj[2]:
            ptmisclib.end_error("Error parsing domain", self.json_no, self.ptjsonlib, self.use_json)
        if not protocol:
            # For header printing
            return parsed_obj[1] if is_ip else '.'.join(parsed_obj[1:])
        target_without_subdomain = f"{protocol}://{parsed_obj[1]}" if is_ip else f"{protocol}://{'.'.join(parsed_obj[1:])}"
        target_with_subdomain = f"{protocol}://{parsed_obj[1]}" if is_ip else f"{protocol}://{'.'.join(parsed_obj[0:])}" if parsed_obj[0] else f"{protocol}://www{'.'.join(parsed_obj[0:])}"
        return target_without_subdomain, target_with_subdomain

    def get_target_ip(self, domain):
        o = urllib.parse.urlparse(domain)
        try:
            return socket.gethostbyname(o.netloc)
        except Exception as e:
            ptmisclib.end_error("No IP address associated with hostname", self.json_no, self.ptjsonlib, self.use_json)


def get_help():
    return [
        {"description": ["Default vhost tester"]},
        {"usage": ["pthost <options>"]},
        {"usage_example": [
            "pthost -d www.example.com"
        ]},
        {"options": [
            ["-d",  "--domain",                       "<domain>",          "Test Domain"],
            ["-t",  "--test",                         "<test-type>",       "Specify test-types (default all)"],
            ["",    "-t is-default",                  "",                  "Test Default vhost"],
            ["",    "-t open-redirect",               "",                  "Test Open Redirect"],
            ["",    "-t crlf",                        "",                  "Test CRLF injection"],
            ["",    "-t host-injection",              "",                  "Test Host injection"],
            ["",    "-t redir-to-https",              "",                  "Test HTTP to HTTPS redirects"],
            ["",    "-t redir-to-sub",                "",                  "Test Subdomain redirects"],
            ["",    "-t subdomain-reflection-www",    "",                  "Test Subdomain reflection (with www)"],
            ["",    "-t subdomain-reflection-no-www", "",                  "Test Subdomain reflection (without www)"],
            ["-ua", "--user-agent",                   "<user-agent>",      "Set user agent"],
            ["-H",  "--headers",                      "<header:value>",    "Set custom headers"],
            ["-c",  "--cookie",                       "<cookie=value>",    "Set cookie(s)"],
            ["-p",  "--proxy",                        "<proxy>",           "Set proxy (e.g. http://127.0.0.1:8080)"],
            ["-P",  "--protocol",                     "<protocol>",        "Set protocol to test (HTTP, HTTPS), default both"],
            ["-j",  "--json",                         "",                  "Output in JSON format"],
            ["-v",  "--version",                      "",                  "Show script version and exit"],
            ["-h",  "--help",                         "",                  "Show this help message and exit"]
        ]
        }]


def parse_args():
    test_choices = ["is-default", "open-redirect", "crlf", "host-injection", "redir-to-https", "redir-to-sub", "subdomain-reflection-www", "subdomain-reflection-no-www"]
    parser = argparse.ArgumentParser(add_help=False, usage=f"{SCRIPTNAME} <options>")
    parser.add_argument("-d", "--domain", type=str, required=True)
    parser.add_argument("-p", "--proxy", type=str)
    parser.add_argument("-P", "--protocol", type=str.lower, nargs="+", default=["http", "https"], choices=["http", "https"])
    parser.add_argument("-t", "--test", type=str.lower, nargs="+", default=test_choices, choices=test_choices)
    parser.add_argument("-c", "--cookie", type=str, nargs="+")
    parser.add_argument("-H", "--headers", type=ptmisclib.pairs, nargs="+")
    parser.add_argument("-ua", "--user-agent", type=str, default="Penterep Tools")
    parser.add_argument("-j", "--json", action="store_true")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        ptmisclib.help_print(get_help(), SCRIPTNAME, __version__)
        sys.exit(0)
    args = parser.parse_args()
    ptmisclib.print_banner(SCRIPTNAME, __version__, args.json)
    return args


def main():
    global SCRIPTNAME
    SCRIPTNAME = "pthost"
    requests.packages.urllib3.disable_warnings()
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
    args = parse_args()
    script = pthost(args)
    script.run(args)

if __name__ == "__main__":
    main()
