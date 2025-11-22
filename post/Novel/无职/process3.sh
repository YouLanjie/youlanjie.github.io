#!/usr/bin/zsh

ls -1 0*.org|while read line;do
	title=${line%.org}
	title=${title#0*_}
	echo "==> $title"
	sed -i "s/^\\* $title\( web版\)\?/**/" "$line"
	sed -i "/^\\** 插图/d" "$line"
	sed -i "2a* $title" "$line"
done
