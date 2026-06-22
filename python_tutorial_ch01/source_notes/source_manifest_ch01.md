# 第1章来源记录

## 主来源

- `第一章_Python基础知识和工作环境Map2024.pptx`

本章内容依据原课件的课程主线重构，重点吸收以下内容：

1. Python 课程整体结构：基础知识与工作环境、数据类型与流程控制、函数与文件、面向对象、GUI、游戏开发、网络爬虫等。
2. Python 是什么：名字来源、Guido van Rossum、Monty Python、跨平台、解释型、交互式、面向对象。
3. Python 设计哲学：免费、开源、简单、优雅、Pythonic、`import this`。
4. Python 学习曲线与最近发展区。
5. 社会化编程、pip 管道、包安装与工具生态。
6. Python 在心理学中的应用：实验编程、PsychoPy、OpenSesame、眼动仪、游戏、VR、数据分析与可视化、人工智能。
7. Python 安装与开发工具：Python 官网、Anaconda、Spyder、IDE、环境检查。
8. 如何快速学习 Python：兴趣、项目、实践、反馈、分享。

## 参考来源

- MATLAB 基础与工作环境资料仅作为教学组织方式参考：借鉴其“工作环境—命令窗口—脚本—当前路径—学习习惯”的讲法，但最终内容全部改写为 Python 教程。
- MATLAB GUI 和数据分析资料仅作为“案例化叙事、任务驱动、图文讲解”的风格参考，没有迁移 MATLAB 技术内容作为第1章主题。
- Python 名字来源与 Monty Python 说明：Python 官方 FAQ  
  <https://docs.python.org/3/faq/general.html#why-is-it-called-python>
- Python 早期起源与 1989 年圣诞假期项目：Guido van Rossum 的 Python 起源回忆  
  <https://www.python.org/doc/essays/foreword/>
- Python 适合初学者的说明：Python 官方 FAQ  
  <https://docs.python.org/3/faq/general.html#is-python-a-good-language-for-beginning-programmers>
- Python 之禅：PEP 20  
  <https://peps.python.org/pep-0020/>
- Guido van Rossum 照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Guido_van_Rossum_in_PyConUS24.jpg>
- CWI 入口照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Entree_CWI.jpg>
- Grace Hopper 与 UNIVAC 照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Grace_Hopper_and_UNIVAC.jpg>
- BBC Broadcasting House 照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:BBC_Broadcasting_House_Portland_Place.jpg>
- Wundt 实验室历史照片：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Leipzig%27te_i%C3%A7g%C3%B6zlem_denemeleri.jpg>
- Stroop 效应教学素材：Wikimedia Commons  
  <https://commons.wikimedia.org/wiki/File:Stroop_effect_example.png>
- PyCharm 解释器配置截图：JetBrains 官方 PyCharm 帮助文档  
  <https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html>
- PyCharm 主界面截图：JetBrains 官方 PyCharm 帮助文档  
  <https://www.jetbrains.com/help/pycharm/guided-tour-around-the-user-interface.html>
- PyCharm 新建项目与运行窗口截图：JetBrains 官方 PyCharm 帮助文档  
  <https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html>
- PyCharm 选择已有 virtualenv 截图：JetBrains 官方 PyCharm 帮助文档  
  <https://resources.jetbrains.com/help/img/idea/2026.1/py_existing_virtualenv_environment_dark.png>
- PyCharm Run/Debug Configuration 截图：JetBrains 官方 PyCharm 帮助文档  
  <https://www.jetbrains.com/help/pycharm/run-debug-configuration.html>
- PyCharm Edit Configurations、Run Configuration、Modify options 和 Run Widget 原图：JetBrains 官方图片资源  
  <https://resources.jetbrains.com/help/img/idea/2026.1/py_edit_rcs.png>  
  <https://resources.jetbrains.com/help/img/idea/2026.1/py_add_new_configuration.png>  
  <https://resources.jetbrains.com/help/img/idea/2026.1/py_modify_rc_options.png>  
  <https://resources.jetbrains.com/help/img/idea/2026.1/py_angular_run_dev_mode.png>
