for i in 1024 512 256 128; do
  convert -resize "${i}x${i}" "base.png" "linux/${i}.png"
done

for i in 64 48 32 24 16; do
  convert -resize "${i}x${i}" "base.png" "base/${i}.png"
done

for i in 128 256; do
  convert -resize "${i}x${i}" "full.png" "full/icon_full_${i}.png"
done

convert -resize "1024x1024" "grey.png" "full/icon_grey_1024.png"

convert -resize "256x256" "set.png" "file/set.png"
convert -resize "256x256" "depot.png" "file/depot.png"

convert "linux/256.png" "Icon.ico"

convert "file/set.png" "file/set.ico"
convert "file/depot.png" "file/depot.ico"
