from pathlib import Path
from html import escape

ROOT=Path(__file__).parent
A='assets/'
TG='https://t.me/+aKiAKbEV8Rw3NDAy'
TAP='https://taplink.cc/russiacma'
# Masks isolate parts of the original raster; no illustration is redrawn.
STEP_POLYGONS=[
    [(281,894),(369,941),(971,827),(974,993),(367,1126),(281,1070)],
    [(242,649),(285,598),(800,592),(837,632),(837,752),(240,783)],
    [(348,450),(383,417),(703,418),(729,447),(729,546),(345,540)],
    [(501,339),(518,317),(761,317),(784,342),(783,403),(498,399)],
    [(623,274),(639,261),(817,263),(829,276),(827,318),(621,313)],
    [(700,232),(713,220),(833,222),(847,233),(846,261),(699,259)],
    [(750,204),(762,195),(865,196),(871,205),(870,221),(750,221)],
    [(790,184),(801,178),(886,177),(892,184),(889,196),(790,196)],
    [(827,167),(838,161),(899,161),(904,165),(903,175),(827,175)],
    [(872,155),(884,151),(927,152),(930,156),(929,160),(872,160)],
]
SEED_POLYGONS=[
    [(452,277),(481,231),(541,210),(593,220),(640,249),(675,300),(675,361),(652,386),(566,382),(543,355),(504,420),(486,449),(467,466),(459,458),(477,430),(500,394),(531,343),(488,325)],
    [(672,54),(850,54),(850,205),(720,205),(698,266),(672,270),(672,248),(713,168),(672,130)],
    [(908,20),(1060,20),(1060,133),(980,133),(937,189),(908,190),(908,170),(950,103),(908,75)],
    [(945,205),(1079,205),(1079,311),(1005,308),(975,343),(945,345),(945,324),(988,271),(945,244)],
    [(769,256),(912,256),(912,384),(845,388),(779,407),(742,409),(742,392),(808,328),(769,302)],
    [(666,433),(730,433),(768,477),(768,529),(713,539),(674,553),(647,562),(642,549),(677,511),(661,483)],
    [(801,438),(917,436),(954,496),(953,581),(934,634),(852,615),(760,641),(716,640),(716,620),(821,549),(785,489)],
    [(1010,376),(1100,376),(1100,448),(1051,448),(1011,470),(991,470),(991,452),(1034,426),(1010,406)],
]
GROW_POLYGONS=[[(0,0),(1122,0),(1122,835),(727,835),(727,913),(751,914),(752,941),(731,960),(716,956),(703,929),(684,886),(676,852),(655,835),(0,835)]]
BEAM_POLYGONS=[[(0,35),(760,192),(760,233),(0,460)]]
GRASS_POLYGONS=[
    [(79,310),(99,291),(119,286),(125,295),(114,329),(91,352),(62,424),(52,424),(72,366),(79,347)],
    [(226,179),(255,174),(286,220),(287,270),(281,282),(315,402),(306,407),(270,285),(247,269),(229,229)],
    [(162,275),(187,270),(207,309),(206,344),(204,409),(196,409),(193,346),(177,339),(163,305)],
    [(845,305),(875,284),(910,285),(913,297),(886,326),(858,337),(825,427),(816,426),(848,337)],
]
GRASS_ORIGINS=[(57,424),(310,404),(200,409),(820,427)]
def layered_art(name,cls,x,y,w,polygons,h=None):
    width,height=1122,1402
    # White rectangle with transparent holes works with alpha masks in all engines.
    holes=''.join('<polygon fill="black" points="'+ ' '.join(f'{px},{py}' for px,py in p)+'"/>' for p in polygons)
    mask=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><mask id="cutouts" maskUnits="userSpaceOnUse" x="0" y="0" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/>{holes}</mask></defs><rect width="100%" height="100%" fill="white" mask="url(#cutouts)"/></svg>'
    (ROOT/f'dist/assets/{name}-mask.svg').write_text(mask)
    height_style=f';--h:{h}' if h else ''
    base=f'<img class="scene-base" src="assets/{name}.webp" alt="" loading="lazy" decoding="async">'
    layers=[]
    for i,p in enumerate(polygons):
        clip='polygon('+','.join(f'{px/width*100:.6f}% {py/height*100:.6f}%' for px,py in p)+')'
        cx=sum(px for px,py in p)/len(p)/width*100;cy=sum(py for px,py in p)/len(p)/height*100
        kind={'steps':'step','dandelion':'seed','sprout':'grow','lighthouse':'beam','rest':'grass'}[name]
        flight=f';--park-x:{[-8,-5,-12,-7,-10,-18,-14,-8][i] if name=="dandelion" else 0}%;--park-y:{[-10,-7,-4,-4,-8,-13,-9,-7][i] if name=="dandelion" else 0}%;--park-turn:{(-1 if i%2 else 1)*(3+i)}deg;--fly-x:{35+i*4}%;--fly-y:{-18-i*2}%;--turn:{(-1 if i%2 else 1)*(8+i*2)}deg;--flight-duration:{18+i%3*3}s'
        origin='67.736185% 15.121255%' if kind=='beam' else '63.6% 66.5%' if kind=='grow' else f'{cx:.4f}% {cy:.4f}%'
        sway=''
        if kind=='grass':
            ox,oy=GRASS_ORIGINS[i]
            origin=f'{ox/width*100:.6f}% {oy/height*100:.6f}%'
            sway=f';--sway-positive:{[3.5,4.0,3.0,3.75][i]}deg;--sway-negative:{[-2.75,-3.25,-3.75,-2.75][i]}deg;--sway-duration:{[7.9,9.3,8.6,10.2][i]}s;--sway-phase:{[0,-2.8,-5.1,-1.5][i]}s'
        layers.append(f'<img class="{kind}-layer" src="assets/{name}.webp" alt="" loading="lazy" decoding="async" style="clip-path:{clip};--layer:{i};transform-origin:{origin}'+(flight if kind=='seed' else sway)+'">')
    trigger='<span class="acorn-trigger" aria-hidden="true"></span>' if name=='sprout' else ''
    return f'<div class="art main-art {name}-stage {cls} motion" style="--x:{x};--y:{y};--w:{w}{height_style}">'+base+''.join(layers)+trigger+'</div>'

