# 第1章质量验收记录

验收日期：2026-06-17

## 验收范围

本次验收范围是 `python_tutorial_ch01` 包，重点包括：

- `chapters/ch01_python_basics_work_env.md`
- `assets/ch01/`
- `assets/ch01/web/`
- `scripts/generate_ch01_visuals.py`
- `scripts/check_links.py`
- `README.md`
- `manifest.json`
- `source_notes/source_manifest_ch01.md`

## 目标对照

| 需求 | 当前证据 | 状态 |
| --- | --- | --- |
| 精简与 ch0 重复内容 | 开头进一步压缩为真实运行任务；1.4-1.6 继续压短为够用概念；1.8 改为环境证据总表；第1章聚焦“环境通电” | 已完成 |
| 增加真实运行环境截图 | 正文前段集中呈现 PowerShell 本机窗口实拍、10 张 PowerShell 命令输出/运行证据素材、11 张 JetBrains 官方 PyCharm 真实界面原图整理图，并新增 PyCharm 解释器/Run 窗口核对图和 PowerShell/PyCharm 同屏核对图 | 已完成 |
| 讲清环境配置步骤 | 1.1-1.2 按 PowerShell 4 步验电和 PyCharm 5 步核对重写；用真实截图讲目录、解释器、`.venv`、Run Configuration、Run 输出和本机 `pycharm64.exe` 路径核对 | 已完成 |
| 减少流程图堆叠 | 移除正文中的环境排错流程图，保留 pip 管线和报错地图两个必要模型图 | 已完成 |
| 图片居中与图注 | 正文 34 张图片均使用 `<figure align="center">` 和 `<figcaption>` | 已完成 |
| 图片内不新增解释文字 | PowerShell 生成图已去掉额外英文说明，只保留命令和输出；讲解放在 Markdown 正文和图注中 | 已完成 |
| 运行截图顺序统一 | 1.1 和 1.2 已调整为先讲文字、命令和核对点，再展示对应 PowerShell / PyCharm 运行截图与图注 | 已完成 |
| 图1-8 中文乱码修复 | `generate_ch01_visuals.py` 对子进程统一设置 UTF-8 输出环境，重新生成后图1-8 中文正常显示 | 已完成 |
| 学生视角 | 正文面向学习者操作，不写“老师应该如何教学” | 已完成 |
| 图文叙事 | Guido、CWI、Grace Hopper、BBC Broadcasting House、Wundt、Stroop、xkcd 和真实 IDE/终端截图穿插在正文中，中段补入第一段脚本反馈回路图，后半章补入运行证据图与路径检查图以减少长段无图 | 已完成 |
| 图片平均穿插 | 新增 `ch01_first_script_feedback_loop.png`，把 `print()`、注释、脚本命名、项目目录和运行证据之间的长段无图切开；最大图片间隔从 209 行降到 171 行 | 已完成 |

## 当前素材清单

正式图片素材 34 张，其中当前正文引用 34 张：

- `ch01_cover.png`
- `ch01_story_timeline.png`
- `ch01_knowledge_route.png`
- `ch01_core_metaphor_workshop.png`
- `ch01_first_script_feedback_loop.png`
- `ch01_xkcd_antigravity_card.png`
- `ch01_psychology_applications.png`
- `ch01_ide_workbench.png`
- `ch01_powershell_create_venv.png`
- `ch01_powershell_project_navigation.png`
- `ch01_powershell_submission_evidence.png`
- `ch01_powershell_local_environment_check.png`
- `ch01_powershell_environment_check.png`
- `ch01_powershell_pathlib_demo.png`
- `ch01_powershell_python_locator.png`
- `ch01_powershell_policy_fallback.png`
- `ch01_powershell_run_scripts.png`
- `ch01_powershell_full_runtime_check.png`
- `ch01_pycharm_main_window.png`
- `ch01_pycharm_new_project.png`
- `ch01_pycharm_interpreter_widget.png`
- `ch01_pycharm_select_interpreter.png`
- `ch01_pycharm_virtualenv_setup.png`
- `ch01_pycharm_existing_virtualenv.png`
- `ch01_pycharm_edit_configurations.png`
- `ch01_pycharm_environment_focus.png`
- `ch01_pycharm_run_configuration_script.png`
- `ch01_pycharm_modify_run_options.png`
- `ch01_pycharm_run_widget.png`
- `ch01_pycharm_run_console.png`
- `ch01_runtime_environment_side_by_side.png`
- `ch01_pip_pipeline.png`
- `ch01_xkcd_environment_card.png`
- `ch01_error_map.png`

下载或截图式原图 29 张：

- `web/guido_van_rossum_pyconus24.jpg`
- `web/cwi_entrance.jpg`
- `web/grace_hopper_univac.jpg`
- `web/bbc_broadcasting_house_portland_place.jpg`
- `web/wundt_lab.jpg`
- `web/stroop_effect_example.png`
- `web/powershell_project_navigation.png`
- `web/powershell_python_environment_check.png`
- `web/local_powershell_environment_check.png`
- `web/powershell_python_locator.png`
- `web/powershell_create_venv.png`
- `web/powershell_policy_fallback.png`
- `web/powershell_ch01_run_scripts.png`
- `web/powershell_full_runtime_check.png`
- `web/powershell_pathlib_demo.png`
- `web/powershell_submission_evidence.png`
- `web/pycharm_main_window.png`
- `web/pycharm_create_project.png`
- `web/pycharm_python_interpreter_widget_dark.png`
- `web/pycharm_selecting_target_interpreter_dark.png`
- `web/pycharm_new_virtualenv_environment_dark.png`
- `web/pycharm_existing_virtualenv_environment_dark.png`
- `web/pycharm_edit_configurations.png`
- `web/pycharm_run_configuration_script.png`
- `web/pycharm_modify_run_options.png`
- `web/pycharm_run_widget.png`
- `web/pycharm_run_tool_window.png`
- `web/xkcd_353_python.png`
- `web/xkcd_1987_python_environment.png`

