# guide

JavaGuide 独立学习镜像，保留原作者 Guide 与 JavaGuide contributors 署名。

仓库：`lovelsf-int/guide`。网站：`https://lovelsf-int.github.io/guide/`。
部署采用 GitHub Actions；2026-10-07 首次发布成功。此后更新均需重新完成构建、静态检查及线上验证。

## 来源与内容

- 上游：https://github.com/Snailclimb/JavaGuide
- 固定版本：`9eab7aaf1a538dc139e6886cb2237b6c61e9a000`
- Apache-2.0；完整许可证见 LICENSE，变更说明见 NOTICE。
- 原始源码 627 个文件，其中 docs 下 454 个 Markdown：446 个可生成页面、7 个共用片段、1 个排除的 TODO。
- Async.md 与 async.md 内容相同、文件名大小写不同。Git 和源码 ZIP 保留两者。macOS 默认文件系统只显示一个，GitHub Actions 的 Linux 构建可生成两个大小写页面。
- 首次本地构建生成 670 个 HTML（含分类、标签、索引与重定向）；新增专题目录后数量会增加。Linux 比 macOS 多一个大小写重复页，实际数量以发布检查输出为准。
- 开源正文及原作者署名保留；2026-10-09 为原先只有商业介绍的专题加入独立原创讲解，旧介绍保留在明确标记的文末。

## 保留的外部依赖

- 1,961 个不同的外部图片 URL（2,395 次原始引用），以 oss.javaguide.cn 为主；保留原地址，未做离线资源复制。
- 外链仍保留原目标。interview.javaguide.cn、idea.javaguide.cn 等独立子站及付费教程不包含在本仓库。
- 2026-10-09 取消本站开源正文的客户端截断；兼容 UnlockContent 标签直接渲染全文。未读取或复制原站未公开的商业课程正文。
- 本地搜索覆盖标题和小节标题，无需外部搜索账号。
- 原文保留原站 canonical 和原作者信息；原创补充页面使用本站 canonical，并明确署名；不启用上游百度统计。

## 构建与检查

要求 Node.js 22（至少 22.12）及 package.json 指定的 pnpm 10.0.0。

```sh
pnpm install --frozen-lockfile
pnpm docs:build
python3 scripts/verify-mirror.py
python3 scripts/verify-readable-content.py
```

静态产物在 dist/；它部署于 /guide/ 子路径。验证脚本扫描全部 HTML 内部链接、静态资源、许可证、站内搜索索引，以及指定文章的“一个最小请求链路”锚点。

## 发布

1. 在 lovelsf-int 下创建公开仓库 guide，或将上游 fork 命名为 guide。
2. 推送本地提交到该仓库 main 分支。
3. GitHub 仓库 Settings → Pages → Source 选择 GitHub Actions。
4. 运行 Publish guide to GitHub Pages 工作流；main 后续更新会自动发布。
5. 等工作流完成后验证网站首页及 `/guide/ai/system-design/ai-application-architecture.html#一个最小请求链路`。

首次启用后，可在 Actions 中查看构建与部署结果。线上行为应在部署成功后单独验证。
