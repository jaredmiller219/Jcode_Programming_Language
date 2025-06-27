import os
import re
from lexer import Lexer
from parser import Parser

class JournalGenerator:
    def __init__(self):
        self.functions = []

    def extract_functions_from_source(self, source_path):
        """Extract all function definitions from a JCode source file"""
        if not os.path.exists(source_path):
            return False, f"Source file not found: {source_path}"

        with open(source_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find all function definitions with their preceding comments
        pattern = r'((?:(?://|#).*\n)+|\s*(?:/\*(?:.|\n)*?\*/)\s*)?\s*(func\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\([^{]*(?:\)\s*\{|\)(?:\s*return\s+[^{]+)?))'
        matches = re.finditer(pattern, content, re.MULTILINE)

        for match in matches:
            comments = match.group(1) or ""
            signature = match.group(2).strip()

            # Clean up signature to remove opening brace if present
            signature = re.sub(r'\s*\{\s*$', '', signature)

            # Clean up comments
            comments = comments.strip()

            self.functions.append((signature, comments))

        return True, None

    def generate_journal(self, source_path, output_path):
        """Generate a function journal from a source file"""
        success, error = self.extract_functions_from_source(source_path)
        if not success:
            return False, error

        source_filename = os.path.basename(source_path)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"/**\n * Function Journal for {source_filename}\n * Generated automatically\n */\n\n")

            for signature, comments in self.functions:
                # Extract function name and parameters for documentation
                func_name_match = re.search(r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)', signature)
                func_name = func_name_match.group(1) if func_name_match else "unknown"

                # Extract parameters
                params_match = re.search(r'\(([^)]*)\)', signature)
                params = []
                if params_match:
                    params_str = params_match.group(1).strip()
                    if params_str:
                        # Split by commas, but handle type annotations
                        param_parts = []
                        current_part = ""
                        paren_level = 0

                        for char in params_str:
                            if char == ',' and paren_level == 0:
                                param_parts.append(current_part.strip())
                                current_part = ""
                            else:
                                current_part += char
                                if char == '(': paren_level += 1
                                elif char == ')': paren_level -= 1

                        if current_part.strip():
                            param_parts.append(current_part.strip())

                        for part in param_parts:
                            param_split = part.split(':') if ':' in part else part.split()
                            if len(param_split) >= 1:
                                param_name = param_split[-1].strip()
                                params.append(param_name)

                # Convert existing comments to XML style if possible
                xml_docs = []
                xml_docs.append("/// <summary>")

                if comments:
                    # Try to extract description from comments
                    if comments.startswith('/*'):
                        # Convert block comment
                        lines = comments.strip('/*').strip('*/').strip().split('\n')
                        for line in lines:
                            clean_line = line.strip().strip('*').strip()
                            if clean_line:
                                xml_docs.append(f"/// {clean_line}")
                    elif comments.startswith('//') or comments.startswith('#'):
                        # Convert line comments
                        lines = comments.split('\n')
                        for line in lines:
                            clean_line = line.strip().strip('//').strip('#').strip()
                            if clean_line:
                                xml_docs.append(f"/// {clean_line}")
                else:
                    # No existing comments, add placeholder
                    xml_docs.append(f"/// The {func_name} function")

                xml_docs.append("/// </summary>")

                # Add param documentation
                for param in params:
                    xml_docs.append(f"/// <param name=\"{param}\">Description of {param}</param>")

                # Add returns documentation if it looks like the function returns something
                if "return" in signature:
                    xml_docs.append("/// <returns>Description of return value</returns>")

                # Write the XML docs and signature
                f.write("\n".join(xml_docs) + "\n")
                f.write(f"{signature}\n\n")

        return True, None
