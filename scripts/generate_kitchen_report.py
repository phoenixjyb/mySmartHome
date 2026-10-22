#!/usr/bin/env python3
"""Generate a self-contained Chinese kitchen-appliance selection report."""
from __future__ import annotations
import argparse, base64, hashlib, html, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
EVIDENCE=ROOT/'references/厨电选型_2026-10-22'
SOURCES=[ROOT/'docs/current/北京厨房三件电器初筛与冰箱历史核对_2026-10-22.md',ROOT/'docs/current/北京博西冰箱850柜位复核_制冰与非制冰_2026-10-22.md']
TEMPLATE=ROOT/'scripts/templates/kitchen_report.html'
DEFAULT=ROOT/'exports/北京厨房电器选型_2026-10-22.html'
GALLERY=[
('cabinet-elevation','橱柜确认图_电器立面.png','橱柜确认图 · 电器立面','柜厂确认图','洗碗机与蒸烤机安装区域；尺寸仍需按完成面实测。'),
('kitchen-plan','橱柜确认图_厨房平面.png','橱柜确认图 · 厨房平面','柜厂确认图','洗碗机位在水槽与灶具之间；不是灶下位置。'),
('sju','博世SJU4HMB99C安装图.png','博世 SJU4HMB99C','厂家安装图','600–608mm净宽范围满足已确认的600mm净口；净高、净深及门板关系待核。'),
('sjv','博世SJV4HMX00C安装图.png','博世 SJV4HMX00C','厂家安装图','全嵌型号需按门板高度与踢脚开启路径重新深化。'),
('cs289','西门子CS289安装图.png','西门子 CS289ABS6W','厂家安装图','安装净宽560–568mm；600mm现有净口需固定侧衬调整。'),
('sx5','美的SX5地柜安装图.png','美的 SX5','厂家安装图','16A专用插座及散热条件按完整安装图落实。'),
('gc5','美的GC5地柜安装图.png','美的 GC5','厂家安装图','复合微波蒸烤路线；安装开口同样需调整到厂家范围。'),
('tq5w','东芝TQ5W安装图.png','东芝 TQ5W','厂家安装图','完整安装图存在多层宽深标注，勿以单一外形参数替代。'),]
def esc(s): return html.escape(s,quote=True)
def imgdata(name):
 p=EVIDENCE/name; mime='png' if p.suffix.lower()=='.png' else 'jpeg'
 return f'data:image/{mime};base64,'+base64.b64encode(p.read_bytes()).decode()
def safe_inline(s):
 s=esc(s)
 # Keep only web links. Local artifacts become explanatory non-links; private app links are removed.
 def link(m):
  label,url=m.group(1),html.unescape(m.group(2))
  if url.startswith('https://') and not re.search(r'(?:chatgpt\.com|openai\.com/c/|codex\.com)',url,re.I): return f'<a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{label}</a>'
  if url.startswith('codex://'): return label
  if url.lower().endswith(('.png','.jpg','.jpeg')):
   key=next((k for k,fn,*_ in GALLERY if fn==Path(url).name),None)
   return f'<a href="#evidence-{key}">查看归档图：{label} ↗</a>' if key else label
  return label
 s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,s)
 s=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',s)
 return re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
