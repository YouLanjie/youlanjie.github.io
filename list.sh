#!/usr/bin/zsh

#================================================================
#   Copyright (C) 2023 YouLanjie
#
#   文件名称：list.sh
#   创 建 者：youlanjie
#   创建日期：2023年05月07日
#   描    述：构建首页
#
#================================================================

cd /mnt/UserData/Code/youlanjie.github.io

out=$(find post -type f -name "*.org"|sed "s/^\(.*\)/(head -n 10 '\1' |grep 'date') \&\& echo '\1'/"|zsh)
out2=$(echo $out|sed -n "N;s/\n/ /;s/^#+date:[ ]*//p")
out3=$(echo $out2|sort -r)
echo $out3|sed "s/^/- /;s/\(^- [^ ]* [^ ]*\) post\/\(.*\)\.org/\1 [[..\/post\/\2\.html][\2]]/" > src/post2.org

# 导出
emacs index.org --eval "(progn (org-html-export-to-html) (kill-emacs))"
