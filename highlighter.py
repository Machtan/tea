import re
from Qt.QtGui import QSyntaxHighlighter, QColor

PINK = QColor.fromRgb(255, 150, 230)
DEFAULT_STYLE = {
    "function": QColor.fromRgb(0xD83726),
    "comment": QColor.fromRgb(0xBD8C78),
    "keyword": QColor.fromRgb(0xB48800),
    "string": QColor.fromRgb(0x288911),
    "litstring": QColor.fromRgb(0x288911),
    "support": QColor.fromRgb(0xC37B21),
    "number": QColor.fromRgb(0x3D80A0),
    "operator": QColor.fromRgb(0x3D80A0),
    "bool": QColor.fromRgb(0x3D80A0),
}
DEFAULT_RULES = [
    ("function", re.compile(r"def ([a-zA-Z_][a-zA-Z0-9_]*)\b")),
    ("operator", re.compile(r"(\+\=|\-\=|\/\=|\*\=|\%\=|\=|\+|\-|\%|\*|\/)")),
    ("support", re.compile(r"\b(self|super|__name__|__file__|__init__|__add__|__sub__|__str__|len|abs|min|max|range|any|all|lambda|int|float|str|bytes|dict|set|list|next)\b")),
    ("keyword", re.compile(r"\b(for|in|if|elif|else|while|continue|break|def|class|return|import|from|with|as)\b")),
    ("number", re.compile(r"\b((?:0x[0-9a-fA-F]+)|(?:[0-9]+)(?:\.[0-9]*)?)\b")),
    ("bool", re.compile(r"\b(True|False)\b")),
    ("string", re.compile(r"(?:[^\\]|r?)(\"[^\"]*(?<!\\)\")")),
    ("litstring", re.compile(r"(?:[^\\]|r?)(\'[^\']*\')")),
    ("comment", re.compile(r"(#.*?$)")),
]
class Highlighter(QSyntaxHighlighter):
    def __init__(self, document, rules, style):
        super().__init__(document)
        self.document = document
        self.style = style
        self.rules = rules
    
    def highlightBlock(self, text):
        # TODO: use block states for multiline patterns
        for name, pattern in self.rules:
            for match in pattern.finditer(text):
                pat = match.groups(1)[0]
                #print("Match {}: {}!".format(name, pat))
                start = match.start(1)
                matchlen = len(pat)
                self.setFormat(start, matchlen, self.style.get(name, PINK))
                #self.setFormat(bstart, bmatchlen, self.style[name])
                #end = match.end(1)
                