def cells(s): return [x.strip() for x in s.strip().strip('|').split('|')]
def markdown(s):
 lines=s.splitlines(); out=[]; i=0
 while i<len(lines):
  line=lines[i]
  if not line.strip(): i+=1; continue
  if line.startswith('|'):
   head=cells(line); i+=2; rows=[]
   while i<len(lines) and lines[i].startswith('|'):
    rows.append('<tr>'+''.join('<td>'+safe_inline(x)+'</td>' for x in cells(lines[i]))+'</tr>'); i+=1
   out.append('<div class="table-wrap" tabindex="0"><table><thead><tr>'+''.join('<th>'+safe_inline(x)+'</th>' for x in head)+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'); continue
  m=re.match(r'^(#{1,3}) (.*)',line)
  if m:
   level=min(len(m[1])+1,4); out.append(f'<h{level}>{safe_inline(m[2])}</h{level}>'); i+=1; continue
  if line.startswith('!['):
   alt=re.match(r'!\[([^]]*)\]\(([^)]+)\)',line)
   if alt:
    k=next((k for k,fn,*_ in GALLERY if fn==Path(alt[2]).name),None)
    out.append(f'<p><a href="#evidence-{k}">查看归档图：{safe_inline(alt[1])} ↗</a></p>' if k else '')
   i+=1; continue
  if line.startswith('- '):
   items=[]
   while i<len(lines) and lines[i].startswith('- '): items.append('<li>'+safe_inline(lines[i][2:])+'</li>'); i+=1
   out.append('<ul>'+''.join(items)+'</ul>'); continue
  para=[line]; i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(#{1,3} |\||- |!\[)',lines[i]): para.append(lines[i]); i+=1
  # Exclude the private handoff artifact and account-operation narrative entirely.
  joined=' '.join(para)
  if any(token in joined for token in ('refrigerator_jd_handoff','账户操作段落','没有变更收货地址','进入结算','本轮未申领','未收藏','账号最终实付')): continue
  out.append('<p>'+safe_inline(joined)+'</p>')
 return '\n'.join(out)
def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,default=DEFAULT); args=ap.parse_args(); output=args.output.resolve()
 parts=[p.read_text() for p in SOURCES]
 # Full relevant research is included; source-only private/account paragraphs are omitted above.
 full=''.join(f'<h2>{esc(p.stem)}</h2>'+markdown(src) for p,src in zip(SOURCES,parts))
 dishwasher_cards='''<article class="card"><span class="pill">洗碗机 · 优先核对</span><h3>博世 SJU4HMB99C</h3><p class="model">20套 · 自带黑色玻璃面板</p><strong>净口宽 600–608 mm</strong><p>已确认600mm净宽满足范围。净高780–835、净深≥550；约825mm高度仅为按图纸尺寸链推算，须实测。</p><p class="price">京东价格：未核 · 北京配送待核</p><a href="https://item.m.jd.com/product/10174664882256.html">京东博世官方旗舰店线索 ↗</a> <a href="#evidence-sju">安装图 ↓</a></article>
<article class="card"><span class="pill">洗碗机 · 全嵌备选</span><h3>博世 SJV4HMX00C</h3><p class="model">16套 · 需配橱柜门板</p><strong>净口宽 600–608 mm</strong><p>净宽条件满足；门板范围615–695mm。不得直接把720mm柜身做成整块机器门板，须核门板和踢脚开门路径。</p><p class="price">京东价格：未核 · 北京配送待核</p><a href="https://item.m.jd.com/product/10174984482587.html">京东博世官方旗舰店线索 ↗</a> <a href="#evidence-sjv">安装图 ↓</a></article>'''
 steam_cards='''<article class="card"><span class="pill">蒸烤一体机 · 无微波</span><h3>西门子 CS289ABS6W</h3><p class="model">45L · 独立蒸制与烤制</p><strong>需净宽 560–568 mm</strong><p>当前600mm净口偏宽，需固定侧衬/安装框每侧约16–20mm；另核460mm高度、净深、通风与2900W供电。</p><p class="price">京东价格：未核 · SKU待核</p><a href="https://www.jd.com/cppf/7375dd224412e51b1ff.html">京东准确型号目录 ↗</a> <a href="#evidence-cs289">安装图 ↓</a></article>
<article class="card"><span class="pill">蒸烤一体机 · 无微波</span><h3>美的 SX5</h3><p class="model">55L · 产品型号 TQN50E-TSBC00</p><strong>需净宽 560–568 mm</strong><p>600mm净口需侧衬调整。16A专用插座；柜后、柜底和柜前通风按完整图落实，深度标注须厂家澄清。</p><p class="price">京东页面价格未核 · 北京条件未核</p><a href="https://item.jd.com/100088782955.html">京东商品页 ↗</a> <a href="#evidence-sx5">安装图 ↓</a></article>
<article class="card"><span class="pill">蒸烤一体机 · 带微波</span><h3>美的 GC5</h3><p class="model">55L · 微波、蒸、烤复合</p><strong>需净宽 560–568 mm</strong><p>适合希望省去独立微波炉时比较。现有600mm净口需调整；16A及通风结构按准确手册落实。</p><p class="price">京东页面价格未核 · 北京条件未核</p><a href="https://item.jd.com/100068784671.html">京东商品页 ↗</a> <a href="#evidence-gc5">安装图 ↓</a></article>'''
 fridge_models=[
 ('西门子 KC89BV163C','自动制冰 · 502L · 京东预留850×600×1930mm；安装仍待厂家确认。','https://item.jd.com/100247956289.html','¥4,776.44 条件展示价 · 2026-10-22 · 国补资格与最终实付未确认','priority'),
 ('西门子 KC89BVA63C','自动制冰 · 厂家规格宽842、高1925；京东详情读取未完成，安装开口待核。','https://item.jd.com/100065033422.html','价格未核 · 京东详情读取超时',''),
 ('博世 KCB89VA26C','自动制冰 · 厂家规格宽842、高1925；销售方与北京配送待核。','https://item.jd.com/10219003019996.html','价格未核 · 目录线索',''),
 ('博世 KFB89VA21C','自动制冰 · 502L · 京东预留850×600×1930mm；页面标单循环。','https://item.jd.com/100307744189.html','¥5,596.84 条件展示价 · 2026-10-22 · 国补资格与最终实付未确认','priority'),
 ('西门子 KF88E1220C','不制冰基准候选 · 宽841、高1915；无制冰配置与深度待准确SKU/安装资料确认。','https://www.jd.com/book/7371f0695ab005dd40a.html','价格未核 · 准确SKU待解析',''),
 ('西门子 KF89CE163C','不制冰基准候选 · 宽841、高1915；双循环已见于规格书，无制冰配置与安装深度待核。','https://www.jd.com/jiage/1315e94f2fbc2859990d.html','价格未核 · 准确SKU待核',''),
 ('博世 KME50S97TI','不制冰基准候选 · 厂家规格宽835、高1915；深度与安装净空待核。','https://item.jd.com/100204728683.html','价格未核 · 页面卖家未确认',''),
 ('博世 KCP50A20TI','不制冰基准候选 · 厂家规格宽842、高1925；深度与循环/配置仍有冲突待核。','https://www.jd.com/jiage/737d27d91b21cb63807.html?electedExtAttrSet=266%2C&extAttrValue=expand_name%2C%40340773%3A%3A266&sort_type=sort_default','价格未核 · 准确SKU待解析','')]
 def fridge_card(item):
  name,fact,url,price,tone=item
  return f'<article class="card"><span class="pill">{ "自动制冰" if "自动制冰" in fact else "不制冰基准 · 配置待确认" }</span><h3>{esc(name)}</h3><p>{esc(fact)}</p><p class="price">{esc(price)}</p><a href="{esc(url)}">京东准确型号/目录线索 ↗</a></article>'
 fridge_html='<div class="fridge-group"><h3>自动制冰组 · 4款</h3><div class="cards">'+''.join(fridge_card(x) for x in fridge_models[:4])+'</div></div><div class="fridge-group"><h3>原讨论不制冰基准组 · 4款</h3><p class="muted">“不制冰”配置仍须按准确SKU确认；本组价格均未核。</p><div class="cards">'+''.join(fridge_card(x) for x in fridge_models[4:])+'</div></div>'
 gallery=''.join(f'<figure id="evidence-{k}"><button class="zoom" data-title="{esc(title)}" aria-label="放大查看：{esc(title)}"><img loading="lazy" src="{imgdata(fn)}" alt="{esc(title)}"></button><figcaption><b>{esc(title)}</b><p>{esc(cap)}</p><small>{esc(origin)}</small></figcaption></figure>' for k,fn,title,origin,cap in GALLERY)
 replacements={'@@DATE@@':'2026年10月22日','@@DISHWASHER_CARDS@@':dishwasher_cards,'@@STEAM_CARDS@@':steam_cards,'@@FRIDGE@@':fridge_html,'@@GALLERY@@':gallery,'@@FULL@@':full,'@@HASH@@':hashlib.sha256(''.join(hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCES).encode()).hexdigest()[:16]}
 page=TEMPLATE.read_text()
 for k,v in replacements.items(): page=page.replace(k,v)
 if '@@' in page: raise ValueError('Unfilled template token')
 output.parent.mkdir(parents=True,exist_ok=True); output.write_text(page)
 print(f'Generated {output} ({len(page.encode()):,} bytes; {len(GALLERY)} images; 2 source documents)')
if __name__=='__main__': main()
