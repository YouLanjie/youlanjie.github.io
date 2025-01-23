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

;;(setq org-html-preamble
;;"<header>
;;     <a href=\"/\">
;;       <img src=\"/img/icon.jpg\" height=\"35\">
;;     </a>
;;     <a href=\"/\">  Home  </a>
;;     <a href=\"/src/post.html\">  Blog  </a>
;;     <a href=\"/src/post2.html\">  TimeLine  </a>
;;     <a href=\"/about.html\">  About  </a>
;;     <div class=\"clearfix\"></div>
;;   </header>")

(setq-default org-src-fontify-natively t
;; 设置org高亮代码块
;; Non-nil means interpret "_" and "^" for display.
	      org-export-with-sub-superscripts '{}
	      ;; 适用于导出
	      org-use-sub-superscripts '{}
	      ;; 适用于org-mode中渲染

	      ;; Org转PDF渲染流程
	      ;; org-latex-pdf-process '("xelatex %f"
	      ;; 			      "rm -fr %b.out %b.log %b.brf %b.bbl auto"
	      ;; 			      )
	      )


(org-html-export-to-html)
(kill-emacs)
