for file in *.fastresume; do
    if [[ -f "$file" ]]; then
		# Due to the stupid path splittor, we need execute it twice.
        sed -b -i 's|H:\\Anime|G:\\Anime|g' "$file"
        sed -b -i 's|H:/Anime|G:/Anime|g' "$file"
        sed -b -i 's|H:\\TwoDimensionalWorldPhoto|G:\\TwoDimensionalWorldPhoto|g' "$file"
        sed -b -i 's|H:/TwoDimensionalWorldPhoto|G:/TwoDimensionalWorldPhoto|g' "$file"
    fi
done