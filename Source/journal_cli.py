import sys
import os
from journal_generator import JournalGenerator
from journal_parser import JournalParser

def print_usage():
    print("JCode Function Journal Tool")
    print("Usage:")
    print("  python journal_cli.py generate <source_file> <output_journal>")
    print("  python journal_cli.py validate <source_file> <journal_file>")
    print("  python journal_cli.py extract-docs <journal_file>")
    print("\nExamples:")
    print("  python journal_cli.py generate code/example.jcode code/example.journal")
    print("  python journal_cli.py validate code/example.jcode code/example.journal")
    print("  python journal_cli.py extract-docs code/example.journal")

def main():
    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command == "generate" and len(sys.argv) == 4:
        source_file = sys.argv[2]
        output_file = sys.argv[3]

        generator = JournalGenerator()
        success, error = generator.generate_journal(source_file, output_file)

        if not success:
            print(f"Error: {error}")
            return

        print(f"Journal successfully generated: {output_file}")

    elif command == "validate" and len(sys.argv) == 4:
        source_file = sys.argv[2]
        journal_file = sys.argv[3]

        parser = JournalParser()
        success, error = parser.parse_journal_file(journal_file)

        if not success:
            print(f"Error parsing journal: {error}")
            return

        success, error = parser.validate_against_source(source_file)

        if not success:
            print(f"Validation failed: {error}")
            return

        print("Journal validation successful!")

    elif command == "extract-docs" and len(sys.argv) == 3:
        journal_file = sys.argv[2]

        parser = JournalParser()
        success, error = parser.parse_journal_file(journal_file)

        if not success:
            print(f"Error parsing journal: {error}")
            return

        docs_info = parser.extract_xml_doc_info()

        # Print structured documentation info
        for func in docs_info:
            print(f"Function: {func.get('name', 'Unknown')}")
            print(f"Signature: {func['signature']}")
            print(f"Summary: {func['summary']}")

            if func['params']:
                print("Parameters:")
                for param in func['params']:
                    print(f"  - {param['name']}: {param['description']}")

            if func['returns']:
                print(f"Returns: {func['returns']}")

            print()

    else:
        print_usage()

if __name__ == "__main__":
    main()
