#!/usr/bin/env python3
# coding: utf-8


import os
import shutil
from pprint import pprint
import markdown2 as md2
from collections import OrderedDict


class CreatorHtml():
    header = '''
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="http://localhost:8888/static/github-markdown.css">
    <style type="text/css">
    .markdown-body {
    box-sizing: border-box;
    min-width: 200px;
    max-width: 980px;
    margin: 0 auto;
    padding: 45px;
    font-size: 0.8em;
    }

    @media (max-width: 767px) {
    .markdown-body {
    padding: 15px;
    }
    }
    </style>
    </head>
    '''
    def __init__(self, src_dir, dst_dir):
        '''
        param:
            src_dir: 遍历原始 markdown 文件的目录
            dst_dir: 创建 html 页面的目录
            '''

        self._src_dir = src_dir
        self._dst_dir = dst_dir
        self._dirs = OrderedDict()
        print(self._src_dir)
        print(self._dst_dir)

    def clean(self):
        for filename in os.listdir(self._dst_dir):
            clean_file = '{}/{}'.format(self._dst_dir, filename)
            if os.path.isdir(clean_file):
                shutil.rmtree(clean_file)
            else:
                os.remove(clean_file)


    def create(self):
        # 检查目录
        if not os.path.exists(self._src_dir):
            print('src directory err: {}'.format(self._src_dir))
            return False

        if not os.path.exists(self._dst_dir):
            print('dst directory err: {}'.format(self._dst_dir))
            return False

        all_dirs = os.walk(self._src_dir)
        start_pos = len(self._src_dir)
        for (dirpath, dirnames, filenames) in all_dirs:
            filenames = [filename for filename in filenames
                         if filename.endswith('.md')]
            if not filenames:
                continue

            # 保留相对路径作为 key
            dirpath = dirpath[start_pos:]
            self._dirs[dirpath] = filenames

        # 遍历原始目录
        pprint(self._dirs)

        # 循环创建文件
        for (dirname, filenames) in self._dirs.items():
            for filename in filenames:
                src_fpath = '{}/{}/{}'.format(self._src_dir, dirname, filename)
                html = self._create_html(src_fpath)
                # print(html)

                filename = '{}.html'.format(filename[:-3])
                dst_fpath = '{}/{}/{}'.format(self._dst_dir, dirname, filename)
                dst_dirpath = os.path.dirname(dst_fpath)

                # 目录不存在则创建
                if not os.path.exists(dst_dirpath):
                    os.makedirs(os.path.dirname(dst_fpath))

                with open(dst_fpath, 'w') as out_html:
                    out_html.write(html)

        # 创建索引文件
        self._create_index('index.html')

    def _create_html(self, filename):
        '''转换markdown文件到html'''

        with open(filename) as f:
            text = f.read()
            html = md2.markdown(text, extras=['tables', 'codelite'])
            html = '{}<body class="markdown-body">{}</body>'.format(self.header,
                                                                    html)

        return html

    def _create_index(self, index_file):
        '''
        创建索引页面
        '''
        all_content = []

        paragraph = '<h1>{}</h1>'.format('go，python 开发文档')
        all_content.append(paragraph)
        all_content.append('<ul>')
        item = '<li><a href="http://localhost:5001">python</a></li>'
        all_content.append(item)
        item = '<li><a href="http://localhost:5002">golang</a></li>'
        all_content.append(item)
        all_content.append('</ul>')

        for (dirpath, filenames) in self._dirs.items():
            paragraph = '<h1>{}</h1>'.format(dirpath)
            all_content.append(paragraph)
            all_content.append('<ul>')
            for filename in filenames:
                filename = '{}.html'.format(filename[:-3])
                link_url = '{}/{}'.format(dirpath, filename)
                item = '<li><a href="/doc{}">{}</a></li>'.format(link_url,
                                                                 filename)
                all_content.append(item)

            all_content.append('</ul>')

        print(all_content)
        content = ''.join(all_content)
        html = '{}<body class="markdown-body">{}</body>'.format(self.header,
                                                                content)
        indx_path = '{}/{}'.format(self._dst_dir, index_file)
        with open(indx_path, 'w') as out_html:
            out_html.write(html)


def main():
    html_creator = CreatorHtml('/Users/zhangshizhuo/Work/doc', '/Users/zhangshizhuo/data/nginx/doc')
    html_creator.clean()
    html_creator.create()


if __name__ == '__main__':
    main()
