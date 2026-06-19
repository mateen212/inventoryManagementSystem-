#!/usr/bin/env python3
import os
import re
from pathlib import Path

MODELS_DIR = Path("app/models")

# Default length for columns where we don't have a custom mapping
DEFAULT_LENGTH = 255

# Custom lengths for specific column names (optional)
CUSTOM_LENGTHS = {
    "name": 100,
    "sku": 50,
    "barcode": 50,
    "email": 100,
    "username": 50,
    "phone": 20,
    "order_number": 50,
    "invoice_number": 50,
    "ip_address": 50,
    "action": 100,
    "title": 200,
    "filename": 255,
    "path": 500,
    "image": 255,
    "pdf_path": 255,
    "full_name": 100,
    "contact_person": 100,
    "hashed_password": 255,
    "location": 255,
    "shipping_address": 255,
    "address": 255,
}

def fix_file(filepath):
    with open(filepath, "r") as f:
        content = f.read()

    # Find all Column(String(...)) occurrences and add a length if missing.
    # Also remove any invalid COLLATE clauses.
    def replacer(match):
        full = match.group(0)
        # Extract the content inside String(...)
        # Pattern: Column( ... String( ... ) ... )
        # We'll capture the inside of String() and check if it has a comma (length already present)
        # but we need to handle nested parentheses? Not expected.

        # We'll use a simpler approach: find the part between String( and the matching )
        # But we can use a regex that matches Column(String( ... ) ) with the first closing paren.
        # We'll use a function to process.

        # Extract the column name from the line (if possible) to apply custom length.
        # We'll look for something like name = Column...
        line = match.string
        # But we don't have the line in the match object.
        # We can use the full match.

        # We'll just add DEFAULT_LENGTH if no length specified.
        # Check if there is a comma after String( before the closing )
        # We'll use a simple condition: if the content inside String() contains a comma and a number, assume length is present.
        # Otherwise, add length.

        # We'll manually find the inner content.
        start = full.find("String(")
        if start == -1:
            return full
        # Find the matching closing ) after String(
        # We'll count parentheses.
        inner_start = start + 7  # len("String(")
        paren_count = 1
        i = inner_start
        while i < len(full) and paren_count > 0:
            if full[i] == '(':
                paren_count += 1
            elif full[i] == ')':
                paren_count -= 1
            i += 1
        inner = full[inner_start:i-1]  # content inside String(...)
        # Check if inner already has a length (i.e., contains a comma and a digit)
        # Also check for COLLATE and remove it.
        # If inner contains "COLLATE", we strip that part.
        inner_clean = re.sub(r'\s*COLLATE\s+\S+', '', inner)  # remove COLLATE clause
        # Now check if there is a comma and a number.
        if re.search(r',\s*\d+', inner_clean):
            # has length, keep as is but remove COLLATE if any
            new_inner = inner_clean
        else:
            # no length, add default
            # Determine length based on column name if possible.
            col_name = None
            # Try to find the column name from the line (e.g., name = Column(...))
            # We can use the line from the file, but we don't have it here.
            # Instead, we can look for a pattern like Column(String(...), maybe preceded by a variable name.
            # We'll just use default.
            length = DEFAULT_LENGTH
            # If we can detect the column name, we could use custom length, but we'll skip for simplicity.
            new_inner = f"{length}, {inner_clean}" if inner_clean.strip() else str(length)
        # Reconstruct the full Column(String(...)) with new inner.
        new_full = full[:start] + "String(" + new_inner + ")" + full[i:]
        return new_full

    # Use re.sub to replace each Column(String(...))
    # We'll use a pattern that matches Column(String(...)) but we need to match nested parentheses.
    # A simple regex cannot handle nested parentheses, but our models are simple.
    # We'll use a function that finds all occurrences by scanning.
    # Alternatively, we can use a line-by-line approach.

    # Let's do line-by-line replacement.
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        # Check if line contains Column(String(
        if "Column(String(" in line:
            # We'll attempt to replace only the first occurrence per line (usually one).
            # Use the replacer function.
            # Since we can't pass the line easily, we'll use a regex that matches Column(String(...)) with nesting.
            # We'll use a regex with re.DOTALL and non-greedy.
            # Pattern: Column\(\s*String\(([^)]*)\)\s*\)
            # This assumes no nested parentheses inside String().
            # It will break if there is a function call inside String().
            # For our models, it's simple: String(255, ...) or String().
            # So we can use:
            def replace_string(m):
                before = m.group(0)
                inner = m.group(1)
                # Clean inner: remove COLLATE
                inner_clean = re.sub(r'\s*COLLATE\s+\S+', '', inner)
                # Check if length already present
                if re.search(r',\s*\d+', inner_clean):
                    new_inner = inner_clean
                else:
                    # Determine length from column name? Not easy here.
                    length = DEFAULT_LENGTH
                    if inner_clean.strip():
                        new_inner = f"{length}, {inner_clean}"
                    else:
                        new_inner = str(length)
                return f"Column(String({new_inner}))"
            new_line = re.sub(r'Column\(\s*String\(\s*([^)]*)\s*\)\s*\)', replace_string, line)
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    new_content = "\n".join(new_lines)
    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        return True
    return False

def main():
    if not MODELS_DIR.exists():
        print(f"Error: {MODELS_DIR} not found.")
        return

    for filepath in MODELS_DIR.glob("*.py"):
        if filepath.name == "__init__.py":
            continue
        fix_file(filepath)

    print("All String columns have been given a default length of 255.")
    print("You may want to adjust lengths manually for specific columns.")

if __name__ == "__main__":
    main()