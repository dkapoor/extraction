# Landmark Extraction

## Running
No third party libraries are necessary. Run the following from the command line

```
python Landmark.py [OPTIONAL_PARAMS] [FILE_TO_EXTRACT_FROM] RULES_FILE

[OPTIONAL_PARAMS] -f: Flatten the file
If FILE_TO_EXTRACT_FROM is not given, input will be taken on stdin.
```

### Examples
```
python extraction/Landmark.py ../sample/jair/jair1.txt ../sample/jair/jair_rules.txt
{
  "abstract": {
    "begin_index": 1784,
    "end_index": 2684,
    "extract": "Call control features (e.g., call-divert, voice-mail) are primitive options to which users can subscribe off-line to personalise their  service. The configuration of a feature subscription involves choosing and sequencing features from a catalogue and is subject to  constraints that prevent undesirable feature interactions at run-time. When the subscription requested by a user is inconsistent, one  problem is to find an optimal relaxation,  which is a generalisation of the feedback vertex  set problem on directed graphs, and thus it is an NP-hard task. We present several constraint programming formulations of the problem. We also present formulations using partial  weighted maximum Boolean satisfiability and mixed integer linear programming.  We study all these formulations by experimentally comparing them  on a variety of randomly generated instances of the feature subscription problem."
  },
  "authors": [
    {
      "end_index": 168,
      "extract": "Lesaint, D.",
      "start_index": 157
    },
    {
      "end_index": 218,
      "extract": "Mehta, D.",
      "start_index": 209
    },
    {
      "end_index": 273,
      "extract": "O'Sullivan, B.",
      "start_index": 259
    },
    {
      "end_index": 325,
      "extract": "Quesada, L.",
      "start_index": 314
    },
    {
      "end_index": 376,
      "extract": "Wilson, N.",
      "start_index": 366
    }
  ],
  "pages": {
    "begin_index": 1535,
    "end_index": 1542,
    "extract": "271-305"
  },
  "title": {
    "begin_index": 2804,
    "end_index": 2888,
    "extract": "Developing Approaches  for Solving a Telecommunications Feature Subscription Problem"
  },
  "volume": {
    "begin_index": 3199,
    "end_index": 3203,
    "extract": "2010"
  }
}

python extraction/Landmark.py -f ../sample/jair/jair1.txt ../sample/jair/jair_rules.txt
{
  "abstract": "Call control features (e.g., call-divert, voice-mail) are primitive options to which users can subscribe off-line to personalise their  service. The configuration of a feature subscription involves choosing and sequencing features from a catalogue and is subject to  constraints that prevent undesirable feature interactions at run-time. When the subscription requested by a user is inconsistent, one  problem is to find an optimal relaxation,  which is a generalisation of the feedback vertex  set problem on directed graphs, and thus it is an NP-hard task. We present several constraint programming formulations of the problem. We also present formulations using partial  weighted maximum Boolean satisfiability and mixed integer linear programming.  We study all these formulations by experimentally comparing them  on a variety of randomly generated instances of the feature subscription problem.",
  "authors": [
    "Lesaint, D.",
    "Mehta, D.",
    "O'Sullivan, B.",
    "Quesada, L.",
    "Wilson, N."
  ],
  "pages": "271-305",
  "title": "Developing Approaches  for Solving a Telecommunications Feature Subscription Problem",
  "volume": "2010"
}
```

```
python extraction/Landmark.py ../sample/jair/jair2.txt ../sample/jair/jair_rules.txt
{
  "abstract": {
    "begin_index": 1656,
    "end_index": 3587,
    "extract": "Value iteration is a powerful yet inefficient algorithm for Markov decision processes (MDPs) because it puts the majority of its effort into backing up the entire state space, which turns out to be unnecessary in many cases. In order to overcome this problem, many approaches have been proposed. Among them, ILAO* and variants of RTDP are state-of-the-art ones. These methods use reachability analysis and heuristic search to avoid some unnecessary backups. However, none of these approaches build the graphical structure of the state transitions in a pre-processing step or use the structural information to systematically decompose a problem, whereby generating an intelligent backup sequence of the state space. In this paper, we present two optimal MDP algorithms. The first algorithm,  topological value iteration (TVI), detects the structure of MDPs and backs up states based on topological sequences. It (1) divides an MDP into strongly-connected components (SCCs), and (2) solves these components sequentially. TVI outperforms VI and other state-of-the-art algorithms vastly when an MDP has multiple, close-to-equal-sized SCCs. The second algorithm,  focused  topological value iteration (FTVI), is an extension of TVI. FTVI restricts its attention to connected components that are relevant for solving the MDP. Specifically, it uses a small amount of heuristic search to eliminate provably sub-optimal actions; this pruning allows FTVI to find smaller connected components, thus running faster.  We demonstrate that FTVI outperforms TVI by an order of magnitude, averaged across several domains. Surprisingly, FTVI also significantly outperforms popular `heuristically-informed' MDP algorithms such as ILAO*, LRTDP, BRTDP and Bayesian-RTDP in many domains, sometimes by as much as two orders of magnitude. Finally, we characterize the type of domains where FTVI excels --- suggesting a way to an informed choice of solver."
  },
  "authors": [
    {
      "end_index": 118,
      "extract": "Dai, P.",
      "start_index": 111
    },
    {
      "end_index": 167,
      "extract": ", Mausam",
      "start_index": 159
    },
    {
      "end_index": 219,
      "extract": "Weld, D. S.",
      "start_index": 208
    },
    {
      "end_index": 273,
      "extract": "Goldsmith, J.",
      "start_index": 260
    }
  ],
  "pages": {
    "begin_index": 1407,
    "end_index": 1414,
    "extract": "181-209"
  },
  "title": {
    "begin_index": 3707,
    "end_index": 3745,
    "extract": "Topological Value Iteration Algorithms"
  },
  "volume": {
    "begin_index": 3999,
    "end_index": 4003,
    "extract": "2011"
  }
}

