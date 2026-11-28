/* Original ClimateOS illustrative campus. World x/y/z in drawing units.
 * ClimateMap.init(canvas,{onPick,onViewChange}) returns update, reset,
 * bindMinimap and destroy. All input/output hours describe a scenario. */
(() => {
  'use strict';
  const ISO_X = .86, ISO_Y = .43, TOP_X = .70, TOP_Y = .70;
  const INK = '#677360', EDGE = '#829078', GRASS = '#c0cba6';
  const anchors = {
    cold: {x:-101,y:5,z:53,name:document.documentElement.lang.startsWith('en') ? 'Cold store' : '制冷车间',color:'#397a8b'},
    tank: {x:47,y:-87,z:41,name:document.documentElement.lang.startsWith('en') ? 'Heat tank' : '储热罐',color:'#b56743'},
    wash: {x:104,y:68,z:34,name:document.documentElement.lang.startsWith('en') ? 'Wash room' : '清洗车间',color:'#a57c38'}
  };
  const seeds = (n) => () => ((n = (Math.imul(n,1664525)+1013904223)>>>0)/4294967296);
  const xy = (u,v) => [(u+v)/2,(v-u)/2];
  const ribbon = (u) => -271+55*Math.sin(u/144)+19*Math.cos(u/78);
  const route = [[-48,23,4],[-29,23,4],[-29,-46,4],[48,-46,4],[48,-83,4]];
  const route2 = [[48,-83,4],[77,-83,4],[77,21,4],[106,21,4],[106,44,4]];
  const clamp = (x,a,b) => Math.max(a,Math.min(b,x));
  const fields = [], grasses = [], trees = [], rocks = [];
  const rand = seeds(723811);
  for(let x=-1250;x<1220;x+=120) for(let y=-1200;y<1200;y+=150) {
    fields.push([x,y,Math.floor(rand()*6),rand()]);
  }
  for(let i=0;i<12500;i++) {
    const x=rand()*1540-770,y=rand()*1540-770;
    if (Math.abs(x+y-ribbon(x-y))>52) grasses.push([x,y,1+rand()*4.4,rand()]);
  }
  for(let i=0;i<3200;i++){
    const x=rand()*1640-820,y=rand()*1640-820,u=x-y,v=x+y,bank=v-ribbon(u);
    const field = Math.sin(x/75)*Math.cos(y/129)+Math.sin((x+y)/110)*.47;
    if(Math.abs(bank)<48 || Math.abs(x+239)<21 || Math.abs(y-151)<23 || Math.abs(y+151)<14 || (Math.abs(x-35)<225 && y>-145 && y<175))continue;
    if((Math.abs(bank)<100 && rand()>.12) || (field>.42 && rand()>.55))trees.push([x,y,11+rand()*17,rand(),rand()]);
  }
  for(let i=0;i<240;i++) {
    const u=rand()*2000-1000;rocks.push([...xy(u,ribbon(u)+(rand()>.5?1:-1)*(39+rand()*7)),rand()*3+1,rand()]);
  }
  const landTones=['#c7d1ac','#cbd3ad','#bbc89e','#c1cda5','#c9cea9','#bfcca6'];
  const crownTones=[['#768d6b','#91a77f','#a9bb93'],['#73876b','#8fa080','#a1b38e'],['#80916a','#9aa67d','#b0bb8d'],['#637f69','#7e9780','#92a68a']];
  function projection(mode,x,y,z=0) {
    return mode==='iso'?[(x-y)*ISO_X,(x+y)*ISO_Y-z]:[(x-y)*TOP_X,(x+y)*TOP_Y];
  }
  function painter(ctx,mode,scale){
    const p=(a)=>projection(mode,...a);
    function poly(pts,fill,stroke=null,lw=.7) {
      if(!pts.length)return; ctx.beginPath();
      pts.forEach((point,i)=>{const [x,y]=p(point);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)});
      ctx.closePath();if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=lw;ctx.stroke()}
    }
    function line(pts,color,w=.8,dash=[]) {
      ctx.beginPath();pts.forEach((q,i)=>{const [x,y]=p(q);if(i)ctx.lineTo(x,y);else ctx.moveTo(x,y)});
      ctx.strokeStyle=color;ctx.lineWidth=w;ctx.setLineDash(dash);ctx.stroke();ctx.setLineDash([]);
    }
    const rect=(x,y,w,d,fill,s=null,z=0)=>poly([[x,y,z],[x+w,y,z],[x+w,y+d,z],[x,y+d,z]],fill,s);
    function ellipse(x,y,z,rx,ry,color,stroke=null){
      const [a,b]=p([x,y,z]);ctx.beginPath();ctx.ellipse(a,b,rx,ry,0,0,Math.PI*2);
      if(color){ctx.fillStyle=color;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=.7;ctx.stroke()}
    }
    function box(x,y,w,d,h,top,left,right,z=0,stroke=INK){
      const t=z+h;
      if(mode==='iso'){
        poly([[x,y+d,z],[x+w,y+d,z],[x+w,y+d,t],[x,y+d,t]],left,stroke);
        poly([[x+w,y,z],[x+w,y+d,z],[x+w,y+d,t],[x+w,y,t]],right,stroke);
      }
      rect(x,y,w,d,top,stroke,t);
    }
    function shadow(x,y,w,d,h){
      if(mode==='iso')poly([[x,y+d],[x+w,y+d],[x+w,y],[x+w+h*.65,y+h*.23],[x+w+h*.65,y+d+h*.23],[x+h*.65,y+d+h*.23]],'#62766342');
    }
    function roof(x,y,w,d,h,peak,near,far){
      const c=y+d/2;
      if(mode==='iso')poly([[x+w,y,h],[x+w,c,h+peak],[x+w,y+d,h]],near,INK);
      poly([[x,y,h],[x+w,y,h],[x+w,c,h+peak],[x,c,h+peak]],far,INK);
      poly([[x,c,h+peak],[x+w,c,h+peak],[x+w,y+d,h],[x,y+d,h]],near,INK);
      for(let t=4;t<w;t+=5) {
        line([[x+t,c,h+peak],[x+t,y+d,h]],'#6e776b55',.5);
        line([[x+t,c,h+peak],[x+t,y,h]],'#7c817244',.5);
      }
    }
    function factory(x,y,w,d,h,kind){
      shadow(x,y,w,d,h+8);box(x,y,w,d,h,'#c5c9b7','#c8c6ac','#a4ab99');
      if(kind==='cold'){
        for(let k=0;k<4;k++){
          const a=x+k*w/4,b=a+w/4;
          if(mode==='iso'){
            poly([[a,y+d,h],[a,y+d,h+10],[b,y+d,h]],'#c6c4a8',INK);
            poly([[a,y,h],[a,y+d,h],[a,y+d,h+10],[a,y,h+10]],'#a3c2c2',INK);
          }
          poly([[a,y,h+10],[b,y,h],[b,y+d,h],[a,y+d,h+10]],k%2?'#d8d7bf':'#e0dcc5',INK);
          for(let j=4;j<d;j+=4.2)line([[a,y+j,h+10],[b,y+j,h]],'#9ca392',.52);
        }
        if(mode==='iso'){
          for(let k=0;k<4;k++) {
            const a=x+10+k*28;poly([[a,y+d,1],[a+18,y+d,1],[a+18,y+d,22],[a,y+d,22]],'#81999a',INK);
            for(let z=3;z<22;z+=3)line([[a,y+d,z],[a+18,y+d,z]],'#a5b4ab',.7);
            box(a-1,y+d,20,2.5,1,'#e6dcbc','#9b9c8a','#7c877e',22);
          }
          for(let a=5;a<d;a+=9)poly([[x+w,y+a,21],[x+w,y+a+6,21],[x+w,y+a+6,28],[x+w,y+a,28]],'#788f8b',INK);
        }
        box(x+w-19,y+4,14,18,5,'#d5d7c6','#acb5a6','#919d90',h+5);
        for(let a=0;a<2;a++)ellipse(x+w-11,y+9+a*8,h+10,3.4,1.8,'#74867e',INK);
      }else{
        roof(x-1,y-1,w+2,d+2,h,10,kind==='wash'?'#c7c4ac':'#9baaa6',kind==='wash'?'#d7d1b6':'#c1c9bb');
        if(mode==='iso'){
          for(let a=6;a<w-6;a+=12)poly([[x+a,y+d,13],[x+a+7,y+d,13],[x+a+7,y+d,21],[x+a,y+d,21]],'#819693',INK);
          for(let a=5;a<d-5;a+=13)poly([[x+w,y+a,9],[x+w,y+a+9,9],[x+w,y+a+9,20],[x+w,y+a,20]],'#778a83',INK);
          for(let a=4;a<w;a+=12)line([[x+a,y+d,3],[x+a+5,y+d,3]],'#b1b19a',.65);
        }
        box(x+w-15,y+8,5,6,12,'#a6aa99','#8f9986','#6f7f74',h+6);
      }
    }
    function tank(x,y,r,h){
      const [a,b]=p([x,y]),rx=r*(mode==='iso'?1.19:.99),ry=r*(mode==='iso'?.61:.99),top=mode==='iso'?b-h:b;
      if(mode==='iso'){
        ellipse(x+h*.24,y+h*.1,0,rx+2,ry,'#68785b40');
        ctx.beginPath();ctx.moveTo(a-rx,top);ctx.lineTo(a-rx,b);
        ctx.ellipse(a,b,rx,ry,0,Math.PI,0,true);ctx.lineTo(a+rx,top);ctx.fillStyle='#bf805a';ctx.fill();ctx.strokeStyle='#8f705a';ctx.lineWidth=.7;ctx.stroke();
        for(let k=1;k<=3;k++){ctx.beginPath();ctx.ellipse(a,b-h*k/4,rx,ry,0,0,Math.PI);ctx.strokeStyle='#a77553';ctx.stroke()}
        for(let i=1;i<5;i++){const f=Math.PI*i/5,sx=a+rx*Math.cos(f),sb=ry*Math.sin(f);ctx.beginPath();ctx.moveTo(sx,top+sb);ctx.lineTo(sx,b+sb);ctx.strokeStyle='#c8956d';ctx.stroke()}
      }
      ellipse(x,y,h,rx,ry,'#dfb489','#967e62');ellipse(x,y,h,rx*.78,ry*.78,null,'#c49b75');
      ellipse(x,y,h+1,2.7,1.7,'#af9475',INK);
    }
    function truck(x,y,body){
      shadow(x,y,18,7,6);box(x,y,14,7,6,body,'#afb6ac','#899891',1.7);
      box(x+14.5,y+.5,5.3,6,4.6,'#ded6ba','#c3c3af','#a9b6ac',1);
      if(mode==='iso')for(const t of [3,12,17])ellipse(x+t,y+7,1.5,1.45,1.5,'#586755');
    }
    function tree(x,y,size,shape,tone){
      const [u,v]=p([x,y]),sw=size*(shape>.72?.34:.50);
      ctx.beginPath();ctx.ellipse(u+size*.25,v+size*.12,sw*1.14,sw*.48,-.18,0,Math.PI*2);ctx.fillStyle='#62795c36';ctx.fill();
      const h=mode==='iso'?size:sw*.25,c=crownTones[Math.min(3,Math.floor(tone*4))];
      if(mode==='iso')line([[x,y,0],[x,y,size*.68]],'#7f8164',1.4);
      if(shape>.72 && mode==='iso'){
        for(let k=0;k<3;k++){
          const oy=v-h*.10-h*k*.19,w=sw*(1-k*.17);
          ctx.beginPath();ctx.moveTo(u,oy-h*.54);ctx.lineTo(u+w,oy);ctx.quadraticCurveTo(u,oy+w*.28,u-w,oy);ctx.closePath();ctx.fillStyle=c[k];ctx.fill();
        }
      }else{
        for(const [dx,dy,r,col] of [[.12,.06,.88,0],[-.33,-.10,.68,1],[.32,-.26,.60,1],[-.06,-.48,.67,2]]){
          ctx.beginPath();ctx.ellipse(u+dx*sw,v-h*.63+dy*sw,r*sw,r*sw*.88,0,0,Math.PI*2);ctx.fillStyle=c[col];ctx.fill();
        }
      }
    }
    function fence(points){
      line(points.map(q=>[...q,3.8]),'#8d9480',.68);
      for(let i=0;i<points.length-1;i++){
        const [x,y]=points[i],[ex,ey]=points[i+1],n=Math.ceil(Math.hypot(ex-x,ey-y)/10);
        for(let j=0;j<n;j++){const a=x+(ex-x)*j/n,b=y+(ey-y)*j/n;line([[a,b,0],[a,b,4.5]],'#7e8978',.80)}
      }
    }
    function base(){
      fields.forEach(([x,y,n,mark])=>{
        rect(x,y,120,150,landTones[n]);
        if(mark>.61)for(let i=4;i<120;i+=6)line([[x+i,y],[x+i,y+149]],'#929c702b',.7);
        if(mark<.23)line([[x,y+1],[x+118,y+1]],'#84987266',1.4);
      });
      grasses.forEach(([x,y,s,k])=>line([[x,y],[x+s,y-.5]],k>.7?'#e3dfb786':'#889e7959',.7));
      const lo=[],hi=[];
      for(let u=-2400;u<=2400;u+=7){lo.push(xy(u,ribbon(u)-40));hi.push(xy(u,ribbon(u)+40))}
      poly(lo.concat(hi.slice().reverse()),'#8db5b1','#a8b99d',3.5);
      for(const side of [-1,1]) {
        const pts=[];for(let u=-2400;u<2400;u+=7)pts.push(xy(u,ribbon(u)+side*35));
        line(pts,side>0?'#acc8ba':'#85aaa9',2.3);
      }
      const ripple=seeds(54177);
      for(let i=0;i<390;i++){
        const u=ripple()*2600-1300,j=(ripple()-.5)*64,len=3+ripple()*15;
        line([xy(u,ribbon(u)+j),xy(u+len,ribbon(u+len)+j)],'#d1e0cf82',.8);
      }
      rocks.forEach(([x,y,r,k])=>ellipse(x,y,0,r*1.4,r*.6,k>.5?'#a6ae96':'#95a48e'));
      rect(-181,-140,385,283,'#cfceb5','#adb29c');
      rect(-170,-116,365,230,'#cacbbb');
      rect(-181,98,385,44,'#bec49f');
      const road=(a,width)=>{line(a,'#9ea897',width+3);line(a,'#cecdb9',width);line(a,'#e5e2c9',.8,[7,9])};
      road([[-1100,151],[710,151]],17);
      road([[-239,-1200],[-239,151]],17);
      road([[-239,-150],[490,-150]],9);
      line([[-160,148],[-160,82],[173,82],[173,-147]],'#aaa99a',11);
      line([[-160,148],[-160,82],[173,82],[173,-147]],'#d7d4bf',9);
      for(let i=0;i<9;i++)line([[-139+i*11,55],[-139+i*11+4,64]],'#eee9d2',1);
      fence([[-180,128],[-180,-136],[184,-136]]);
      fence([[-142,129],[-100,129],[102,129],[134,129]]);
      const details=[];
      function item(depth,draw){details.push({depth,draw})}
      for(const a of trees)item(a[0]+a[1],()=>tree(...a));
      for(let i=0;i<10;i++){
        const a=[-119+i*23,115+(i%2)*3,13+i%4,.2+i%2*.59,(i%3)/3];item(a[0]+a[1],()=>tree(...a));
      }
      for(let i=0;i<6;i++){
        const a=[157,-109+i*27,14+i%4,.18,(i%3)/3];item(a[0]+a[1],()=>tree(...a));
      }
      item(3,()=>factory(-163,-27,127,62,32,'cold'));
      item(210,()=>factory(64,36,82,49,23,'wash'));
      item(-140,()=>factory(-157,-109,56,32,16,'utility'));
      item(-133,()=>factory(-85,-120,44,20,11,'utility'));
      for(const [x,y] of [[22,-94],[53,-91],[33,-62]])item(x+y+10,()=>tank(x,y,14,32));
      item(-80,()=>{box(-27,-105,12,39,3,'#adb2a2','#8c9788','#9ea690');for(let i=0;i<4;i++)box(-25,-101+i*9,9,6,6,'#c9cbbb','#9ba995','#819486',3)});
      item(47,()=>truck(-82,56,'#ddd6ba'));item(86,()=>truck(7,71,'#bdc6b6'));item(295,()=>truck(130,146,'#c3b093'));
      item(99,()=>box(13,59,25,11,9,'#b1b9a7','#929f94','#788e83'));
      item(405,()=>factory(214,141,65,41,18,'utility'));
      item(-435,()=>factory(-288,-246,47,26,19,'utility'));
      for(let i=0;i<6;i++){
        const x=245+(i%3)*46,y=-240+Math.floor(i/3)*55;
        item(x+y+38,()=>factory(x,y,24,16,10,'utility'));
      }
      // Supply/return traces follow yard corridors; routes behind plant geometry.
      for(const path of [route,route2]){line(path,'#a36e42',4.8);line(path,'#e7b36d',3)}
      details.sort((a,b)=>a.depth-b.depth);details.forEach(s=>s.draw());
    }
    return {base,line,p,ellipse};
  }
  const stylesheetFont='system-ui,"PingFang SC","Microsoft YaHei",sans-serif';
  const projectAnchor=(mode,id)=>{const s=anchors[id];return projection(mode,s.x,s.y,s.z)};
  function roundBox(ctx,x,y,w,h,r){
    ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);
    ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();
  }
  function init(canvas, options={}) {
    const state={mode:'iso',hour:14,selected:'cold',zoom:1,panX:0,panY:0};
    const ctx=canvas.getContext('2d'),cached=document.createElement('canvas');
    let mini=null,miniCleanup=()=>{}, w=0,h=0,ratio=1,scale=1,targets=[],frame=0,last=0,drag=null,destroyed=false,dirty=true,wasTouch=''; 
    const media=window.matchMedia('(prefers-reduced-motion: reduce)');
    function transform(){
      scale=Math.min(Math.max(w,300)/625,Math.max(h,230)/318)*state.zoom;
      state.panX=clamp(state.panX,-520*scale,520*scale);
      state.panY=clamp(state.panY,-220*scale,220*scale);
      return [w*.50+state.panX,h*.52+state.panY];
    }
    const toScreen=(x,y)=>{const [a,b]=transform();return [a+x*scale,b+y*scale]};
    function backdrop(){
      const c=cached.getContext('2d'),[ox,oy]=transform();
      c.setTransform(ratio,0,0,ratio,0,0);c.fillStyle=GRASS;c.fillRect(0,0,w,h);
      c.translate(ox,oy);c.scale(scale,scale);
      painter(c,state.mode,scale).base();
      dirty=false;
    }
    function labels(){
      const used=[],pins=[];
      ctx.font='600 12px '+stylesheetFont;
      const keys=Object.keys(anchors).sort((a,b)=>Number(a===state.selected)-Number(b===state.selected));
      for(const id of keys){
        const [u,v]=toScreen(...projectAnchor(state.mode,id)),active=id===state.selected,a=anchors[id],shift=state.mode==='plan'?11:6;
        if(u<-5||v<-5||u>w+5||v>h+5)continue;
        const bw=ctx.measureText(a.name).width+30,bh=26;
        const candidates = id==='cold'?[[u-bw-15,v-33-shift],[u-bw/2,v-45],[u+13,v-30]]:
          id==='tank'?[[u+13,v-38-shift],[u-bw/2,v-50],[u-bw-12,v-30]]:
          [[u+13,v+5],[u-bw/2,v+25],[u-bw-15,v+8]];
        let pos;
        for(const [x,y] of candidates){
          pos=[clamp(x,5,Math.max(5,w-bw-5)),clamp(y,5,Math.max(5,h-bh-5))];
          if(!used.some(([a,b,c,d])=>a<pos[0]+bw+6&&a+c+6>pos[0]&&b<pos[1]+bh+3&&b+d+3>pos[1]))break;
        }
        const [x,y]=pos;used.push([x,y,bw,bh]);
        const tipX=clamp(u,x+5,x+bw-5),tipY=clamp(v,y+3,y+bh-3);
        ctx.strokeStyle=active?'#3a503d':'#536b58';ctx.lineWidth=1.1;ctx.beginPath();ctx.moveTo(u,v);ctx.lineTo(tipX,tipY);ctx.stroke();
        ctx.beginPath();ctx.arc(u,v,active?4:3,0,Math.PI*2);ctx.fillStyle=a.color;ctx.fill();ctx.strokeStyle='#fcf9e8';ctx.lineWidth=1.4;ctx.stroke();
        ctx.save();ctx.shadowColor='#42523b35';ctx.shadowOffsetY=2;ctx.shadowBlur=5;
        roundBox(ctx,x,y,bw,bh,5);ctx.fillStyle=active?'#314e3d':'#f5f4e8';ctx.fill();ctx.restore();
        ctx.strokeStyle=active?'#344f3e':'#8c9a82';ctx.lineWidth=.8;roundBox(ctx,x,y,bw,bh,5);ctx.stroke();
        ctx.beginPath();ctx.arc(x+10,y+bh/2,3.1,0,2*Math.PI);ctx.fillStyle=active?'#f3d09d':a.color;ctx.fill();
        ctx.fillStyle=active?'#fffdf1':'#334c40';ctx.textBaseline='middle';ctx.fillText(a.name,x+20,y+bh/2+.5);
        pins.push({id,x,y,width:bw,height:bh,u,v});
      }
      targets=pins;
    }
    function minimap(){
      if(!mini)return;
      const mw=mini.clientWidth||120,mh=mini.clientHeight||72;
      if(mini.width!==Math.round(mw*ratio)||mini.height!==Math.round(mh*ratio)){
        mini.width=Math.round(mw*ratio);mini.height=Math.round(mh*ratio);
      }
      const c=mini.getContext('2d'),factor=Math.min(mw/1130,mh/620);
      c.setTransform(ratio,0,0,ratio,0,0);c.fillStyle='#bac6a1';c.fillRect(0,0,mw,mh);
      const p=(x,y)=>[mw/2+(x-y)*.86*factor,mh/2+(x+y)*.43*factor];
      const path=(pts,color,width)=>{c.beginPath();pts.forEach(([x,y],i)=>i?c.lineTo(...p(x,y)):c.moveTo(...p(x,y)));c.strokeStyle=color;c.lineWidth=width;c.stroke()};
      const river=[];for(let i=-800;i<805;i+=12)river.push(xy(i,ribbon(i)));
      path(river,'#85aead',Math.max(3,38*factor));path([[-800,151],[650,151]],'#e0dfc8',3);
      path([[-239,-800],[-239,151]],'#dcdac5',2);path([[-239,-150],[650,-150]],'#dcdac5',2);
      for(const t of trees){const [x,y]=p(t[0],t[1]);c.fillStyle='#7f96794b';c.fillRect(x,y,1.7,1.4)}
      for(const k of Object.keys(anchors)){const a=anchors[k],[x,y]=p(a.x,a.y);c.fillStyle=a.color;c.fillRect(x-2,y-2,5,4)}
      const sx=state.mode==='iso'?1:ISO_X/TOP_X,sy=state.mode==='iso'?1:ISO_Y/TOP_Y;
      const rw=w/scale*factor*sx,rh=h/scale*factor*sy,rx=mw/2-state.panX/scale*factor*sx-rw/2,ry=mh/2-state.panY/scale*factor*sy-rh/2;
      c.fillStyle='#243d3533';c.beginPath();c.rect(0,0,mw,mh);c.rect(rx,ry,rw,rh);c.fill('evenodd');
      c.strokeStyle='#355544';c.lineWidth=1.4;c.strokeRect(rx,ry,rw,rh);
    }
    function draw(ms){
      if(!w||!h||destroyed)return;
      if(dirty){backdrop();minimap()}
      ctx.setTransform(1,0,0,1,0,0);ctx.drawImage(cached,0,0);
      ctx.setTransform(ratio,0,0,ratio,0,0);
      const [ox,oy]=transform();
      const evening=state.hour>=17||state.hour<6;
      if(evening){ctx.fillStyle=state.hour>=21||state.hour<5?'#304d6723':'#a9835821';ctx.fillRect(0,0,w,h)}
      ctx.save();ctx.translate(ox,oy);ctx.scale(scale,scale);
      const brush=painter(ctx,state.mode,scale);
      ctx.lineDashOffset=media.matches?0:-(ms/120)%9;
      brush.line(evening?route2:route,evening?'#fff1bb':'#fff3b9',1.9,[2.2,6.8]);
      ctx.restore();labels();
    }
    function loop(ms){frame=0;if(ms-last>70){draw(ms);last=ms}if(!media.matches && !destroyed && !document.hidden)frame=requestAnimationFrame(loop)}
    function render(){draw(performance.now());if(!frame&&!media.matches&&!document.hidden)frame=requestAnimationFrame(loop)}
    function resize(){
      const box=canvas.getBoundingClientRect();w=box.width;h=box.height;if(!(w>0&&h>0))return;
      ratio=Math.min(window.devicePixelRatio||1,2.5);
      cached.width=canvas.width=Math.round(w*ratio);cached.height=canvas.height=Math.round(h*ratio);dirty=true;render();
    }
    const changed=()=>{dirty=true;render();options.onViewChange?.({...state})};
    function update(value={}){
      const before=JSON.stringify(state);
      if(value.mode==='plan'||value.mode==='iso')state.mode=value.mode;
      if(Number.isFinite(value.zoom))state.zoom=clamp(value.zoom,.72,2.4);
      if(Number.isFinite(value.hour))state.hour=clamp(Math.round(value.hour),0,23);
      if(Object.hasOwn(anchors,value.selected))state.selected=value.selected;
      if(before!==JSON.stringify(state))changed();
    }
    function reset(){state.panX=state.panY=0;state.zoom=1;changed()}
    const coord=(e)=>{const b=canvas.getBoundingClientRect();return [e.clientX-b.left,e.clientY-b.top]};
    function hit(x,y){
      const matched=targets.slice().reverse().find(a=>
        (x>=a.x-4&&x<=a.x+a.width+4&&y>=a.y-4&&y<=a.y+a.height+4)||
        Math.hypot(x-a.u,y-a.v)<13);
      if(matched)return matched.id;
      const [cx,cy]=transform(),u=(x-cx)/scale,v=(y-cy)/scale;
      const regions={cold:[-163,-27,127,62,32],wash:[64,36,82,49,23],tank:[5,-109,64,64,27]};
      for(const [id,[px,py,pw,pd,height]] of Object.entries(regions)){
        const hs=state.mode==='iso'?height:0;
        const a=u/(state.mode==='iso'?ISO_X:TOP_X),b=(v+hs)/(state.mode==='iso'?ISO_Y:TOP_Y);
        if((a+b)/2>=px&&(a+b)/2<=px+pw&&(b-a)/2>=py&&(b-a)/2<=py+pd)return id;
      }
      return null;
    }
    function down(e){if(e.button!==0||drag)return;drag={id:e.pointerId,x:e.clientX,y:e.clientY,px:state.panX,py:state.panY,moved:false};canvas.setPointerCapture(e.pointerId)}
    function move(e){
      if(!drag){canvas.style.cursor=hit(...coord(e))?'pointer':'grab';return}
      if(e.pointerId!==drag.id)return;
      const dx=e.clientX-drag.x,dy=e.clientY-drag.y;
      if(drag.moved||Math.hypot(dx,dy)>4){drag.moved=true;state.panX=drag.px+dx;state.panY=drag.py+dy;canvas.style.cursor='grabbing';changed()}
    }
    function up(e){
      if(!drag||e.pointerId!==drag.id)return;const moved=drag.moved;drag=null;
      if(canvas.hasPointerCapture(e.pointerId))canvas.releasePointerCapture(e.pointerId);canvas.style.cursor='grab';
      if(!moved&&e.type==='pointerup'){const id=hit(...coord(e));if(id){update({selected:id});options.onPick?.(id)}}
    }
    function wheel(e){if(e.shiftKey){e.preventDefault();update({zoom:state.zoom*(e.deltaY<0?1.12:1/1.12)})}}
    function bindMinimap(el){
      miniCleanup();mini=el;if(!mini)return;
      function seek(e){
        const box=el.getBoundingClientRect(),mw=box.width,mh=box.height,factor=Math.min(mw/1130,mh/620);
        const iso=state.mode==='iso';
        state.panX=-(e.clientX-box.left-mw/2)*scale/factor*(iso?1:TOP_X/ISO_X);
        state.panY=-(e.clientY-box.top-mh/2)*scale/factor*(iso?1:TOP_Y/ISO_Y);changed();
      }
      const begin=e=>{if(e.button!==0)return;el.setPointerCapture(e.pointerId);seek(e)};
      const travel=e=>{if(el.hasPointerCapture(e.pointerId))seek(e)};
      const end=e=>{if(el.hasPointerCapture(e.pointerId))el.releasePointerCapture(e.pointerId)};
      el.addEventListener('pointerdown',begin);el.addEventListener('pointermove',travel);el.addEventListener('pointerup',end);
      const prevTouch=el.style.touchAction;el.style.touchAction='none';
      miniCleanup=()=>{el.removeEventListener('pointerdown',begin);el.removeEventListener('pointermove',travel);el.removeEventListener('pointerup',end);el.style.touchAction=prevTouch};
      minimap();
    }
    const vis=()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0}else render()};
    const onMotion=()=>{cancelAnimationFrame(frame);frame=0;render()};
    canvas.addEventListener('pointerdown',down);canvas.addEventListener('pointermove',move);canvas.addEventListener('pointerup',up);
    canvas.addEventListener('pointercancel',up);canvas.addEventListener('wheel',wheel,{passive:false});
    document.addEventListener('visibilitychange',vis);media.addEventListener('change',onMotion);
    const observer=new ResizeObserver(resize);observer.observe(canvas);wasTouch=canvas.style.touchAction;canvas.style.touchAction='none';canvas.style.cursor='grab';resize();
    function destroy(){
      destroyed=true;cancelAnimationFrame(frame);observer.disconnect();miniCleanup();
      canvas.removeEventListener('pointerdown',down);canvas.removeEventListener('pointermove',move);canvas.removeEventListener('pointerup',up);
      canvas.removeEventListener('pointercancel',up);canvas.removeEventListener('wheel',wheel);document.removeEventListener('visibilitychange',vis);
      media.removeEventListener('change',onMotion);canvas.style.touchAction=wasTouch;
    }
    return {update,reset,bindMinimap,destroy};
  }
  window.ClimateMap={init};
})();
