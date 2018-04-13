import pymysql
import os
from datetime import datetime
import bleach
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n' % \
                mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)


renderer = HighlightRenderer()
markdown = mistune.Markdown(renderer=renderer)
con = pymysql.connect(host='localhost',user='root',passwd='A19990701',db='blog',port=3306,charset='utf8mb4')
path = r'C:\Users\86728\blog\post'
file = '进程与线程.md'
with open(os.path.join(path,file),'r',encoding='utf-8') as f:
    content = f.read()
    html = bleach.linkify(markdown(content))
    cur = con.cursor()
    cur.execute('insert into python values (null,%s,%s,%s,%s)',(file[:-3],content,html,datetime.utcnow()))
    cur.close()
    con.commit()
    con.close()