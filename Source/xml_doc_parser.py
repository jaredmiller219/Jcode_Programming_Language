import re
from typing import Dict, List, Optional, Any

class XmlDocComment:
    """Represents a parsed XML documentation comment"""

    def __init__(self):
        self.summary = ""
        self.params = {}  # name -> description
        self.type_params = {}  # name -> description
        self.returns = ""
        self.remarks = ""
        self.examples = []
        self.exceptions = {}  # type -> description
        self.see_also = []
        self.value = ""
        self.custom_tags = {}  # tag name -> content

    @staticmethod
    def parse(comment_text: str) -> 'XmlDocComment':
        """Parse XML documentation from a comment string"""
        doc = XmlDocComment()

        # Clean up the comment text
        lines = comment_text.split('\n')
        cleaned_lines = []
        for line in lines:
            # Remove leading /// or /** and trailing */
            line = re.sub(r'^///\s*', '', line)
            line = re.sub(r'^/\*\*\s*', '', line)
            line = re.sub(r'\s*\*/$', '', line)
            line = re.sub(r'^\s*\*\s*', '', line)  # Remove * from each line in block comments
            cleaned_lines.append(line)

        comment_text = '\n'.join(cleaned_lines)

        # Extract summary
        summary_match = re.search(r'<summary>(.*?)</summary>', comment_text, re.DOTALL)
        if summary_match:
            doc.summary = summary_match.group(1).strip()

        # Extract params
        param_matches = re.finditer(r'<param\s+name="([^"]+)">(.*?)</param>', comment_text, re.DOTALL)
        for match in param_matches:
            doc.params[match.group(1)] = match.group(2).strip()

        # Extract type params
        typeparam_matches = re.finditer(r'<typeparam\s+name="([^"]+)">(.*?)</typeparam>', comment_text, re.DOTALL)
        for match in typeparam_matches:
            doc.type_params[match.group(1)] = match.group(2).strip()

        # Extract returns
        returns_match = re.search(r'<returns>(.*?)</returns>', comment_text, re.DOTALL)
        if returns_match:
            doc.returns = returns_match.group(1).strip()

        # Extract remarks
        remarks_match = re.search(r'<remarks>(.*?)</remarks>', comment_text, re.DOTALL)
        if remarks_match:
            doc.remarks = remarks_match.group(1).strip()

        # Extract examples
        example_matches = re.finditer(r'<example>(.*?)</example>', comment_text, re.DOTALL)
        for match in example_matches:
            doc.examples.append(match.group(1).strip())

        # Extract exceptions
        exception_matches = re.finditer(r'<exception\s+cref="([^"]+)">(.*?)</exception>', comment_text, re.DOTALL)
        for match in exception_matches:
            doc.exceptions[match.group(1)] = match.group(2).strip()

        # Extract see also
        seealso_matches = re.finditer(r'<seealso\s+cref="([^"]+)"\s*/>', comment_text, re.DOTALL)
        for match in seealso_matches:
            doc.see_also.append(match.group(1))

        # Extract value
        value_match = re.search(r'<value>(.*?)</value>', comment_text, re.DOTALL)
        if value_match:
            doc.value = value_match.group(1).strip()

        return doc

    def to_string(self) -> str:
        """Convert the XML documentation to a string"""
        lines = []

        if self.summary:
            lines.append("/// <summary>")
            for summary_line in self.summary.split('\n'):
                lines.append(f"/// {summary_line}")
            lines.append("/// </summary>")

        for param_name, param_desc in self.params.items():
            lines.append(f'/// <param name="{param_name}">{param_desc}</param>')

        for typeparam_name, typeparam_desc in self.type_params.items():
            lines.append(f'/// <typeparam name="{typeparam_name}">{typeparam_desc}</typeparam>')

        if self.returns:
            lines.append(f"/// <returns>{self.returns}</returns>")

        if self.remarks:
            lines.append("/// <remarks>")
            for remark_line in self.remarks.split('\n'):
                lines.append(f"/// {remark_line}")
            lines.append("/// </remarks>")

        for example in self.examples:
            lines.append("/// <example>")
            for example_line in example.split('\n'):
                lines.append(f"/// {example_line}")
            lines.append("/// </example>")

        for exception_type, exception_desc in self.exceptions.items():
            lines.append(f'/// <exception cref="{exception_type}">{exception_desc}</exception>')

        for see_also in self.see_also:
            lines.append(f'/// <seealso cref="{see_also}"/>')

        if self.value:
            lines.append(f"/// <value>{self.value}</value>")

        return '\n'.join(lines)
