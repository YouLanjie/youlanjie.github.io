;;; fastsetup.el --- Emacs快速启动配置               -*- lexical-binding: t; -*-
;;; Code:

;; 添加仓库
(require 'package)
(package-initialize)

(setq-default make-backup-files nil
	      ;; 关闭文件自动备份
	      auto-save-default nil
	      ;; 关闭自动保存
	      )

;; 主题
(require 'monokai-theme)
(load-theme 'monokai t)

;; Org html代码高亮
(require 'htmlize)

(setq org-html-preamble
"<header>
     <a href=\"/\">
       <img src=\"/img/icon.jpg\" height=\"35\">
     </a>
     <a href=\"/\">  Home  </a>
     <a href=\"/src/post.html\">  Blog  </a>
     <a href=\"/src/post2.html\">  TimeLine  </a>
     <a href=\"/about.html\">  About  </a>
     <div class=\"clearfix\"></div>
   </header>")


(org-html-export-to-html)
(kill-emacs)
