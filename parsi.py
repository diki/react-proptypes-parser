from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from imports_grammar import ImportsParser

propTypesGrammar = Grammar(
  """
  propTypes = (propTypeDef / anything)*
  propTypeDef = keyword (space / token)+ (key (space / token)+ (word / token)* (separator / space)+)+ token
  anything = (word / token / space)
  token = "=" / "{" / "}" / ":" / "." / "[" / "]" / "(" / ")" / ";" / "," / "'" / "<" / ">" / "/" / '"' / "*"
  separator = ","
  keyword = "propTypes"
  key = ~"\w+"
  word = ~"\w+"
  space = ~"\s+"
  """)

f = open('test.js')
contents = f.read()
print ImportsParser(contents).entry
