from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

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

importsGrammar = Grammar(
  """
  import = ((keyword (type1 / type2 / type4 / type3 / type5_6/ type7)) / anything)*
  type1 = member_template source_template
  type2 = (space)* "*" (space)* "as" (space)* member_template source_template
  type3 = member_group source_template
  type4 = (space)* "{" named_template "}" source_template
  type5_6 = (space)* "{" multi "}" (space)* source_template
  type7 = member_template (member_group)* source_template
  keyword = "import"
  from = "from"
  
  multi = (multi_alias / multi_member) (named_template / member_template)*
  multi_alias = (space / separator)* member (space)* "as" (space)* member (space)* separator
  multi_member = (space / separator)* member (space)* separator
  separator = ","
  anything = (word / token / space)
  member_group = (space)* "{" member_template "}" (space)*
  local = (space / separator)* member (space / separator)*
  named_template = member_template "as" member_template
  member_template = (space / separator)* member (space / separator)*
  source_template = (space)* from (space / token)+ source token
  member = ~"\w+"
  source = ~"\w+"
  token = "=" / "{" / "}" / ":" / "." / "[" / "]" / "(" / ")" / ";" / "," / "'" / "<" / ">" / "/" / '"'
  key = ~"\w+"
  word = ~"\w+"
  space = ~"\s+"
  """)

class ImportsParser(NodeVisitor):
  def __init__(self, text):
    # print "init"
    self.entry = {}
    self.tempMembers = [];
    self.sourceId = 1;
    ast = importsGrammar.parse(text)
    print ast;
    self.visit(ast)
  def visit_member(self, n, vc):
    # print "member"
    # print n.text
    self.tempMembers.append(n.text);
    # self.entry['name'] = n.text
  def visit_source(self, n, vc):
    # print "source"
    # print n
    # print self.sourceId
    # print self.tempMembers
    self.entry[n.text + "_" + str(self.sourceId)] = self.tempMembers;
    self.tempMembers = []
    self.sourceId += 1
    # self.tempMembers = [];
    # self.entry['gender'] = n.text
  # def visit_age(self, n, vc):
  #   self.entry['age'] = n.text
  def generic_visit(self, n, vc):
    pass

f = open('test.js')
contents = f.read()
print ImportsParser(contents).entry
