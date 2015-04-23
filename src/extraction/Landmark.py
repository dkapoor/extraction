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
from postprocessing.PostProcessor import RemoveHtml

MAX_EXTRACT_LENGTH=100000
ITEM_RULE = 'ItemRule'
ITERATION_RULE = 'IterationRule'
#from http://www.fon.hum.uva.nl/praat/manual/Regular_expressions_1__Special_characters.html
_specialcharacters = frozenset(
    '\^${}[]().*+?|<>-&')

def escape_regex_string(input_string):
    s = list(input_string)
    specialcharacters = _specialcharacters
    for i, c in enumerate(input_string):
        if c in specialcharacters:
            if c == "\000":
                s[i] = "\\000"
            else:
                s[i] = '\\' + c
    return input_string[:0].join(s)

def flattenResult(extraction_object, name = 'root', dont_remove_html = []):
    from postprocessing.PostProcessor import RemoveExtraSpaces
    
    result = {}
    if isinstance(extraction_object, dict):
        if 'sub_rules' in extraction_object:
            for item in extraction_object['sub_rules']:
                result[item] = flattenResult(extraction_object['sub_rules'][item], item, dont_remove_html)
        elif 'sequence' in extraction_object:
            result = flattenResult(extraction_object['sequence'], 'sequence', dont_remove_html)
        elif 'extract' in extraction_object:
            processor = RemoveExtraSpaces(extraction_object['extract'])
            value = processor.post_process()
            if name not in dont_remove_html:
                processor = RemoveHtml(value)
                value = processor.post_process()
            return value
        else:
            for extract in extraction_object:
                result[extract] = flattenResult(extraction_object[extract], extract, dont_remove_html)
    
    if isinstance(extraction_object, list):
        result = []
        for extract in extraction_object:
            result.append(flattenResult(extract, 'sequence', dont_remove_html))
    return result

def loadRule(rule_json_object):
    """ Method to load the rules - when adding a new rule it must be added to the if statement within this method. """
    name = rule_json_object['name']
    rule_type = rule_json_object['rule_type']
    sub_rules = []
    if 'sub_rules' in rule_json_object:
        sub_rules = rule_json_object['sub_rules']
    
    """ This is where we add our new type """
    if rule_type == ITEM_RULE or rule_type == 'RegexRule':
        begin_regex = rule_json_object['begin_regex']
        end_regex = rule_json_object['end_regex']
        rule = ItemRule(name, begin_regex, end_regex, sub_rules)
    if rule_type == ITERATION_RULE or rule_type == 'RegexIterationRule':
        begin_regex = rule_json_object['begin_regex']
        end_regex = rule_json_object['end_regex']
        iter_begin_regex = rule_json_object['iter_begin_regex']
        iter_end_regex = rule_json_object['iter_end_regex']
        no_first_begin_iter_rule = False
        if 'no_first_begin_iter_rule' in rule_json_object:
            no_first_begin_iter_rule = rule_json_object['no_first_begin_iter_rule']
        no_last_end_iter_rule = False
        if 'no_last_end_iter_rule' in rule_json_object:
            no_last_end_iter_rule = rule_json_object['no_last_end_iter_rule']
        
        
        rule = IterationRule(name, begin_regex, end_regex, iter_begin_regex,
                                  iter_end_regex, no_first_begin_iter_rule,
                                  no_last_end_iter_rule, sub_rules)
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
    
    @abc.abstractmethod
    def toJson(self):
        """ Method to print the rule as JSON """
    
    def set_name(self, name):
        self.name = name
        
#     def __getitem__(self, key):
#         return getattr(self, key)
#     
#     def __setitem__(self, key, value):
#         return setattr(self, key, value)
    
    def set_sub_rules(self, sub_rules):
        self.sub_rules = sub_rules
    
    def __init__(self, name, sub_rules = None):
        self.name = name
        self.sub_rules = []
        
        if sub_rules:
            self.sub_rules = RuleSet(sub_rules)

class ItemRule(Rule):
    """ Rule to apply a begin set and single end regex and return only ONE value """
    def apply(self, page_string):
        value = self.extract(page_string)
        
        if self.sub_rules:
            value['sub_rules'] = self.sub_rules.extract(value['extract'])
        
        return value
    
    def extract(self, page_string):
        try:
            begin_match_end = 0
            if self.begin_regex:
                begin_match = self.begin_rule.search(page_string)
                begin_match_end = begin_match.end()
            end_match_start = len(page_string)
            if self.end_regex:
                end_match = self.end_rule.search(page_string[begin_match_end:])
                end_match_start = end_match.start()
            extract = page_string[begin_match_end:begin_match_end+end_match_start]
            begin_index = begin_match_end
            end_index = begin_match_end+end_match_start
        except:
            extract = ''
            begin_index = -1
            end_index = -1
        return {'extract': extract,'begin_index':begin_index,'end_index':end_index}
    
    def toolTip(self):
        return 'BEGIN RULE: ' + cgi.escape(self.begin_rule.pattern) + '<hr>END RULE: ' + cgi.escape(self.end_rule.pattern)
    
    def toJson(self):
        json_dict = {}
        json_dict['name'] = self.name
        json_dict['rule_type'] = ITEM_RULE
        json_dict['begin_regex'] = self.begin_regex
        json_dict['end_regex'] = self.end_regex
        if self.sub_rules:
            json_dict['sub_rules'] = json.loads(self.sub_rules.toJson())
        return json.dumps(json_dict)
    
    def __init__(self, name, begin_regex, end_regex, sub_rules = None):
        Rule.__init__(self, name, sub_rules)
        self.begin_rule = re.compile(begin_regex, re.S)
        self.end_rule = re.compile(end_regex, re.S)
        
        self.begin_regex = begin_regex
        self.end_regex = end_regex
        
