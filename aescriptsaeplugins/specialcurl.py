#!/usr/local/autopkg/python

import os
import shutil
import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["specialcurl"]


class specialcurl(Processor):
    """Unpacks a package payload."""

    input_variables = {
        "Referer": {
            "required": True,
            "description": (
                "The referer url"
            ),
        },
        "filename": {"required": True, "description": "Destination directory."},
        "url": {
            "required": True,
            "description": (
                "URL to download from"
            ),
        },
    }
    output_variables = {}
    description = __doc__
    
    def download(self):
        try:
            ccmd = [
                "/usr/bin/curl",
                "-L",
                "-H",
                self.env["Referer"],
                self.env["url"],
                "-o",
                self.env["filename"]
            ]
            proc = subprocess.Popen(
                ccmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            (_, err_out) = proc.communicate()
        except OSError as err:
            error = (
                f"download failed with error code {err.errno}: {err.strerror}"
            )
        if proc.returncode != 0:
            error = (
                f"download of {self.env['url']} with curl failed: "
                f"{err_out}"
            )
        self.output("Downloaded sucessfully")

    def main(self):
        self.download()


if __name__ == "__main__":
    PROCESSOR = specialcurl()
    PROCESSOR.execute_shell()
