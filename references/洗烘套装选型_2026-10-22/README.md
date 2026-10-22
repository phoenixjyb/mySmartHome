# 洗烘套装选型证据归档（2026-10-22）

[完整研究报告](../../docs/current/北京洗烘套装选型_600与610mm及博西C档_2026-10-22.md)

本目录保存本次调研实际使用的关键原始图片、厂家PDF和公开H5数据。没有保存京东登录状态、个人配送地址、账号信息或浏览器缓存。柜体图来自用户附件。资料用于复核候选，不能替代原厂现场安装确认；未购买、未联系商家。

| 文件 | 来源及用途 |
|---|---|
| [定制柜尺寸-用户提供.jpg](定制柜尺寸-用户提供.jpg) | 用户原始柜体图；净宽630、设备区约1750的初读来源，须核实完成面及板厚 |
| [松下M2-不含门尺寸.png](松下M2-不含门尺寸.png) | 京东M2Q1＋M2QR1原始商品图的PNG读取副本；明确505/550不含门 |
| [松下M2-叠放安装尺寸.png](松下M2-叠放安装尺寸.png) | 同一商品专属630×560×1722开口图 |
| [松下-通用安装须知.png](松下-通用安装须知.png) | 同页通用安装图，保留与专属图的侧边留空间口径差异 |
| [TCL-T10-含门和后留空.jpg](TCL-T10-含门和后留空.jpg) | [TCL T10官网](https://www.tcl.com/cn/zh/washing-machine/t10)安装图：含门580、背后30 |
| [东芝T19洗衣机说明书.pdf](东芝T19洗衣机说明书.pdf) | [原厂PDF](https://dsdcp.smartmidea.net/mcsp/prod/20231008/37b0d035bf7441c195a2161981e7165f.pdf)：最大580及背部30 |
| [东芝T19烘干机-新旧款安装对比.jpg](东芝T19烘干机-新旧款安装对比.jpg) | [原厂精确型号页面](https://www.midea.cn/59/1000000000400701806524.html)对比图；旧机突出30与新机安装深600不能混淆 |
| [海尔75DW-洗衣机原厂H5数据.json](海尔75DW-洗衣机原厂H5数据.json) | [公开H5数据](https://washerh5.haier.net/washShare/ies/CEAEFW000/D/web/prod.json)，精确型号XQG100-BLEG75DWU1，含556尺寸表及安装图来源 |
| [海尔75DW-烘干机原厂H5数据.json](海尔75DW-烘干机原厂H5数据.json) | [公开H5数据](https://washerh5.haier.net/washShare/ies/CF0J0C000/C/web/prod.json)，精确型号GA100-STQ75DWU1，含577尺寸表及安装图来源 |
| [海尔75DW-含门尺寸示意.png](海尔75DW-含门尺寸示意.png) | H5原始D/D1/D2/D3示意图，尺寸数值须结合JSON精确型号表，勿只看无数值示意 |
| [海尔75DW-洗衣机安装留空.png](海尔75DW-洗衣机安装留空.png) | 上述洗衣机H5安装图：后30、左右15、上20 |
| [海尔75DW-烘干机安装留空.png](海尔75DW-烘干机安装留空.png) | 上述烘干机H5安装图：后10、左右15、上20 |
| [博世WWJ752Y10W尺寸表.pdf](博世WWJ752Y10W尺寸表.pdf) | [原厂PDF](https://media3.bosch-home.com/Documents/specsheet/zh-CN/WWJ752Y10W.pdf)：565名义深与610外廓 |
| [西门子WW52J7Y00W尺寸表.pdf](西门子WW52J7Y00W尺寸表.pdf) | [原厂PDF](https://media3.bosch-home.com/Documents/specsheet/zh-CN/WW52J7Y00W.pdf)：C档白色推荐精确洗衣机 |
| [西门子WW52J7I80W尺寸表.pdf](西门子WW52J7I80W尺寸表.pdf) | [原厂PDF](https://media3.bosch-home.com/Documents/specsheet/zh-CN/WW52J7I80W.pdf)：另一精确洗衣机的565/610外廓 |
| [美的MGH20AIR说明书.pdf](美的MGH20AIR说明书.pdf) | [原厂PDF](https://dsdcp.smartmidea.net/mcsp/prod/20250110/77ff6caad54445de80b397a3aed40a90.pdf)：600＋后30的排除依据 |
| [小天鹅TG10VE40洗衣机说明书.pdf](小天鹅TG10VE40洗衣机说明书.pdf) | [原厂PDF](https://dsdcp.smartmidea.net/mcsp/prod/20250321/da045930008e488abd4a3bfbb7bcbba0.pdf)：582＋后30的排除依据 |

松下商品图的原始URL保留在研究报告对应章节；通用安装图来源为同一京东商品详情页。PNG副本仅为读取格式转换，未修改尺寸内容。H5 JSON只规范化换行、缩进和行尾空白，已校验解析后的数据完全相同。未单独留存的其他品牌参数仍可按报告给出的厂家页面追溯。

## 校验

本目录的`SHA256SUMS.txt`覆盖研究报告、目录说明及本目录证据文件（不含校验文件本身）。在仓库根目录执行：

```sh
shasum -a 256 -c references/洗烘套装选型_2026-10-22/SHA256SUMS.txt
```

这是独立研究资料归档，没有重建V3.2发布资料包；根目录已有的包级MANIFEST及其他未提交修改不在本次提交范围内。
