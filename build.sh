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

app_name="${0##*/}"

# Show an INFO message
# $1: message string
_msg_info() {
    local _msg="${1}"
    [[ "${quiet}" == "y" ]] || printf '[%s] INFO: %s\n' "${app_name}" "${_msg}"
}

# Show a WARNING message
# $1: message string
_msg_warning() {
    local _msg="${1}"
    printf '[%s] WARNING: %s\n' "${app_name}" "${_msg}" >&2
}

# Show an ERROR message then exit with status
# $1: message string
# $2: exit code number (with 0 does not exit)
_msg_error() {
    local _msg="${1}"
    local _error=${2}
    printf '[%s] ERROR: %s\n' "${app_name}" "${_msg}" >&2
    if (( _error > 0 )); then
        exit "${_error}"
    fi
}

usage() {
	usagetext="\
usage: build.sh [options]
  options:
     -m 创建博客到public目录下（不建议使用）
     -b 构建博客列表与首页
     -u 导出未更新的org为html页面
     -t 导出时不检查文件的新旧
     -n 不更新文件内容
     -h 帮助信息"
	echo $usagetext
	exit $1
}

mk_public() {
	_msg_info "检测是否存在public文件夹..."
	if [[ ! -d public ]] {
		if [[ -f public ]] {
			_msg_error "文件\`public\`已存在且非文件夹" 1
		}
		_msg_warning "文件夹\`public\`不存在"
		_msg_info "将创建public文件夹"
		if [[ ! -d public ]] {
			_msg_error "无法创建" 1
		}
	} else {
		_msg_info "结果为真，将进行构建操作"
	}
	_msg_info "清除public目录"
	find public |grep -v "\.git"|sed -n "s/public\//.\/public\//p"|sort -r|sed "s/^/rm -d '/"|sed "s/$/'/"|zsh
	_msg_info "创建目录树"
	find post -type d|sed -n "s/post\//.\/public\/post\//p"|sed "s/^/mkdir -p '/"|sed "s/$/'/"|zsh
	_msg_info "复制文件"
	find post -type f|grep -v "\.org"|sed "s/^/cp -r '/"|sed "s/ 'post\/\(.*\)$/ 'post\/\1' 'public\/post\/\1'/"|zsh
	_msg_info "复制首页"
	cp index.html public/
	_msg_info "复制404页"
	cp 404.html public/
	_msg_info "复制主题与图片"
	cp -r theme/ public/
	cp -r img/ public/
	_msg_info "Done!"
}

update_file() {
	emacs -Q -nw ./src/fastsetup.el "$1" --eval "(eval-buffer \"fastsetup.el\")"
	out=$(echo $1|sed "s/\\.org$/.html/")
	section1="^<style>"
	section2="^<\\/style>"
	sed -i "/$section1/,/$section2/{/$section1/!{/$section2/!d}}" "$out"
	sed -i "/$section1/,/$section2/d" "$out"
}

check_time() {
	if [[ (! -f $2) || ($1 -nt $2) || $flag_no_time == "true" ]] {
		_msg_info "Export '$1' ..."
		if [[ $flag_no_exp == "false" ]] {
			update_file $1
		}
		if [[ $flag_no_exp == "true" ]] {
			echo "" >> $2
		}
		return 0
	}
	return -1
}

update() {
	#update_file index.org
	#echo $file_list
	for name (post/**/*.org) {
		out=$(echo $name|sed "s/\\.org$/.html/")
		check_time "$name" "$out"
	}
}

build() {
	_msg_info "清空源文件"
	echo "#+TITLE: TimeLine\n#+setupfile: ../setup.setup" > src/timeline.org
	_msg_info "构建列表中"
	_msg_info "获取文件头并处理中"
	file_list=(post/**/*.org)
	line_max=$(echo $file_list|wc -l)
	for name ($file_list) {
		title=$(head -n 5 $name |grep -i '#+title: ')
		declare -l title="$title"
		title=$(echo $title|sed 's/^#+title:[ ]*//')

		date=$(head -n 5 $name |grep -i '#+date: ')
		declare -l date="$date"
		date=$(echo $date|sed 's/^#+date:[ ]*//;s/<\(.*\)>/\1/;s/\([^ ]*\) [一|二|三|四|五|六|日] /\1 /')
		if [[ $date == "" ]] {
			continue
		}

		desc=$(head -n 5 $name |grep -i '#+description: ')
		name=$(echo $name|sed 's/^/..\//')
		if [[ $desc != "" ]] {
			declare -l desc="$desc"
			desc=$(echo $desc|sed 's/^#+description:[ ]*//')
			printf '- /%s/ [[%s][%s]]\\\\\\\\\\n  %s\n' "$date" "$name" "$title" "$desc" >> src/timeline.org
		} else {
			printf "- /%s/ [[%s][%s]]\n" "$date" "$name" "$title" >> src/timeline.org
		}
	}
	list=$(cat src/timeline.org|sort -r)
	echo $list > src/timeline.org
	_msg_info "列表输出完成"
	_msg_info "导出子页面中..."
	tmp="true"
	check_time "404.org" "404.html"
	check_time "about.org" "about.html"
	check_time "src/post.org" "src/post.html" || tmp="false"
	update_file src/timeline.org
	if [[ $tmp == "true" ]] {
		_msg_info "导出首页中..."
		# emacs index.org -nw --eval "(progn (org-html-export-to-html) (kill-emacs))"
		update_file index.org
	}
	_msg_info "Done!"
}

flag_no_exp="false"
flag_no_time="false"

while {getopts 'mbnuth?' arg} {
	case $arg {
		m) mk_public ;exit 0 ;;
		b) build ;exit 0 ;;
		u) update ;exit 0 ;;
		t) flag_no_time="true" ;;
		n) flag_no_exp="true" ;;
		h|?) usage 0;;
		*) usage 1;;
	}
}

if [[ $@ == "" ]] {
	_msg_error "No options!"
	usage 1
} else {
	_msg_error "Bad options!"
	usage 1
}