# Split existing rasters with complementary masks; these paths do not redraw art.
LION_POLYGON=[(0,1065),(151,1058),(172,1005),(164,945),(171,886),(168,817),(181,741),(185,665),(207,587),(253,556),(293,547),(330,529),(378,506),(419,457),(455,412),(466,376),(507,348),(541,325),(557,300),(590,293),(624,256),(653,246),(688,243),(718,257),(753,241),(791,254),(818,232),(854,240),(889,258),(920,272),(943,299),(963,329),(968,370),(977,406),(991,450),(1007,489),(1006,538),(996,565),(978,590),(954,608),(920,626),(887,629),(870,649),(840,681),(808,712),(795,740),(760,760),(794,790),(844,798),(880,819),(916,820),(945,838),(963,868),(970,903),(968,942),(959,990),(952,1038),(981,1046),(1019,1065),(1091,1080),(1122,1120),(1122,1402),(0,1402)]
def paired_art(name,cls,x,y,w,polygon=None,width=1122,height=1402):
    if name=='hands':
        # Preserve the original joined-hands composition; split assets stay saved.
        content='<img class="pair-original" src="assets/hands.webp" alt="" loading="lazy" decoding="async">'
    else:
        polygons=[polygon]
        points=[' '.join(f'{px},{py}' for px,py in part) for part in polygons]
        for label,foreground in [('foreground',True),('background',False)]:
            rect='black' if foreground else 'white';fill='white' if foreground else 'black'
            silhouettes=''.join(f'<polygon points="{part}" fill="{fill}"/>' for part in points)
            mask=f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}"><defs><mask id="part"><rect width="100%" height="100%" fill="{rect}"/>{silhouettes}</mask></defs><rect width="100%" height="100%" fill="white" mask="url(#part)"/></svg>'
            (ROOT/f'dist/assets/{name}-{label}-mask.svg').write_text(mask)
        source='lion-light' if name=='lion' else name
        content=f'<img class="pair-original" src="assets/{source}.webp" alt="" loading="lazy" decoding="async"><img class="{name}-background" src="assets/{source}.webp" alt="" loading="lazy" decoding="async"><img class="{name}-foreground" src="assets/{source}.webp" alt="" loading="lazy" decoding="async">'
    return f'<div class="art main-art {name}-stage {cls} motion" style="--x:{x};--y:{y};--w:{w};aspect-ratio:{width}/{height}" aria-hidden="true">'+content+'<span class="illustration-trigger" aria-hidden="true"></span></div>'

def img(name,cls,x,y,w,extra='',h=None,angle=0):
    height=f';--h:{h}' if h is not None else ''
    return f'<img class="art {cls} motion" src="{A}{name}.webp" alt="" loading="'+('eager' if 'hero-part' in cls else 'lazy')+f'" decoding="async" style="--x:{x};--y:{y};--w:{w};--rotation:{angle}deg{height}" {extra}>'
def rule(cls,x,y,w,h=2,dot=False,size=80,position=72):
    # Match the circle's zoom start to the drawing head reaching its position.
    low,high=0.0,1.0
    for _ in range(24):
        t=(low+high)/2
        if 3*t*t-2*t*t*t < position/100: low=t
        else: high=t
    t=(low+high)/2
    phase=3*(1-t)**2*t*.4+3*(1-t)*t*t*.25+t**3
    point=f'<img class="line-point" src="assets/red-circle.webp" alt="" width="{size}" height="{size}" style="--point-size:{size};--point-position:{position}%;--point-phase:{phase:.5f}">' if dot else ''
    return f'<div class="rule motion line-reveal {cls}" aria-hidden="true" style="--x:{x};--y:{y};--w:{w};--h:{h}">{point}</div>'
def button(text='Найти встречу ↗',url=TG):
    return f'<a class="button" href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
def copy(text,cls=''):
    return f'<div class="copy {cls}">{text}</div>'
def body(text):
    # Paragraph spacing can be tuned without changing copy or revealing letters.
    if '<br><br>' in text:
        return '<div class="body">'+''.join(f'<p>{part}</p>' for part in text.split('<br><br>'))+'</div>'
    return f'<p class="body">{text}</p>'
def lead(text):return f'<p class="lead">{text}</p>'
def heading(text):
    lines='\n'.join(f'<span class="heading-line">{line}</span>' for line in text.split('<br>'))
    return f'<h2>{lines}</h2>'
def steps(items):return '<ol class="steps">'+''.join(f'<li><span class="num">{i:02d}</span><span>{t}</span></li>' for i,t in enumerate(items,1))+'</ol>'
def section(n,label,h,content):
    return f'<section class="section s{n}" id="section-{n}" aria-labelledby="title-{n}" style="--height:{h}"><div class="inner"><p class="eyebrow motion text-motion'+(' hero-part' if n==1 else '')+f'">{n:02d} / {label}</p>{content}</div></section>'
def visual(content):return '<div class="visual" aria-hidden="true">'+content+'</div>'
sections=[]
sections.append(section(1,'ЮБИЛЕЙ СООБЩЕСТВА',1100,
    '<header class="hero-header"><a class="brand" href="#section-1" aria-label="CMA — на начало страницы"><img src="assets/logo.svg" alt="CMA" width="64" height="64"></a><a class="header-link" href="'+TG+'" target="_blank" rel="noopener noreferrer">Найти встречу ↗</a></header>'+
    copy('<h1><span class="heading-line">5 ЛЕТ</span>\n<span class="heading-line">РОССИЙСКОМУ</span>\n<span class="heading-line">СООБЩЕСТВУ<span class="mobile-break"></span> <span class="hero-cma">CMA</span></span></h1>','hero-title')+
    copy(body('Пять лет встреч, поддержки,<br class="desktop-only"> опыта и выздоровления.')+lead('Жизнь без зависимости возможна.')+'<a class="text-link desktop-only" href="#section-2">Узнать больше ↓</a><div class="mobile-only">'+button()+'</div>','hero-intro')+
    visual(img('blue-circle','deco hero-part',1120,72,440,'data-depth="-6"')+img('seagull','seagull hero-part',982,142,238,h=179)+img('cloud','cloud hero-part',647,537,945,h=317)+img('panorama','main-art hero-part hero-panorama',507,442,836,'fetchpriority="high" data-depth="10"',h=627))+
    rule('hero-rule hero-part',0,916,396,dot=True,size=80,position=65)+rule('hero-axis vertical hero-part',1280,0,2,400)))
sections.append(section(2,'ПЯТЬ ЛЕТ',900,
    copy(heading('ПЯТЬ ЛЕТ<br>МЫ РЯДОМ')+body('Пять лет мы встречаемся, делимся опытом и поддерживаем друг друга.<br><br>Вместе создаём место, где можно говорить честно и быть услышанным.'))+
    visual(img('blue-circle','deco',-140,130,600)+'<span class="big-five motion">5</span>'+layered_art('lighthouse','',404,412,370,BEAM_POLYGONS))+rule('anniversary-rule',792,590,648)))
sections.append(section(3,'ЧТО ТАКОЕ CMA',980,
    copy(heading('ЧТО ТАКОЕ<br>CMA')+body('CMA — сообщество людей, которые помогают друг другу выздоравливать от химсекс-зависимости и наркотиков.<br><br>Мы делимся опытом, силой и надеждой — и продолжаем двигаться вперёд вместе.')+lead('Нет никаких взносов и сборов.<br>Главное — желание прекратить употребление.'))+
    visual(img('beige-sector','deco',975,145,450)+img('bicycle','main-art',775,130,565))+
    rule('about-rule',0,870,396,dot=True,size=80,position=45)+rule('bicycle-rule vertical',1368,130,2,620)))
sections.append(section(4,'ПРОГРАММА ДЕЙСТВИЙ',1160,
    copy(heading('12 ШАГОВ —<br>ЭТО ПУТЬ')+body('Программа 12 шагов помогает нам идти путём выздоровления.<br><br>Мы учимся принимать помощь, действовать и передавать свой опыт тем, кто еще страдает от зависимости.'))+
    visual(img('blue-rectangle','deco rectangle steps-shape',773,130,598,h=598,angle=-90)+layered_art('steps','',880,315,510,STEP_POLYGONS))+rule('divider',72,1090,1296)))
sections.append(section(5,'УЗНАТЬ СЕБЯ',1050,
    copy(heading('ЕСЛИ ТЫ<br>УЗНАЁШЬ СЕБЯ')+body('Ты пытался остановиться —<br class="desktop-only"> и снова возвращался.<br><br>Употребление стало связано с сексом, одиночеством или попыткой убежать от трудных чувств.<br><br>Хочется, чтобы всё было иначе.<br><br>Мы узнаём себя в этих чувствах. Наши встречи дают место, где об этом можно говорить открыто.')+lead('Тебе не обязательно<br class="desktop-only"> разбираться с этим одному.'))+
    visual(img('peach-circle','deco',-190,257,760)+layered_art('rest','',54,167,580,GRASS_POLYGONS))+
    rule('recognize-rule',1044,820,396,dot=True,size=80,position=30)))
supports=[('Встречи','Делимся опытом и слышим друг друга.'),('Сообщество','Учимся быть рядом и просить поддержки.'),('Наставник','Передаём опыт прохождения Шагов.'),('12 шагов','Применяем программу в повседневной жизни.')]
sections.append(section(6,'ЧТО ПОМОГАЕТ',1158,
    copy(heading('ВЫЗДОРОВЛЕНИЕ —<br>НЕ В ОДИНОЧКУ'))+
    '<dl class="support">'+''.join(f'<div><dt>{t}</dt><dd>{d}</dd></div>' for t,d in supports)+'</dl>'+
    visual(img('blue-circle','deco',24,515,500)+paired_art('hands','',110,345,490,width=1086,height=1448))+rule('support-rule vertical',720,324,2,680)))
words=['сон','ясность','отношения','движение','интерес','покой','обычная жизнь']
def animated_word(word):
    letters=''.join(f'<span class="letter" style="--letter-index:{i}">{escape(char)}</span>' for i,char in enumerate(word))
    return f'<li>{letters}</li>'
sections.append(section(7,'ВОЗВРАЩЕНИЕ К ЖИЗНИ',1086,
    copy(heading('ЖИЗНЬ БЕЗ<br>ЗАВИСИМОСТИ<br>ВОЗМОЖНА')+body('За эти годы мы делились не только трудностями, но и опытом возвращения к обычной жизни.<br><br>К простым вещам, которые снова обретают значение.'))+
    visual(img('peach-circle','deco lamp-light',586,57,972)+'<span class="lamp-glow" aria-hidden="true"></span>'+img('lamp','main-art lamp',891,364,452,h=678)+'<ul class="life-words">'+''.join(animated_word(w) for w in words)+'</ul>'+rule('life-rule vertical',828,100,2,330,dot=True,size=80,position=25))))
sections.append(section(8,'ПЕРВЫЙ ШАГ',1120,
    copy(heading('МОЖНО ПРОСТО<br>ПРИЙТИ')+body('За пять лет каждый из нас когда-то пришёл впервые.')+steps(['Найти встречу.','Прийти и послушать.','Познакомиться с людьми.','Прийти еще на одну встречу.'])+'<div class="first-step-cta">'+lead('Не нужно знать всё заранее.<br>Мы тоже начинали с первого шага.')+button()+'</div>')+
    visual(img('beige-sector','deco door-shape',827,219,552,angle=90)+'<div class="art main-art door-stage motion" style="--x:870;--y:285;--w:520" aria-hidden="true"><img class="door-open" src="assets/door.webp" width="1086" height="1448" alt="" loading="lazy" decoding="async"><img class="door-closed" src="assets/door-closed.webp" width="1086" height="1448" alt="" loading="lazy" decoding="async"></div>')+
    rule('door-rule vertical',792,390,2,300,dot=True,size=72,position=70)))
chair_positions=[(210,610,215),(475,540,210),(735,480,205),(1000,570,210),(900,830,245)]
# Equal visible chair height, excluding transparent margins (alpha >= 128).
# Keep each chair's horizontal centre and feet in their original places.
chair_bounds=[(352,7,495),(324,12,494),(299,12,484),(366,4,484),(365,13,472)]
chair_positions=[
    (round(x+(w-300*source_w/(bottom-top))/2,3),
     round(y+(w-300*source_w/(bottom-top))*bottom/source_w,3),
     round(300*source_w/(bottom-top),3))
    for (x,y,w),(source_w,top,bottom) in zip(chair_positions,chair_bounds)
]
sections.append(section(9,'МЕСТО ДЛЯ ТЕБЯ',1280,
    copy(heading('СООБЩЕСТВО —<br>ЭТО ВАЖНО')+body('Когда-то мы сами пришли на первую встречу.<br>Мы приходим разными, но узнаём себя в историях других.<br><br>Сегодня встречаем тех, кто только начинает свой путь.<br>Так живет наше сообщество.'))+
    visual(img('blue-rectangle','deco rectangle chairs-shape',204.5,394.5,531,h=796,angle=-90)+''.join(img(f'chair-group-{i}',f'chair chair-{i}'+(' chair-free' if i==5 else ''),x,y,w) for i,(x,y,w) in enumerate(chair_positions,1)))+rule('divider chairs-rule',72,1220,1296)))
sections.append(section(10,'НЕБОЛЬШИЕ ДЕЙСТВИЯ',960,
    copy(heading('ДЕНЬ<br>ЗА ДНЁМ')+body('День за днём мы учимся жить по-новому, поддерживать друг друга и расти.')+lead('Сегодня достаточно<br>сегодняшнего дня.'))+
    visual(img('peach-circle','deco',1010,100,560)+layered_art('sprout','',865,180,510,GROW_POLYGONS))+rule('daily-rule',0,800,396)+rule('daily-axis vertical',72,640,2,240)))
sections.append(section(11,'ПРИГЛАШЕНИЕ',980,
    copy(heading('ТЕБЕ НЕ НУЖНО<br>СПРАВЛЯТЬСЯ<br>ОДНОМУ')+body('Сегодня ты тоже можешь опереться на наш опыт и поддержку.<br><br>Прийти на встречу. Написать. Позвонить.')+button()+'<a class="text-link" href="'+TAP+'" target="_blank" rel="noopener noreferrer">Связаться с CMA ↗</a>')+
    visual(img('blue-circle','deco',152,80,480,'data-depth="-6"')+paired_art('lion','',0,241,547,LION_POLYGON))))
sections.append(section(12,'КОНТАКТЫ',480,
    copy(heading('МЫ РЯДОМ')+body('Первым шагом<br class="desktop-only"> может быть просто разговор.'))+
    '<address class="contacts"><a href="'+TG+'" target="_blank" rel="noopener noreferrer">Telegram / встречи ↗</a><a href="tel:+79214002581">+7 (921) 400-25-81</a><a class="email" href="mailto:russiacma@gmail.com">russiacma@gmail.com</a><a class="text-link" href="'+TAP+'" target="_blank" rel="noopener noreferrer">Все контакты / Taplink ↗</a></address>'+
    rule('divider contact-divider',72,432,1296)))
# Inline the user's unmodified SVG geometry so its real strokes can be drawn.
logo=(ROOT/'dist/assets/logo.svg').read_text()
logo=logo[logo.index('<svg'):].replace('<svg ', '<svg aria-hidden="true" ',1)
intro='<div class="intro-overlay" aria-hidden="true"><div class="intro-paper"></div><div class="intro-logo">'+logo+'</div></div><button class="intro-skip" type="button">Пропустить</button>'
boot='''<script>(()=>{try{if(!matchMedia('(prefers-reduced-motion: reduce)').matches&&!location.hash&&performance.getEntriesByType('navigation')[0]?.type!=='back_forward'){document.documentElement.classList.add('intro-pending');window.cmaIntroFallback=setTimeout(()=>{document.documentElement.classList.remove('intro-pending');const m=document.querySelector('main');if(m)m.inert=false;},9000);}}catch(e){}})();</script>'''
html='''<!doctype html>
<html lang="ru"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#FBF9F7"><title>5 лет российскому сообществу CMA</title><meta name="description" content="Пять лет встреч, поддержки, опыта и выздоровления. Жизнь без зависимости возможна. Найти встречу и связаться с российским сообществом CMA."><link rel="icon" href="assets/logo.svg" type="image/svg+xml"><link rel="preload" href="assets/inter-regular.ttf" as="font" type="font/ttf" crossorigin><link rel="preload" href="assets/inter-tight-variable.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="styles.css">'''+boot+'''<script src="app.js" defer></script></head><body><a class="skip" href="#section-3">Перейти к содержанию</a>'''+intro+'''<main>'''+''.join(sections)+'''</main></body></html>'''
# Reuse the original layered dandelion in a mobile-only footer decoration.
mobile_dandelion='<div class="mobile-dandelion"><div class="mobile-dandelion-figure"><img class="mobile-dandelion-shape" src="assets/beige-rectangle.webp" alt="" loading="lazy" decoding="async">'+layered_art('dandelion','mobile-dandelion-art',0,0,310,SEED_POLYGONS)+'<button class="mobile-dandelion-trigger" type="button" aria-label="Развеять пушинки одуванчика"></button></div></div>'
html=html.replace('</main>',mobile_dandelion+'</main>')
# Keep this public review page out of compliant search engines. Crawling stays
# allowed so bots can read noindex, including after an earlier indexed visit.
html=html.replace('<head>', '<head><meta name="robots" content="noindex, nofollow, noimageindex">',1)
footer='<footer class="site-footer"><div class="site-footer-inner"><a class="footer-brand" href="#section-1" aria-label="CMA — на начало страницы"><img src="assets/logo.svg" alt="CMA" width="36" height="36"><span>5 лет российскому сообществу CMA</span></a></div></footer>'
html=html.replace('</body>', footer+'</body>')
# Give each section a true heading and retain the artwork as independent files.
for n in range(1,len(sections)+1):
    token=f'id="section-{n}"'
    start=html.index(token); stop=html.find('</section>',start)
    chunk=html[start:stop];tag='<h1>' if n==1 else '<h2>'
    chunk=chunk.replace(tag,tag[:-1]+f' id="title-{n}">',1)
    html=html[:start]+chunk+html[stop:]
html=html.replace('<script src="app.js" defer>', '<link rel="stylesheet" href="motion.css"><link rel="stylesheet" href="editorial.css"><script src="app.js" defer>')
# Re-opened phones must fetch this animation rather than a cached previous script.
html=html.replace('href="styles.css"', 'href="styles.css?v=20261010-31"').replace('href="motion.css"', 'href="motion.css?v=20261017-puff3"').replace('href="editorial.css"', 'href="editorial.css?v=20261017-hero-cma1"').replace('src="app.js"', 'src="app.js?v=20261017-puff1"')
(ROOT/'dist/index.html').write_text(html)
