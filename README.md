# tools
- csdn2markdown  
通过抓包分析，获取CSDN博客的Markdown格式。批量下载markdown格式的个人博客，从而完成博客迁移。

- scholar helper  
输入论文题目，获取论文引用格式  
主要使用`requests`请求Google学术，使用`Beautiful Soup`解析
搭建在aws，可访问[scholar.khay.site](http://scholar.khay.site)使用  
TODO：  
    + 返回多个候选结果，可以直接在解析使用 `find_all()`；需要更改合适的ui
    + 返回bibtex引用格式，使用上述方法请求存在问题，待解决