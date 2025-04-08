#!/bin/bash

TODAY=$(date +%Y%m%d)
# Step 1: Create an empty file dadabot.full to avoid self-appending.
> dadabot.full

# Step 2: Append files: Process all .py and .json files (excluding "dadabot.full" and the venv folder).
find . -path './venv' -prune -o -type f \( -name "*.py" -o -name "*.json" \) ! -name "dadabot_full_${TODAY}.py" -print0 | while IFS= read -r -d '' file; do
    # Print to console which file is being processed.
    echo "Processing: $file"
    
    # Determine the directory and file name. Remove leading "./" from directory if desired.
    dir=$(dirname "$file")
    name=$(basename "$file")
    
    # Insert opening lines before the header.
    echo "#####" >> dadabot.full
    echo "" >> dadabot.full
    # Insert the header with the file's directory and name.
    echo "# ${dir}/${name}" >> dadabot.full
    # Append the content of the file.
    cat "$file" >> dadabot.full
    # Add another blank line after the file content for separation.
    echo "" >> dadabot.full
done

# Step 3: Rename dadabot.full to include today's date in the format YYYYMMDD.
mv dadabot.full "dadabot_full_${TODAY}.py"

echo "Created dadabot_full_${TODAY}.py successfully!"