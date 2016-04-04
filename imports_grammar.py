from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

importsGrammar = Grammar(
  """
  import = ((keyword (type1 / type2 / type4 / type3 / type5_6 / type7/ type8)) / anything)*
  type1 = default_template source_template
  type2 = (space)* "*" (space)* "as" (space)* namespace_template source_template
  type3 = member_group source_template
  type4 = (space)* "{" named_namespace_template "}" (space)* source_template
  type5_6 = (space)* "{" (space)* multi (space)* "}" (space)* source_template
  type7 = default_template type5_6
  type8 = default_template named_namespace_template source_template

  multi = (multi_alias / multi_member) (named_namespace_template / member_template)*
  multi_alias = named_namespace (space)* separator
  multi_member = (space / separator)* member (space)* separator
  anything = (word / token / space)
  member_group = (space)* "{" named_template "}" (space)*
  default_template = (space / separator)* default (space / separator)*
  named_namespace_template = (space / separator)* named_namespace (space / separator)*
  namespace_template = (space / separator)* namespace (space / separator)*
  named_template = (space / separator)* named (space / separator)*
  member_template = (space / separator)* member (space / separator)*
  source_template = (space)* from (space / token)+ source token
  named_namespace = named_member (space)* "as" (space)* named_member
  from = "from"
  named = ~"\w+"
  keyword = "import"
  named_member = ~"\w+"
  separator = ","
  namespace = ~"\w+"
  default = ~"\w+"
  member = ~"\w+"
  source = ~"\w+"
  token = "=" / "{" / "}" / ":" / "." / "[" / "]" / "(" / ")" / ";" / "," / "'" / "<" / ">" / "/" / '"'
  key = ~"\w+"
  word = ~"\w+"
  space = ~"\s+"
  """)

class ImportsParser(NodeVisitor):
  def __init__(self, text):
    self.entry = {}
    self.tempMembers = [];
    self.sourceId = 1;
    ast = importsGrammar.parse(text)
    print ast
    self.visit(ast)
  def visit_named_namespace(self, n, vc):
    self.tempMembers.append([n.text])
  def visit_named(self, n, vc):
    self.tempMembers.append([n.text, n.text])
  def visit_default(self, n, vc):
    self.tempMembers.append([n.text, 'default'])
  def visit_namespace(self, n, vc):
    self.tempMembers.append([n.text, '*'])
  def visit_member(self, n, vc):
    self.tempMembers.append(n.text);
  def visit_source(self, n, vc):
    self.entry[n.text + "_" + str(self.sourceId)] = self.tempMembers;
    self.tempMembers = []
    self.sourceId += 1
  def generic_visit(self, n, vc):
    pass