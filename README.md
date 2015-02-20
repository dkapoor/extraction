# Landmark Extraction

## Running
No third party libraries are necessary. Run the following from the command line
python Landmark.py <FILE_TO_EXTRACT_FROM> <RULES_FILE>

### Examples
```
python src/extraction/Landmark.py sample/jair/jair1.txt sample/jair/jair_rules.txt
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
python src/extraction/Landmark.py sample/jair/jair2.txt sample/jair/jair_rules.txt
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
    "iter_end_regex": "\">"
}
```
* name: the name of this rule
* rule_type: RegexRule
* begin_regex: The quote escaped regular expression to get to the beginning of where you would like to extract.
* end_regex: The quote escaped regular expression to get to the end of where you would like to extract (starting from the end of begin_regex).
* iter_begin_regex: The quote escaped regular expression for the beginning of EACH item to be repeated.
* iter_end_regex: The quote escaped regular expression for the end EACH item to be repeated (starting from the end of each iter_begin_regex).