- PowerShell 项目目录定位截图：本机运行 `cd`、`Get-Location`、`Get-ChildItem` 和 `Test-Path` 后整理
- PowerShell 本机环境检查实拍：本机打开 Windows PowerShell，运行 `python --version`、`python -m pip --version` 和 `02_environment_check.py` 后截取，正文图 `ch01_powershell_local_environment_check.png` 使用该素材
- PowerShell 环境检查整理图：本机运行 `python --version`、`python -m pip --version` 和 `02_environment_check.py` 后整理，作为备用素材保留
- PowerShell Python 定位图：`scripts/generate_ch01_visuals.py` 读取当前机器的 `py -0p`、`python --version`、`sys.executable`、`python -m pip --version`、`where.exe python` 和 `where.exe pycharm64.exe` 输出后整理，图内只保留命令和输出
- PowerShell 创建 `.venv` 图：由 `scripts/generate_ch01_visuals.py` 按本章推荐命令生成终端输出素材，图内不再放额外解释文字
- PowerShell 执行策略与 `.venv` 备用运行图：由 `scripts/generate_ch01_visuals.py` 按本章推荐命令生成终端输出素材，图内不再放额外解释文字
- PowerShell 连续运行截图：本机依次运行 `python --version`、`python -m pip --version`、`01_hello_python.py` 和 `02_environment_check.py` 后截取
- PowerShell 本章完整运行证据图：`scripts/generate_ch01_visuals.py` 在当前机器上实际运行 `python --version`、`python -m pip --version`、`01_hello_python.py`、`02_environment_check.py` 和 `04_show_me_the_python.py` 后整理，图内只保留命令和输出，正文图 `ch01_powershell_full_runtime_check.png` 使用该素材
- PyCharm 解释器与运行结果核对图：`scripts/generate_ch01_visuals.py` 组合 JetBrains 官方真实 PyCharm 选择已有解释器截图与 Run 窗口截图，图内不新增解释文字，正文图 `ch01_pycharm_environment_focus.png` 使用该素材
- PowerShell 与 PyCharm 同屏核对图：`scripts/generate_ch01_visuals.py` 组合本章 PowerShell 完整运行证据素材与 JetBrains 官方 PyCharm Run 窗口截图，图内不新增解释文字，正文图 `ch01_runtime_environment_side_by_side.png` 使用该素材
- 第一段脚本反馈回路图：`scripts/generate_ch01_visuals.py` 生成 `ch01_first_script_feedback_loop.png`，用文件、终端、反馈卡片、日志和文件夹符号连接 `print()`、脚本命名、项目目录与运行证据，图片内部不新增解释文字。
- `import antigravity` 梗图：xkcd 353《Python》  
  <https://xkcd.com/353/>
- Python 环境梗图：xkcd 1987《Python Environment》  
  <https://xkcd.com/1987/>
- xkcd 授权说明：CC BY-NC 2.5  
  <https://xkcd.com/license.html>

## 生成素材

本章正式版图片已经统一整理，采用 1800px 宽画布、统一留白和简洁构图。当前生成 34 张正式图片素材，其中 Markdown 正文引用 34 张；素材库保留 6 张下载的 Wikimedia 真实图片原图、11 张 JetBrains 官方 PyCharm 截图、10 张 PowerShell 截图素材和 2 张下载的 xkcd 梗图原图：

