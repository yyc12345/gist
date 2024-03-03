import markdown
import markdown.extensions.toc
import argparse

_gTemplateHead: str = '''
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
'''
_gTemplateTail: str = '''
    </body>
</html>
'''

def BuildSimpleMarkdown(input_file: str, output_file: str) -> None:
    """
    Build a simple markdown.

    input_file: The path to input markdown file.
    output_file: The path to output html file. You should make sure that
    this output html file can visit `style.css` provided with this script.
    """
    with open(input_file, 'r', encoding='utf-8') as fr:
        with open(output_file, 'w', encoding='utf-8') as fw:
            fw.write(_gTemplateHead)
            fw.write(
                markdown.markdown(
                    fr.read(), 
                    output_format='html5',
                    extensions=[
                        'markdown.extensions.admonition',
                        'markdown.extensions.tables',
                        # table of content should not include header (h1)
                        #markdown.extensions.toc.TocExtension(baselevel=2),
                        'markdown.extensions.toc',
                        'markdown.extensions.fenced_code'
                    ]
                )
            )
            fw.write(_gTemplateTail)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple Markdown Generator')
    parser.add_argument('-i', '--input', required=True, action='store', dest='input_file')
    parser.add_argument('-o', '--output', required=True, action='store', dest='output_file')
    args = parser.parse_args()
    BuildSimpleMarkdown(args.input_file, args.output_file)
