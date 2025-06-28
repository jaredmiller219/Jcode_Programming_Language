import os
import re
from lexer import Lexer
from parser import Parser

class JournalEntry:
    def __init__(self, signature, xml_docs):
        self.signature = signature
        self.xml_docs = xml_docs

    def __str__(self):
        return f"{self.xml_docs}\n{self.signature}"

class JournalParser:
    def __init__(self):
        self.entries = []

    def parse_journal_file(self, filepath):
        """Parse a journal file and extract function signatures with XML documentation"""
        if not os.path.exists(filepath):
            return False, f"Journal file not found: {filepath}"

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Split the file by function declarations with XML docs
        pattern = r'((?:///.*\n)+)?\s*(func\s+[^{]+)'
        matches = re.finditer(pattern, content, re.MULTILINE)

        for match in matches:
            xml_docs = match.group(1) or ""
            signature = match.group(2).strip()

            # Clean up XML docs
            xml_docs = xml_docs.strip()

            self.entries.append(JournalEntry(signature, xml_docs))

        return True, None

    def validate_against_source(self, source_path):
        """
        Validate that all function signatures in the journal
        match those in the source code
        """
        if not os.path.exists(source_path):
            return False, f"Source file not found: {source_path}"

        with open(source_path, 'r', encoding='utf-8') as f:
            source_content = f.read()

        # Extract function signatures from source
        source_pattern = r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\([^)]*\)(?:\s*return\s+[^{]+)?'
        source_signatures = re.findall(source_pattern, source_content)

        # Check if all journal signatures exist in source
        journal_signatures = [re.search(r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)', entry.signature).group(1)
                             for entry in self.entries]

        missing = []
        for sig in journal_signatures:
            if sig not in source_signatures:
                missing.append(sig)

        if missing:
            return False, f"Functions in journal but not in source: {', '.join(missing)}"

        return True, None

    def extract_xml_doc_info(self):
        """Extract structured information from XML documentation"""
        result = []

        for entry in self.entries:
            func_info = {
                'signature': entry.signature,
                'summary': '',
                'params': [],
                'type_params': [],
                'returns': '',
                'remarks': '',
                'examples': [],
                'exceptions': [],
                'see_also': [],
                'value': ''
            }

            # Extract function name
            name_match = re.search(r'func\s+([a-zA-Z_][a-zA-Z0-9_]*)', entry.signature)
            if name_match:
                func_info['name'] = name_match.group(1)

            # Extract summary
            summary_match = re.search(r'///\s*<summary>\s*\n((?:///.*\n)+?)///\s*</summary>|/\*\*\s*<summary>\s*\n((?:.*\n)+?)\s*</summary>', entry.xml_docs)
            if summary_match:
                summary_group = summary_match.group(1) or summary_match.group(2)
                summary_lines = summary_group.strip().split('\n')
                func_info['summary'] = '\n'.join([re.sub(r'^///\s*|\s*\*\s*', '', line).strip() for line in summary_lines])

            # Extract params
            param_matches = re.finditer(r'///\s*<param\s+name="([^"]+)">\s*(.*?)\s*</param>|/\*\*.*?<param\s+name="([^"]+)">\s*(.*?)\s*</param>', entry.xml_docs)
            for param_match in param_matches:
                param_name = param_match.group(1) or param_match.group(3)
                param_desc = param_match.group(2) or param_match.group(4)
                func_info['params'].append({
                    'name': param_name,
                    'description': param_desc
                })

            # Extract type params
            typeparam_matches = re.finditer(r'///\s*<typeparam\s+name="([^"]+)">\s*(.*?)\s*</typeparam>|/\*\*.*?<typeparam\s+name="([^"]+)">\s*(.*?)\s*</typeparam>', entry.xml_docs)
            for typeparam_match in typeparam_matches:
                typeparam_name = typeparam_match.group(1) or typeparam_match.group(3)
                typeparam_desc = typeparam_match.group(2) or typeparam_match.group(4)
                func_info['type_params'].append({
                    'name': typeparam_name,
                    'description': typeparam_desc
                })

            # Extract return info
            returns_match = re.search(r'///\s*<returns>\s*(.*?)\s*</returns>|/\*\*.*?<returns>\s*(.*?)\s*</returns>', entry.xml_docs)
            if returns_match:
                func_info['returns'] = returns_match.group(1) or returns_match.group(2)

            # Extract remarks
            remarks_match = re.search(r'///\s*<remarks>\s*\n((?:///.*\n)+?)///\s*</remarks>|/\*\*.*?<remarks>\s*\n((?:.*\n)+?)\s*</remarks>', entry.xml_docs)
            if remarks_match:
                remarks_group = remarks_match.group(1) or remarks_match.group(2)
                remarks_lines = remarks_group.strip().split('\n')
                func_info['remarks'] = '\n'.join([re.sub(r'^///\s*|\s*\*\s*', '', line).strip() for line in remarks_lines])

            # Extract examples
            example_matches = re.finditer(r'///\s*<example>\s*\n((?:///.*\n)+?)///\s*</example>|/\*\*.*?<example>\s*\n((?:.*\n)+?)\s*</example>', entry.xml_docs)
            for example_match in example_matches:
                example_group = example_match.group(1) or example_match.group(2)
                example_lines = example_group.strip().split('\n')
                func_info['examples'].append('\n'.join([re.sub(r'^///\s*|\s*\*\s*', '', line).strip() for line in example_lines]))

            # Extract exceptions
            exception_matches = re.finditer(r'///\s*<exception\s+cref="([^"]+)">\s*(.*?)\s*</exception>|/\*\*.*?<exception\s+cref="([^"]+)">\s*(.*?)\s*</exception>', entry.xml_docs)
            for exception_match in exception_matches:
                exception_type = exception_match.group(1) or exception_match.group(3)
                exception_desc = exception_match.group(2) or exception_match.group(4)
                func_info['exceptions'].append({
                    'type': exception_type,
                    'description': exception_desc
                })

            # Extract see also
            seealso_matches = re.finditer(r'///\s*<seealso\s+cref="([^"]+)"\s*/>|/\*\*.*?<seealso\s+cref="([^"]+)"\s*/>', entry.xml_docs)
            for seealso_match in seealso_matches:
                seealso_cref = seealso_match.group(1) or seealso_match.group(2)
                func_info['see_also'].append(seealso_cref)

            result.append(func_info)

        return result
