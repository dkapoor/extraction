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

import abc
import re

class Processor(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def post_process(self):
        pass
    
    def __init__(self, input_string):
        self.input_string = input_string

class RemoveExtraSpaces(Processor):
    def post_process(self):
        return re.sub("\\s+", " ", self.input_string).strip()
        
    def __init__(self, input_string):
        Processor.__init__(self, input_string)

class RemoveHtml(Processor):
# Code from Fetch
#     String startAndEndOfTag = "<[^ \t][^>]*[^ \t]>";
#     String singleCharacterTag = "<[^ \t>]>";
#     String startOfTagOnly = "<([^ \t][^>]*)?$";
#     String endOfTagOnly = "^([^<]*[^ \t])?>";
#     String patternString = singleCharacterTag + "|" + startAndEndOfTag + "|" + startOfTagOnly + "|" + endOfTagOnly; 
#     try{
#       s_stripHtmlPattern = (new Perl5Compiler()).compile(patternString, Perl5Compiler.READ_ONLY_MASK | Perl5Compiler.SINGLELINE_MASK);
#     }
#
#   public static String stripHtml(String s){
#     Substitution substitution = RegExps.makeSubstitution("");
#     String text = RegExps.substituteAllMatches(s,s_stripHtmlPattern,substitution);
#     return text;
#   }
    
    def post_process(self):
        return re.sub(self.patternString, "", self.input_string)
        
    def __init__(self, input_string):
        Processor.__init__(self, input_string)
        startAndEndOfTag = "<[^ \t][^>]*[^ \t]>"
        singleCharacterTag = "<[^ \t>]>"
        startOfTagOnly = "<([^ \t][^>]*)?$"
        endOfTagOnly = "^([^<]*[^ \t])?>"
        self.patternString = singleCharacterTag + "|" + startAndEndOfTag + "|" + startOfTagOnly + "|" + endOfTagOnly
