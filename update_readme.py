import re

def update_readme(stats_file, readme_file):
    # 读取统计数据
    with open(stats_file, 'r', encoding='utf-8') as f:
        stats = f.read().strip()

    # 读取 README 文件
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 更新统计数据
    pattern = r'(<!-- CODE_CHANGES -->).*?(<!-- CODE_CHANGES_END -->)'
    replacement = r'\1\n```\n个人代码统计:\n{}\n```\n\2'.format(stats)
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 写回 README 文件
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)

if __name__ == '__main__':
    update_readme('commit_stats.txt', 'README.md')