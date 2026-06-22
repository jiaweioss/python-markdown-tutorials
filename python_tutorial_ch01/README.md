# Python Markdown 教程书：第1章详细版

本包是第1章《Python基础知识与工作环境》的详细教材交付。

## 内容

- `chapters/ch01_python_basics_work_env.md`：第1章 Markdown 教材正文
- `assets/ch01/`：第1章正式版配图素材，已统一整理为 1800px 宽的居中图片
- `assets/ch01/web/`：从 Wikimedia Commons、JetBrains 官方文档、xkcd 下载的真实图片和梗图原图，并保存 PowerShell 本机窗口实拍、完整运行证据素材与 JetBrains 官方 PyCharm 真实界面截图
- `code/ch01/`：第1章可运行 Python 示例代码
- `source_notes/source_manifest_ch01.md`：来源线索记录
- `source_notes/quality_audit_ch01.md`：第1章质量验收记录
- `source_notes/beginner_practice_report_ch01.md`：第1章初学者实操检测报告
- `scripts/check_links.py`：Markdown 与 HTML 图片链接检查脚本
- `scripts/generate_ch01_visuals.py`：第1章正式版图片生成脚本
- `manifest.json`：交付清单

## 本轮优化重点

- 精简与第0章重复的开场铺垫，把第1章更明确地定位为“让 Python 在本机跑起来”的通电章。
- 将真实运行环境截图前置到正文 1.1 和 1.2：PowerShell 改成 4 步验电表，PyCharm 改成 5 步核对表，并统一为“先文字讲解和命令，再看对应截图与图注”；正文明确提醒不同版本界面可能不同，但要核对的证据始终是目录、解释器、pip、PyCharm 路径和输出。
- 修复图1-8 的 Windows 中文输出乱码：生成脚本对子进程运行统一设置 UTF-8 输出环境，重新生成后的运行证据图中文显示正常。
- 新增 `ch01_pycharm_environment_focus.png`，用 PyCharm 真实界面截图强调解释器路径与 Run 窗口输出要一起核对，解释文字全部放在 Markdown 图注和正文中。
- 新增 `ch01_runtime_environment_side_by_side.png`，把本章 PowerShell 完整运行证据和真实 PyCharm Run 窗口同屏展示，图内不新增解释文字，说明放在图注中。
- 将原 1.8 的重复环境截图段压缩为“环境证据总表”，并继续把 1.15-1.16 写成环境证据复习卡，避免同一组截图和 pip 逻辑讲两遍。
- 保留 Guido、CWI、Wundt、Stroop、xkcd 等故事与心理学素材，让环境配置不变成枯燥安装说明书。
- 新增并整理 Guido、CWI、Grace Hopper、BBC Broadcasting House、Wundt 实验室和 Stroop 效应等互联网图片素材。
- 新增 `ch01_xkcd_antigravity_card.png`，以无新增解释文字的图片形式呈现 `import antigravity` 梗图，说明文字放在正文与图注中。
- 新增 `ch01_xkcd_environment_card.png`，以无新增解释文字的图片形式呈现 xkcd 1987《Python Environment》，解释放在图片下方。
- 更新 `ch01_powershell_create_venv.png`、`ch01_powershell_python_locator.png` 和 `ch01_powershell_policy_fallback.png`，去掉图片里的额外解释文字，只保留命令和输出，说明统一放在 Markdown 正文与图注中。
- 更新 `ch01_powershell_python_locator.png`，用本机实际命令输出说明 `py -0p`、`python`、`pip`、`where.exe python` 和 `where.exe pycharm64.exe` 应该如何一起核对；正文特别解释真实电脑上多个命令不一致时要优先看 `sys.executable`。
- 新增 `ch01_powershell_policy_fallback.png`，补上执行策略阻止 `Activate.ps1` 时的备用做法：直接调用 `.venv\Scripts\python.exe`。
- 新增 `ch01_powershell_local_environment_check.png`，用本机 PowerShell 实拍窗口呈现版本、pip、解释器路径和当前工作目录四类证据。
- 新增 `ch01_powershell_full_runtime_check.png`，把本机实际运行 `python --version`、`python -m pip --version`、`01_hello_python.py`、`02_environment_check.py` 和 `04_show_me_the_python.py` 的输出整理成一张上机证据图。
- 在后半章补入 `ch01_powershell_environment_check.png`、`ch01_knowledge_route.png`、`ch01_core_metaphor_workshop.png`、`ch01_powershell_pathlib_demo.png` 和 `ch01_powershell_submission_evidence.png`，让图片从开头集中展示改为平均穿插到安装路线、Hello 程序、Python 之禅、路径检查和提交证据中。
- 新增 `ch01_first_script_feedback_loop.png`，把 `print()`、脚本命名、项目目录和运行证据串成一张无解释文字的反馈回路图，说明放在图注和正文里。
- 更新 `ch01_pycharm_main_window.png`，改用 JetBrains 官方 PyCharm 主窗口总览图，避免和解释器入口图重复，让学生先看到 IDE 的真实工作台布局。
- 整理 `ch01_pycharm_new_project.png`、`ch01_pycharm_interpreter_widget.png`、`ch01_pycharm_select_interpreter.png`、`ch01_pycharm_virtualenv_setup.png`、`ch01_pycharm_existing_virtualenv.png` 和 `ch01_pycharm_run_console.png`，让 PyCharm 从主界面识别、新建项目、选择解释器、创建或复用 `.venv` 到 Run 窗口输出形成完整实操链路。
- 新增 `ch01_pycharm_edit_configurations.png`、`ch01_pycharm_run_configuration_script.png`、`ch01_pycharm_modify_run_options.png` 和 `ch01_pycharm_run_widget.png`，把 Run Configuration 的入口、脚本路径、工作目录和运行按钮讲清楚。
- 删除正文中的环境排错流程图，把解释器、pip、当前目录的判断改为 Markdown 速查表；保留少量必要模型图：pip 管线和报错地图。
- 本章心理学预告改为极简 Stroop 任务，示例脚本同步更新为颜色词反应时小实验。
- 继续精简和第0章重复的“科研卡片工厂”铺垫，把 1.3-1.7 的总论段落进一步压短为短故事、够用概念和心理学应用直觉，并把后半段重复的学习习惯、自测、误区、评价清单和上机速查压缩为“上机路线与提交证据”和“本章总结”。
- 新增 `ch01_powershell_project_navigation.png`，并保留 PowerShell 环境检查和连续运行截图，讲清从项目目录定位到 `hello` 脚本、环境检查脚本的完整复现路径。
- 将 PyCharm 官方真实截图提前到工作环境章节，讲清新建项目、解释器入口、解释器列表、新建 virtualenv 和 Run 窗口输出。
- 正文 34 张图片全部使用居中的 `<figure>` 结构，并在图片下方使用 `<figcaption>` 显示清晰图注。
- 本轮复查后，34 张图片前均已有文字讲解、命令说明或过渡句，统一为“先叙述，再图片和图注”。
- 修复 `scripts/generate_ch01_visuals.py` 的 PNG 保存方式，重新生成后 63 张 PNG/JPG/GIF 均通过 PIL 打开验证。
- 新增初学者实操检测报告，记录 6 个示例脚本、交互脚本输入、图片链接、语法检查、PIL 图片检查和图文顺序检查结果。
- 本章项目改为“科研卡片工厂通电日志”，代码会生成 `reports/ch01_environment_log.txt`。
- 正文只保留简短来源说明，详细来源与授权集中放入 `source_notes/source_manifest_ch01.md`，避免打断学生阅读。

## 推荐阅读方式

先打开 `chapters/ch01_python_basics_work_env.md`，按正文顺序阅读；遇到代码示例时，在 `code/ch01/` 中运行对应脚本。

## 代码运行建议

在本包根目录下运行：

```bash
python code/ch01/01_hello_python.py
python code/ch01/02_environment_check.py
python code/ch01/04_show_me_the_python.py
python code/ch01/05_experiment_preview.py
```

第1章代码仅使用 Python 标准库，不需要额外安装第三方库。
