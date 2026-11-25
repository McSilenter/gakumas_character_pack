# 许可

学マス角色扩展包和它所扩展的 [Eidolon-SC](https://github.com/Sallyn0225/eidolon-sc) 一样，以 GNU Affero General Public License 第 3 版或（由你选择）任何更新的版本发布：你可以在这个许可下再分发、修改它。许可全文见 [LICENSE](LICENSE)。

扩展包构建出来的镜像是打过补丁的 Eidolon-SC，仍受 Eidolon-SC 的许可约束；`overlay/patches/` 就是这些改动的源码。把实例开放给别人通过网络使用时，请照 AGPL 第 13 条向他们提供源码，比如给出原项目和本仓库的地址。

Eidolon-SC 自己不受 AGPL 约束的部分（Spine 运行库、酒吧里 VA-11 HALL-A 的美术和音频、像素字体）见原项目的 LICENSING.md，扩展包没有改变它们的许可。

## 不受 AGPL 约束的部分

下面这些不属于本程序，不受 GNU Affero General Public License 约束，版权归各自的权利人：

- `characters/avatars/` 里的头像：取自《学园偶像大师》的官方图片，版权属于版权方。
- `characters/characters.toml` 的 `voice_id` 指向的 Fish Audio 音色：用游戏语音训练，不在本仓库里，版权属于版权方和配音演员。
- 人设（`characters/sheets/`）、资料（`characters/facts/`）里引用的游戏台词和官方介绍文的原文片段：版权属于版权方。引用它们只是为了说明角色，篇幅都很短。

这些部分请只在个人、非商业的范围内使用；版权方要求时会删除。

本仓库不含游戏剧情原文。
