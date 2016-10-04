from jinja2 import Environment, FileSystemLoader
import os

def img_table():
    table = {
        'head':('src','alt','title'),
        'body':[],
    }
    for img in page.images:
        src = img['src'] if img.has_attr('src') else ""
        alt = img['alt'] if img.has_attr('alt') else ""
        title = img['title'] if img.has_attr('title') else ""
        table['body'].append((src,alt,title))
    return table

page = HTMLPage(url)   # Create a page object

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('report.html')
fname = 'image-report.html'
context = {'data':img_report()}
with open('reports/report_output.html','w') as f:
    f.write(template.render(context))
print('\'%s\' created' % fname)