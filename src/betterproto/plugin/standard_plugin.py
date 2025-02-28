"""
Protocol Buffers code generator plugin.
This module provides a simplified plugin for protocol buffer code generation
that uses standard Python types (enum.IntEnum and dataclasses) without the
additional serialization, type checking, and other behaviors.
"""

import importlib.resources
import json
import os
import sys
from typing import (
    Dict,
    List,
    Optional,
    Set,
    TextIO,
    Tuple,
)

import jinja2

from betterproto.plugin.compiler import Compiler
from betterproto.plugin.parser import Parser


def _get_template_env() -> jinja2.Environment:
    """Get the Jinja environment with our templates."""
    template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
    )
    return env


def _get_header_template() -> str:
    """Get the content of the header template."""
    env = _get_template_env()
    return env.get_template("standard_header.py.j2").render()


def _get_code_template() -> str:
    """Get the content of the code template."""
    env = _get_template_env()
    return env.get_template("standard_template.py.j2").render()


def generate_code(
    proto_file: str,
    output_file: str,
    include_imports: bool = False,
    package_override: Optional[str] = None,
    python_module_override: Optional[str] = None,
) -> None:
    """Generate Python code from proto file."""
    
    parser = Parser()
    compiler = Compiler()
    
    with open(proto_file, "rb") as f:
        proto_content = f.read()
    
    parsed = parser.parse_proto(proto_content)
    compiled = compiler.compile_parsed(parsed, include_imports=include_imports)
    
    env = _get_template_env()
    header_template = env.get_template("standard_header.py.j2")
    code_template = env.get_template("standard_template.py.j2")
    
    with open(output_file, "w") as f:
        f.write(header_template.render(output_file=compiled))
        f.write("\n\n")
        f.write(code_template.render(output_file=compiled))


def main() -> None:
    """Main entry point for the plugin."""
    # Read request from stdin
    data = sys.stdin.buffer.read()
    
    # Parse request
    request = json.loads(data)
    
    # Generate code for each file
    response = {"file": []}
    
    for proto_file in request.get("file", []):
        proto_name = proto_file.get("name", "")
        if not proto_name:
            continue
        
        # Generate Python code
        output_file = proto_name.replace(".proto", "_pb.py")
        
        # Parse, compile and generate code
        parser = Parser()
        compiler = Compiler()
        
        parsed = parser.parse_proto(proto_file.get("content", "").encode())
        compiled = compiler.compile_parsed(parsed)
        
        env = _get_template_env()
        header_template = env.get_template("standard_header.py.j2")
        code_template = env.get_template("standard_template.py.j2")
        
        content = header_template.render(output_file=compiled)
        content += "\n\n"
        content += code_template.render(output_file=compiled)
        
        response["file"].append({
            "name": output_file,
            "content": content,
        })
    
    # Write response to stdout
    sys.stdout.buffer.write(json.dumps(response).encode())


if __name__ == "__main__":
    main()