class IterationRule(ItemRule):
    """ Rule to apply a begin set and single end regex and return all values """
     
    def apply(self, page_string):
        base_extract = self.extract(page_string)
        start_page_string = base_extract['extract']
        
        sequence_number = 1
        extracts = []
        start_index = 0
        while start_index < len(start_page_string):
            try:
                if start_index == 0 and self.no_first_begin_iter_rule:
                    begin_match_start = 0
                    begin_match_end = 0
                else:
                    begin_match = self.iter_begin_rule.search(start_page_string[start_index:])
                    begin_match_start = begin_match.start()
                    begin_match_end = begin_match.end()
                
                end_match = self.iter_end_rule.search(start_page_string[start_index+begin_match_end:])
                value = start_page_string[start_index+begin_match_end:start_index+begin_match_end+end_match.start()]
                if 0 < len(value.strip()) < MAX_EXTRACT_LENGTH:
                    extracts.append({'extract':value,'begin_index':start_index+begin_match_end+base_extract['begin_index'],'end_index':start_index+begin_match_end+end_match.start()+base_extract['begin_index'],'sequence_number':sequence_number})
                    sequence_number = sequence_number + 1
                start_index = start_index+begin_match_start+end_match.start()
            except:
                if self.no_last_end_iter_rule:
                    end_match_start = len(start_page_string)
                    value = start_page_string[start_index+begin_match_end:start_index+begin_match_end+end_match_start]
                    if 0 < len(value.strip()) < MAX_EXTRACT_LENGTH:
                        extracts.append({'extract':value,'begin_index':start_index+begin_match_end+base_extract['begin_index'],'end_index':start_index+begin_match_end+end_match_start+base_extract['begin_index'],'sequence_number':sequence_number})
                        sequence_number = sequence_number + 1
                start_index = len(start_page_string)
        
        if self.sub_rules:
            for extract in extracts:
                sub_extraction = self.sub_rules.extract(extract['extract'])
                for sub_extract_name in sub_extraction:
                    sub_extraction[sub_extract_name]['begin_index'] += extract['begin_index']
                    sub_extraction[sub_extract_name]['end_index'] += extract['begin_index']
                extract['sub_rules'] = sub_extraction
                
        base_extract['sequence'] = extracts
        return base_extract
    
    def toJson(self):
        json_dict = {}
        json_dict['name'] = self.name
        json_dict['rule_type'] = ITERATION_RULE
        json_dict['begin_regex'] = self.begin_regex
        json_dict['end_regex'] = self.end_regex
        json_dict['iter_begin_regex'] = self.iter_begin_regex
        json_dict['iter_end_regex'] = self.iter_end_regex
        json_dict['no_first_begin_iter_rule'] = self.no_first_begin_iter_rule
        json_dict['no_last_end_iter_rule'] = self.no_last_end_iter_rule
        if self.sub_rules:
            json_dict['sub_rules'] = json.loads(self.sub_rules.toJson())
        return json.dumps(json_dict)
    
    def __init__(self, name, begin_regex, end_regex, iter_begin_regex,
                 iter_end_regex, no_first_begin_iter_rule = False,
                 no_last_end_iter_rule = False, sub_rules = None):
        ItemRule.__init__(self, name, begin_regex, end_regex, sub_rules)
        self.iter_begin_regex = iter_begin_regex
        self.iter_end_regex = iter_end_regex
        self.iter_begin_rule = re.compile(iter_begin_regex, re.S)
        self.iter_end_rule = re.compile(iter_end_regex, re.S)
        self.no_first_begin_iter_rule = no_first_begin_iter_rule
        self.no_last_end_iter_rule = no_last_end_iter_rule

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
    
    def add_rule(self, rule):
        self.rules.append(rule)
    
    def toJson(self):
        json_list = []
        for rule in self.rules:
            json_list.append(json.loads(rule.toJson()))
        return json.dumps(json_list, sort_keys=True, indent=2, separators=(',', ': '))
    
    def __init__(self, json_object=None):
        self.rules = []
        rule_list = []
        if json_object:
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
            opts, args = getopt.getopt(argv[1:], "fh", ["flatten", "help"])
            
            flatten = False
            
            for opt in opts:
                if opt in [('-f', ''), ('--flatten', '')]:
                    flatten = True
                if opt in [('-h', ''), ('--help', '')]:
                    raise Usage('python extraction/Landmark.py [OPTIONAL_PARAMS] [FILE_TO_EXTRACT] [RULES FILE]\n\t[OPTIONAL_PARAMS]: -f to flatten the result')
                
        except getopt.error, msg:
            raise Usage(msg)
        if len(args) > 1:
                #read the page from arg0
                page_file_str = args[0]
                with codecs.open(page_file_str, "r", "utf-8") as myfile:
                    page_str = myfile.read().encode('utf-8')

                #read the rules from arg1
                json_file_str = args[1]
        else:
            #read the page from stdin
            page_str = sys.stdin.read().encode('utf-8')

            #read the rules from arg0
            json_file_str = args[0]

        with codecs.open(json_file_str, "r", "utf-8") as myfile:
            json_str = myfile.read().encode('utf-8')
        json_object = json.loads(json_str)
        rules = RuleSet(json_object)
        
        extraction_list = rules.extract(page_str)
        
        if flatten:
            print json.dumps(flattenResult(extraction_list), sort_keys=True, indent=2, separators=(',', ': '))
        else:
            print json.dumps(extraction_list, sort_keys=True, indent=2, separators=(',', ': '))
        
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())