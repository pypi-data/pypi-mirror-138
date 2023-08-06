import click
import sys
from html.parser import HTMLParser
from html import escape


@click.command()
@click.version_option()
@click.argument("input", type=click.File("r"), required=False)
def cli(input):
    """
    CLI tool for stripping hidden form values from an HTML document

    You can pipe HTML into this tool:

        curl http://... | strip-hidden-form-values > output.html

    Or pass it a filename:

        strip-hidden-form-values input.html > output.html
    """
    if input is None:
        input = sys.stdin
    parser = StripHiddenParser(sys.stdout)
    parser.feed(input.read())


class StripHiddenParser(HTMLParser):
    def __init__(self, output):
        super().__init__()
        self.output = output

    def handle_starttag(self, tag, attrs, end=">"):
        self.output.write("<{}".format(tag))
        is_hidden = (
            tag.lower() == "input" and dict(attrs).get("type", "").lower() == "hidden"
        )
        if attrs:
            for attr, value in attrs:
                if is_hidden and attr.lower() == "value":
                    value = ""
                self.output.write(' {}="{}"'.format(attr, escape(value)))
        self.output.write(end)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs, end=" />")

    def handle_endtag(self, tag):
        self.output.write("</{}>".format(tag))

    def handle_data(self, data):
        self.output.write(data)

    def handle_comment(self, data):
        self.output.write("<!--{}-->".format(data))

    def handle_entityref(self, name):
        self.output.write("&{};".format(name))

    def handle_charref(self, name):
        self.output.write("&#{};".format(name))

    def handle_decl(self, data):
        self.output.write("<!{}>".format(data))

    def handle_pi(self, data):
        self.output.write("<?{}>".format(data))

    def unknown_decl(self, data):
        self.output.write("<![{}]>".format(data))