python extraction/Landmark.py -f ../sample/jair/jair2.txt ../sample/jair/jair_rules.txt
{
  "abstract": "Value iteration is a powerful yet inefficient algorithm for Markov decision processes (MDPs) because it puts the majority of its effort into backing up the entire state space, which turns out to be unnecessary in many cases. In order to overcome this problem, many approaches have been proposed. Among them, ILAO* and variants of RTDP are state-of-the-art ones. These methods use reachability analysis and heuristic search to avoid some unnecessary backups. However, none of these approaches build the graphical structure of the state transitions in a pre-processing step or use the structural information to systematically decompose a problem, whereby generating an intelligent backup sequence of the state space. In this paper, we present two optimal MDP algorithms. The first algorithm,  topological value iteration (TVI), detects the structure of MDPs and backs up states based on topological sequences. It (1) divides an MDP into strongly-connected components (SCCs), and (2) solves these components sequentially. TVI outperforms VI and other state-of-the-art algorithms vastly when an MDP has multiple, close-to-equal-sized SCCs. The second algorithm,  focused  topological value iteration (FTVI), is an extension of TVI. FTVI restricts its attention to connected components that are relevant for solving the MDP. Specifically, it uses a small amount of heuristic search to eliminate provably sub-optimal actions; this pruning allows FTVI to find smaller connected components, thus running faster.  We demonstrate that FTVI outperforms TVI by an order of magnitude, averaged across several domains. Surprisingly, FTVI also significantly outperforms popular `heuristically-informed' MDP algorithms such as ILAO*, LRTDP, BRTDP and Bayesian-RTDP in many domains, sometimes by as much as two orders of magnitude. Finally, we characterize the type of domains where FTVI excels --- suggesting a way to an informed choice of solver.",
  "authors": [
    "Dai, P.",
    ", Mausam",
    "Weld, D. S.",
    "Goldsmith, J."
  ],
  "pages": "181-209",
  "title": "Topological Value Iteration Algorithms",
  "volume": "2011"
}
```

## CREATING RULES
There are two types of rules currently that can be used to extract information from text. They are highlighted below:

### RegexRule - Used to extract one piece of content from the text
```
{
    "name": "title",
    "rule_type": "RegexRule",
    "begin_regex": "<meta name=\"citation_title\" content=\"",
    "end_regex": "\">"
}
```
* name: the name of this rule
* rule_type: RegexRule
* begin_regex: The quote escaped regular expression to get to the beginning of where you would like to extract.
* end_regex: The quote escaped regular expression to get to the end of where you would like to extract (starting from the end of begin_regex).

### RegexIterationRule - Used to extract a list of content from the text
```
{
    "name": "authors",
    "rule_type": "RegexIterationRule",
    "begin_regex": "<meta",
    "end_regex": "</div>",
    "iter_begin_regex": "citation_author\" content=\"",
    "iter_end_regex": "\">",
    "no_first_begin_iter_rule": true,
    "no_last_end_iter_rule": false
}
```
* name: the name of this rule
* rule_type: RegexRule
* begin_regex: The quote escaped regular expression to get to the beginning of where you would like to extract.
* end_regex: The quote escaped regular expression to get to the end of where you would like to extract (starting from the end of begin_regex).
* iter_begin_regex: The quote escaped regular expression for the beginning of EACH item to be repeated.
* iter_end_regex: The quote escaped regular expression for the end EACH item to be repeated (starting from the end of each iter_begin_regex).
* no_first_begin_iter_rule [Optional]: Boolean which defines if the iter_begin_regex should be used for the FIRST element of the list
* no_last_end_iter_rule [Optional]: Boolean which defines if the iter_end_regex should be used for the LAST element of the list
