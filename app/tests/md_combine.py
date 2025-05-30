from pathlib import Path

# Set the input directory (containing .md files)
input_dir = Path('app/rag_data/37signals_md')  
output_file = input_dir.parent / 'combined.md'  # One directory up

# Collect and sort all .md files in the input directory
md_files = sorted(input_dir.glob('*.md'))

# Combine contents
with open(output_file, 'w', encoding='utf-8') as outfile:
    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as infile:
            outfile.write(f"# {md_file.stem}\n\n")  # Optional: filename as section title
            outfile.write(infile.read())
            outfile.write('\n\n')  # Add spacing between files

print(f"✅ Combined markdown saved to: {output_file}")
