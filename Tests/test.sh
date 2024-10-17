#!/bin/bash


rm -rf out/
mkdir out/

exit_code=0
iter=0

# Read the file line by line
while IFS= read -r url ; do
    iter=$(($iter+1))
    echo "$url" > "URLs/$iter.txt"


    # Give it more try. Pytube is not quite responsive. Might be prone to errors
    for i in $(seq 1 10) ; do
        python3 ../html_md_youtube_card.py "$url" 2> /dev/null 1> "out/$iter.md"
        if [[ $? == 0 ]] ; then
            
            nr_diff_lines=$(diff out/$iter.md ref/$iter.md > /dev/null | wc -l)

            if [[ $nr_diff_lines != 0 ]] ; then
                exit_code=255
                echo "[ERROR] For URLs/$iter.txt, the command following command does not work:"
                echo "$ python3 ../html_md_youtube_card.py " "$url"
                diff "out/$iter.md" "ref/$iter.md"
                echo ''
                break
            else
                echo "[OK] URLs/$iter.txt"
            fi
            
            # If the script did not return an error code, exit the for
            break
        fi
    done
done < URLs.txt


echo ''

if [[ $exit_code == 0 ]] ; then
    echo "Great! All tests PASSED"
else
    echo "Some tests FAILED :(("
fi

exit $exit_code
