set -x

day=$(date "+%-d")
year=$(date "+%Y")
puzzle_url="https://adventofcode.com/${year}/day/${day}"
input_url="https://adventofcode.com/${year}/day/${day}/input"
input_file="day${day}_input.txt"
script_file="day${day}.py"
browser="firefox"
editor="vim"

# Open pages
if [ -z "${browser}" ]; then
    echo "No browser set - ignored."
else
    "${browser}" "${puzzle_url}"
    "${browser}"  "${input_url}"
fi

# Optional: read cookie config file - setting AOC_SESSION_COOKIE env variable
# See template file aoc_cookie_session.sh for instructions
source ~/aoc_cookie_session.sh 2> /dev/null

# Get input file
if [ -f "${input_file}" ]; then
    echo "Input file ${input_file} already exists - ignored."
elif [ -z "${AOC_SESSION_COOKIE}" ]; then
    # Create empty input file
    touch "${input_file}"
else
    echo "Cookie session AOC_SESSION_COOKIE used to get input file."
    # Get input file
    curl "${input_url}" -H "cookie: session=${AOC_SESSION_COOKIE}" -o "${input_file}"
fi

# Create script file based on template
if [ -f "${script_file}" ]; then
    echo "Script file ${script_file} already exists - ignored."
else
    cp ./day_template.py "${script_file}"
    sed -i "s/DAYNUMBER/${day}/g" "${script_file}"
fi

# Add line to README.md
echo -e "\n${puzzle_url} : 0/2" >> README.md

# Change number of days in all_days.py
sed -i "s/^\(nb_days = \).*/\1${day}/g" all_days.py

# Add everything and commit - not performed anymore
# git add "${input_file}" "${script_file}" README.md
# git commit -m "Day ${day} - part 1"

# Open relevant files to start solving the problem
if [ -z "${editor}" ]; then
    echo "No editor set - ignored."
else
    "${editor}" "${script_file}" "${input_file}"
fi
