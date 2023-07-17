# mc-assets-out
> 不知道你们有没有和我一样的疑惑，Mc的音效放在哪里？以前找了半天也找不着。

今天发现Mc的音效都是在assets文件夹里，但是名字都是hash值。简单写了个能提取 `.minecraft/assets` 中的资源文件的程序。

## 使用方法
### Step 0
当然你得先有Minecraft Java版的启动器，并且下载了至少一个版本。

### Step 1
找个地方克隆此库。

```bash
git clone https://github.com/the-cat1/mc-assets-out
```

### Step 2
复制 `.minecraft` 下的 `assets` 文件夹到根目录下（即 `mc-assets-out.py` 文件的旁边）。

### Step 3
启动 `mc-assets-out.py` 并选择版本(举例 `1.8`)，然后静静等待。

```
========== Assets Out ==========
Minecraft资源提取器(Version1.0)
By the-cat1
Github:https://github.com/the-cat1/mc-assets-out

查找indexes...
Minecraft assets indexes:
    1.17.json
    1.8.json
    legacy.json
    pre-1.6.json
请选择index文件(输入clean以删除输出目录)：1.8.json
读取index文件...
[成功] icons/icon_16x16.png
[成功] icons/icon_32x32.png
[成功] icons/minecraft.icns
<省略730行>
[成功] realms/lang/zh_TW.lang

--------------------------------
完成，已输出到目录：out/1.8。
共计：734文件，734成功，0失败。
```

### Step 4
然后，在 `out/1.8` 文件夹下，就可以看到资源文件了（还有背景音乐哦）。

```
mc-assets-out
    |
    |- out\1.8
    |   |- icons
    |   |   |- icon_16x16.png
    |   |   \- ...
    |   |- minecraft
    |   |   |- icons
    |   |   |   \- ...
    |   |   |- lang
    |   |   |   \- ...
    |   |   |- sounds
    |   |   |   |- ambient
    |   |   |   |   |- cave
    |   |   |   |   |   |- cave1.ogg
    |   |   |   |   |   |- cave2.ogg
    |   |   |   |   |   |- cave3.ogg
    |   |   |   |   |   \- ...
    |   |   |   |   \- ...
    |   |   |   \- ...
    |   |   \- sounds.json
    |   |- realms
    |   |   \-lang
    |   |       \- ...
    |   \- pack.mcmeta
    \- ...
```

### Step ∞
如果不用了可以在选择版本那里输 `clean` 。

## 原理
开头说了，其实资源文件都放在 `objects` 里，只不过名字变成hash值了。所以只要找到一个映射表，把文件名和hash值一一对应，我们只要改名字就行了。

刚好，在 `.minecraft/assets/indexes` 里，有几个JSON文件，对应不同的游戏版本。每个JSON都记录着原来的文件名和对应的文件大小、**hash值**。文件的格式如下：

```json
{
    "object": {
        "文件名1": {
            "hash": "文件的hash值",
            "size": 0 /*文件大小*/
        },
        "文件名2": {
            "hash": "文件的hash值",
            "size": 0 /*文件大小*/
        }
        // ...
    }
}
```

这样，文件hash值和文件名的对应关系搞定了。但是，文件在 `objects` 中的存储方式又和正常不一样：

```
objects
    |- 00
    |   |- 00b9b316015118f4b9be09e02bca0859519cd0aa
    |   |- 00b38fae5d28d99514a3e73a913af16359b12b7a
    |   \- ...
    |- 01
    |   \- ...
    \- ...
```

根据我的观察，每个文件在由它的hash值的前两位所组成的文件夹，就像这样：

```
objects
    |- 00
    |   |- 00XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   |- 00XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   \- ...
    |- 01
    |   |- 01XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   |- 01XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   \- ...
    |- 02
    |   |- 02XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   |- 02XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    |   \- ...
    \- ...
```

所以，改名字就很简单了，一个下午就整出来了，空行加起来也不够100行。
