# Copyright:: 2015, InferLink, Corp. <developers@inferlink.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
import getopt
import re, json
import abc
import codecs
import cgi

def loadRule(rule_json_object):
    """ Method to load the rules - when adding a new rule it must be added to the if statement within this method. """
    name = rule_json_object['name']
    rule_type = rule_json_object['rule_type']
    sub_rules = []
    if 'sub_rules' in rule_json_object:
        sub_rules = rule_json_object['sub_rules']
    
    """ This is where we add our new type """
    if rule_type == 'RegexRule':
        begin_regex = rule_json_object['begin_regex']
        end_regex = rule_json_object['end_regex']
        rule = RegexRule(name, begin_regex, end_regex, sub_rules)
    if rule_type == 'RegexIterationRule':
        begin_regex = rule_json_object['begin_regex']
        end_regex = rule_json_object['end_regex']
        iter_begin_regex = rule_json_object['iter_begin_regex']
        iter_end_regex = rule_json_object['iter_end_regex']
        rule = RegexIterationRule(name, begin_regex, end_regex, iter_begin_regex, iter_end_regex, sub_rules)
        
    return rule

class Rule:
    """ Base abstract class for all rules """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def apply(self, page_string):
        """ Method to apply this rule. The output is a JSON object of the extraction"""
        
    @abc.abstractmethod
    def toolTip(self):
        """ Method that produces an HTML tooltop for this rule """
    
    def __init__(self, name, sub_rules = None):
        self.name = name
        self.sub_rules = []
        
        if sub_rules:
            self.sub_rules = RuleSet(sub_rules)

class RegexRule(Rule):
    """ Rule to apply a begin set and single end regex and return only ONE value """
    def apply(self, page_string):
        value = self.extract(page_string)
        
        if self.sub_rules:
            value = self.sub_rules.extract(value)
        
        return value
    
    def extract(self, page_string):
        try:
            begin_match = self.begin_rule.search(page_string)
            end_match = self.end_rule.search(page_string[begin_match.end():])
            value = page_string[begin_match.end():begin_match.end()+end_match.start()]
        except:
            value = ''
        return value
    
    def toolTip(self):
        return 'BEGIN RULE: ' + cgi.escape(self.begin_rule.pattern) + '<hr>END RULE: ' + cgi.escape(self.end_rule.pattern)
    
    def __init__(self, name, begin_regex, end_regex, sub_rules = None):
        Rule.__init__(self, name, sub_rules)
        self.begin_rule = re.compile(begin_regex, re.S)
        self.end_rule = re.compile(end_regex, re.S)
        
class RegexIterationRule(RegexRule):
    """ Rule to apply a begin set and single end regex and return all values """
     
    def apply(self, page_string):
        start_page_string = self.extract(page_string)
        
        values = []
        start_index = 0
        while start_index < len(start_page_string):
            try:
                begin_match = self.iter_begin_rule.search(start_page_string[start_index:])
                end_match = self.iter_end_rule.search(start_page_string[start_index+begin_match.end():])
                value = start_page_string[start_index+begin_match.end():start_index+begin_match.end()+end_match.start()]
                start_index = start_index+begin_match.start()+end_match.end()
                values.append(value)
            except:
                start_index = len(start_page_string)
         
        if self.sub_rules:
            sub_values = []
            for value in values:
                sub_extraction = self.sub_rules.extract(value)
                sub_values.append(sub_extraction)
            values = sub_values
             
        return values
    
    def __init__(self, name, begin_regex, end_regex, iter_begin_regex, iter_end_regex, sub_rules = None):
        RegexRule.__init__(self, name, begin_regex, end_regex, sub_rules)
        self.iter_begin_rule = re.compile(iter_begin_regex, re.S)
        self.iter_end_rule = re.compile(iter_end_regex, re.S)

class RuleSet:
    """A set of rules that is built from a JSON Object or JSON Array"""
    def extract(self, page_str):
        extraction_object = {}
        for rule in self.rules:
            extraction_object[rule.name] = rule.apply(page_str);
        
        return extraction_object
    
    def names(self):
        names = []
        for rule in self.rules:
            names.append(rule.name)
        return names
    
    def get(self, rule_name):
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def __init__(self, json_object):
        self.rules = []
        rule_list = []
        if isinstance(json_object, dict):
            #this is a single rule so add it to the list
            rule_list.append(json_object)
        else:
            rule_list = json_object
            
        for rule_json in rule_list:
            self.rules.append(loadRule(rule_json))

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
            raise Usage(msg)
        
        #read the page from arg0
        page_file_str = args[0]
        with codecs.open(page_file_str, "r", "utf-8") as myfile:
            page_str = myfile.read().encode('utf-8')

        #read the rules from arg1
        json_file_str = args[1]
        with codecs.open(json_file_str, "r", "utf-8") as myfile:
            json_str = myfile.read().encode('utf-8')
        
        json_object = json.loads(json_str)
        rules = RuleSet(json_object)
        extraction_list = rules.extract(page_str)
        print json.dumps(extraction_list, sort_keys=True, indent=2, separators=(',', ': '))
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())