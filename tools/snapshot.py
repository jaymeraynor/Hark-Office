from PIL import Image, ImageDraw
import json,sys
D='/workspace/built/sites/82bece3a-e2c8-4974-8224-aeb2cf31cfbc/'
bg=Image.open(D+'office_bg.png').convert('RGBA'); W,H=bg.size
SIT={'gm':[47.97,27.0],'marketing':[33.6,53.4],'keyword':[21.4,64.8],'programmer':[38.5,66.7],'security':[31.50,78.91],'operations':[52.2,86.2],'analyst':[42.9,96.1],'trader':[55.1,99.1],'designer':[84.56,92.71]}
SH={'gm':9.4,'marketing':17.2,'keyword':17.6,'programmer':17.5,'security':14.84,'operations':17.5,'analyst':17.6,'trader':14.8,'designer':13.0}
SRC={'gm':'gm_sit_nokb.png','marketing':'marketing_back.png','keyword':'keyword_back.png','programmer':'programmer_side.png','security':'security_sit.png','operations':'operations_side.png','analyst':'analyst_back.png','trader':'trader_sit.png','designer':'designer_back_r.png'}
MIRROR={'operations'}
ZS={'designer':955}
items=[]
for k,(x,y) in SIT.items():
    items.append((ZS.get(k,round(y*10)),'actor',k))
for name,l,t,w,z in [('design_desk3.png',82.12,74.87,10.17,950),('design_chair3.png',82.12,74.87,10.17,960),('trader_desk_occluder.png',51.7,87,20.3,1500),('security_desk_occluder.png',28.05,67.06,12.72,835)]:
    items.append((z,'prop',(name,l,t,w)))
items.sort(key=lambda i:i[0])
state={}
try: state=json.load(open(sys.argv[1]))['roles']
except Exception: pass
working={ {'ops':'operations'}.get(k,k) for k,v in state.items() if v.get('status')=='working'}
for z,kind,v in items:
    if kind=='actor':
        im=Image.open(D+SRC[v]).convert('RGBA'); h=round(SH[v]/100*H); w=round(im.width*h/im.height)
        im=im.resize((w,h),Image.LANCZOS)
        if v in MIRROR: im=im.transpose(Image.FLIP_LEFT_RIGHT)
        x,y=SIT[v]; px=round(x/100*W-w/2); py=round(y/100*H-h)
        bg.alpha_composite(im,(px,py))
    else:
        n,l,t,wp=v; im=Image.open(D+n).convert('RGBA'); w=round(wp/100*W); h=round(im.height*w/im.width)
        bg.alpha_composite(im.resize((w,h),Image.LANCZOS),(round(l/100*W),round(t/100*H)))
_o=Image.open('/workspace/office_assets/gm_glass_occluder.png').convert('RGBA')
_o.putalpha(_o.getchannel('A').point(lambda a:int(a*0.6)))
bg.alpha_composite(_o)
d=ImageDraw.Draw(bg)
for k in working:
    x,y=SIT[k]; h=SH[k]/100*H; cx=x/100*W; cy=y/100*H-h-10
    d.ellipse([cx-9,cy-9,cx+9,cy+9],fill=(52,199,89,255),outline=(255,255,255,255),width=3)
bg.convert('RGB').save(sys.argv[2],'PNG',optimize=True)
