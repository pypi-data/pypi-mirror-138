import os,sys
import time
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
from os import PathLike
import shutil

from typing import Union

from notion2md.console.formatter import *
from notion2md.config import Config
from notion2md.notion_api import get_children
from notion2md.convertor.block import BlockConvertor
from notion2md.exceptions import UnInitializedConfigException
from notion2md.console.ui.indicator import Indicator

from cleo.helpers import option
from cleo.commands.command import Command

def zip_dir(zip_name: str, source_dir: Union[str, PathLike]):
    src_path = Path(source_dir).expanduser().resolve(strict=True)
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zf:
        for file in src_path.rglob('*'):
            zf.write(file, file.relative_to(src_path))

class ExportBlockCommand(Command):
    name = "block"
    description = "Export a Notion block object to markdown."

    options = [
        option("url", "u", "The url of Notion block object.", flag=False),
        option("id", "i", "The id of Notion block object.", flag=False),
        option("name", "n", "The name of Notion block object", flag=False),
        option("path", "p", "The path to save exported markdown file.", flag=False),
        option("download", None, "Download files/images inside of the block object", flag=True),
        option("unzipped", None, "Download unzipped output files/images", flag=True),
    ]
    help = """The block command retrieves and exports Notion <highlight>block object</highlight> to markdownfile.

- By default, the <highlight>id</highlight> of the block will be the name of markdown file, but if you path a value after <code>--name/-n</code>, the value will be the name of the markdown file.
    
- It will save the exported zip file in the path(<highlight>"notion-output/"</highlight> or <highlight>specific path you entered</highlight>)

- By default, it won't save files/images in the block object, but if you pass <code>--download</code> option, it will download files/images in the path(<highlight>"notion-output/"</highlight> or <highlight>specific path you entered</highlight>)

- By default, it will make a zip file in the output path, but if you want unzipped files, pass <code>--unzipped</code> option.
    """
    def handle(self):
        try:
            config = Config(**self.io.input.options)
        except UnInitializedConfigException as e:
            self.line(error(e))
            sys.exit(1)
        if not config.target_id:
            self.line_error(error("Notion2Md requires either id or url."))
            sys.exit(1)
        exporter = BlockConvertor(self.io)
        #Directory Checking and Creating
        if not os.path.exists(config.tmp_path):
            os.makedirs(config.tmp_path)
        if not os.path.exists(config.output_path):
            os.makedirs(config.output_path)
        start_time = time.time()
        #Get actual blocks
        self.line("")
        indicator = Indicator(self.io,fmt="{message}{elapsed}s")
        with indicator.auto(status("Retrieving",""),status("Retrieved","children blocks in ")):
            blocks = get_children(config.target_id)
        #Write(Export) Markdown file
        self.line(status("Converting",f"{str(len(blocks))} blocks"))
        with open(os.path.join(config.tmp_path,config.file_name + '.md'),'w',encoding="utf-8") as output:
            output.write(exporter.convert(blocks))
        self.line(status("Converted",f"{str(len(blocks))} blocks to markdown {start_time - time.time():0.1f}s"))

        #Compress Output files into a zip file
        if not config.unzipped:
            zip_dir(os.path.join(config.output_path,config.file_name)+".zip",config.tmp_path)
            shutil.rmtree(config.tmp_path)
            extension = ".zip"
        else:
            extension = ".md"
        #Result and Time Check
        self.line(status("Exported", f'"{config.file_name}{extension}" in "./{config.path_name}/"'))
        self.line("")