- `ch01_cover.png`
- `ch01_knowledge_route.png`
- `ch01_core_metaphor_workshop.png`
- `ch01_first_script_feedback_loop.png`
- `ch01_ide_workbench.png`
- `ch01_pip_pipeline.png`
- `ch01_powershell_create_venv.png`
- `ch01_powershell_environment_check.png`
- `ch01_powershell_full_runtime_check.png`
- `ch01_powershell_local_environment_check.png`
- `ch01_powershell_pathlib_demo.png`
- `ch01_powershell_policy_fallback.png`
- `ch01_powershell_project_navigation.png`
- `ch01_powershell_submission_evidence.png`
- `ch01_powershell_python_locator.png`
- `ch01_powershell_run_scripts.png`
- `ch01_pycharm_environment_focus.png`
- `ch01_pycharm_existing_virtualenv.png`
- `ch01_pycharm_edit_configurations.png`
- `ch01_pycharm_interpreter_widget.png`
- `ch01_pycharm_main_window.png`
- `ch01_pycharm_new_project.png`
- `ch01_pycharm_modify_run_options.png`
- `ch01_pycharm_run_configuration_script.png`
- `ch01_pycharm_run_console.png`
- `ch01_pycharm_run_widget.png`
- `ch01_pycharm_select_interpreter.png`
- `ch01_pycharm_virtualenv_setup.png`
- `ch01_runtime_environment_side_by_side.png`
- `ch01_psychology_applications.png`
- `ch01_error_map.png`
- `ch01_story_timeline.png`
- `ch01_xkcd_antigravity_card.png`
- `ch01_xkcd_environment_card.png`
- `web/xkcd_353_python.png`
- `web/xkcd_1987_python_environment.png`
- `web/guido_van_rossum_pyconus24.jpg`
- `web/cwi_entrance.jpg`
- `web/grace_hopper_univac.jpg`
- `web/bbc_broadcasting_house_portland_place.jpg`
- `web/wundt_lab.jpg`
- `web/stroop_effect_example.png`
- `web/powershell_project_navigation.png`
- `web/powershell_python_environment_check.png`
- `web/local_powershell_environment_check.png`
- `web/powershell_create_venv.png`
- `web/powershell_full_runtime_check.png`
- `web/powershell_pathlib_demo.png`
- `web/powershell_policy_fallback.png`
- `web/powershell_ch01_run_scripts.png`
- `web/powershell_python_locator.png`
- `web/powershell_submission_evidence.png`
- `web/pycharm_create_project.png`
- `web/pycharm_edit_configurations.png`
- `web/pycharm_existing_virtualenv_environment_dark.png`
- `web/pycharm_main_window.png`
- `web/pycharm_modify_run_options.png`
- `web/pycharm_python_interpreter_widget_dark.png`
- `web/pycharm_run_configuration_script.png`
- `web/pycharm_run_tool_window.png`
- `web/pycharm_run_widget.png`
- `web/pycharm_selecting_target_interpreter_dark.png`
- `web/pycharm_new_virtualenv_environment_dark.png`

当前正文重点使用 Guido、CWI、Grace Hopper 与 UNIVAC、BBC Broadcasting House、Wundt 实验室、Stroop 心理学任务、PowerShell 项目目录定位、PowerShell 本机环境检查实拍、PowerShell 环境检查复盘、PowerShell Python 与 PyCharm 定位探针、PowerShell 创建 `.venv`、PowerShell 执行策略备用运行、PowerShell `pathlib` 路径检查、PowerShell 连续运行脚本、PowerShell 本章完整运行证据总览、PowerShell 第1章提交证据、第一段脚本反馈回路图、PyCharm 解释器与运行结果核对图、PowerShell 与 PyCharm 同屏核对图、PyCharm 主窗口总览、解释器选择、新建项目、解释器配置、新建或选择已有 virtualenv、Run Configuration、Run 窗口输出、pip 管道、报错地图、`import antigravity` 梗图和 Python 环境混乱梗图。本轮继续精简 ch0 重复内容，把开头改成真实运行任务，把 PowerShell 配置压缩为 4 步验电表，把 PyCharm 配置压缩为 5 步核对表，并把 1.8 改成环境证据总表；同时在中段补入脚本反馈回路图，在后半章补入历史照片、PowerShell 复盘图、`pathlib` 路径图和提交证据图，让图片更平均穿插。生成图不再额外放置解释性长文字，解释内容统一放在 Markdown 正文与图注中。互联网原图仅用于学习类比，详细来源与授权说明集中记录在本文件中。

## 图文呈现规则

- 正文图片统一使用居中的 `<figure>` 结构。
- 图片本体使用 `<img ... style="zoom:50%; display:block; margin:0 auto;" />` 居中显示。
- 每张图片下方都有 `<figcaption>` 图注，图注负责标题、情境说明和学习提示。
- 本章项目延续第0章“科研卡片工厂”主线，最终产物是 `reports/ch01_environment_log.txt`。
