#!/usr/bin/zsh

#================================================================
#   Copyright (C) 2023 YouLanjie
#
#   文件名称：build.sh
#   创 建 者：youlanjie
#   创建日期：2023年04月02日
#   描    述：构建博客
#
#================================================================

cd /mnt/UserData/Code/youlanjie.github.io

find public |grep -v "\.git"|sed -n "s/public\//.\/public\//p"|sort -r|sed "s/^/rm -d '/"|sed "s/$/'/"|zsh

find post -type d|sed -n "s/post\//.\/public\/post\//p"|sed "s/^/mkdir -p '/"|sed "s/$/'/"|zsh

find post -type f|grep -v "\.org"|sed "s/^/cp -r '/"|sed "s/ 'post\/\(.*\)$/ 'post\/\1' 'public\/post\/\1'/"|zsh

cp index.html public/
cp 404.html public/

cp -r theme/ public/

cp -r img/ public/