## 外部来源

- Python FAQ：<https://docs.python.org/3/faq/general.html>
- Guido van Rossum 的 Python 起源回忆：<https://www.python.org/doc/essays/foreword/>
- PEP 20：<https://peps.python.org/pep-0020/>
- Guido van Rossum 照片：<https://commons.wikimedia.org/wiki/File:Guido_van_Rossum_in_PyConUS24.jpg>
- CWI 入口照片：<https://commons.wikimedia.org/wiki/File:Entree_CWI.jpg>
- Grace Hopper 与 UNIVAC 照片：<https://commons.wikimedia.org/wiki/File:Grace_Hopper_and_UNIVAC.jpg>
- BBC Broadcasting House 照片：<https://commons.wikimedia.org/wiki/File:BBC_Broadcasting_House_Portland_Place.jpg>
- Wundt 实验室历史照片：<https://commons.wikimedia.org/wiki/File:Leipzig%27te_i%C3%A7g%C3%B6zlem_denemeleri.jpg>
- Stroop 效应练习素材：<https://commons.wikimedia.org/wiki/File:Stroop_effect_example.png>
- PyCharm 解释器配置截图：<https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html>
- PyCharm 主界面截图：<https://www.jetbrains.com/help/pycharm/guided-tour-around-the-user-interface.html>
- PyCharm 新建项目与 Run 窗口截图：<https://www.jetbrains.com/help/pycharm/creating-and-running-your-first-python-project.html>
- PyCharm 选择已有 virtualenv 截图：<https://resources.jetbrains.com/help/img/idea/2026.1/py_existing_virtualenv_environment_dark.png>
- PyCharm Run/Debug Configuration 截图：<https://www.jetbrains.com/help/pycharm/run-debug-configuration.html>
- PowerShell 项目目录定位、本机环境检查实拍、环境检查复盘、Python 与 PyCharm 定位探针、`.venv` 创建、执行策略备用运行、`pathlib` 路径检查、连续运行图、本章完整运行证据总览、第1章提交证据、PyCharm 解释器/Run 窗口核对图和 PowerShell/PyCharm 同屏核对图：本机运行命令后整理、截取或由本章生成脚本生成，图片内只保留命令和输出
- xkcd 353：<https://xkcd.com/353/>
- xkcd 1987：<https://xkcd.com/1987/>
- xkcd 授权说明：<https://xkcd.com/license.html>

## 验收命令

在 `python_tutorial_ch01` 目录下运行：

```bash
python scripts/generate_ch01_visuals.py
python scripts/check_links.py
```

语法、图片和清单检查：

```bash
@'
from pathlib import Path
from PIL import Image
import ast, json, re
root = Path.cwd()
md = root / "chapters/ch01_python_basics_work_env.md"
text = md.read_text(encoding="utf-8")
assert len(re.findall(r"<img\b", text)) == 34
assert len(re.findall(r"<figcaption>", text)) == 34
assert not re.findall(r"!\[[^\]]*\]\(", text)
for py in list((root / "code").rglob("*.py")) + list((root / "scripts").rglob("*.py")):
    ast.parse(py.read_text(encoding="utf-8"), filename=str(py))
for img in (root / "assets").rglob("*"):
    if img.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif"}:
        with Image.open(img) as im:
            im.verify()
data = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
assert data["chapter"]["asset_count"] == 63
assert data["chapter"]["image_refs"] == 34
print("ch01 quality audit OK")
'@ | python -
```

当前结果：

- 正文字符数：29709
- 正文图片引用数：34
- 正文 figcaption 数：34
- Markdown 图片语法数：0
- manifest 素材数：63
- `scripts/check_links.py`：通过，检查 1 个 Markdown 文件，0 个缺失本地图片链接
- Python 语法检查：通过，`py_compile` 覆盖 8 个 `.py` 文件
- 图片 PIL 打开检查：通过，63 张图片均可打开
- 图1-8 编码复查：通过，中文输出已正常显示，无乱码方块
- 图文顺序复查：通过，1.1 和 1.2 已统一为先文字讲解/命令，再放运行截图
- `01_hello_python.py`、`02_environment_check.py`、`03_import_this.py`、`04_show_me_the_python.py`、`05_experiment_preview.py`、`06_common_error_examples.py` 烟测：通过
- `05_experiment_preview.py` Stroop 预告烟测：通过，使用示例输入 `S001` 与 `j`
- 临时总览图人工检查：通过；34 张 ch1 正文图均居中展示，PowerShell / PyCharm 真实界面图无错位、无越界，生成图未新增解释性长文字
- 全书轻量一致性扫描：11 个章节目录、130 个 Python 文件、108 个 `code/` 脚本、281 个正文图片引用，0 个缺失本地图片、0 个图注数量不一致、0 个 manifest 不一致、0 个旧 `_audit*` 残留；另发现 ch03 练习工作区中 2 个非正文引用的 `figure.png` 示例文件不是有效图片，后续优化 ch03 时处理。

## 剩余边界

本次验收集中在 ch01。整套教程其他章节仍可继续沿用 ch0/ch1 的图文标准逐章审计、压缩重复内容、补真实运行截图和项目成果图。
