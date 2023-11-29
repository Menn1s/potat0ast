set working_dir (pwd | awk -F '/' '{print $(NF)}')
sed -i "s/(\\(.*.png\\)/(\\/posts\\/"$working_dir"\\/\\1/" *.md
