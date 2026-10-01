/* MTG shared page script: hero network, table-of-contents highlight, copy buttons */
(function(){
"use strict";
var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

/* copy buttons */
document.querySelectorAll('[data-copy]').forEach(function(b){
  b.addEventListener('click',function(){
    var t=b.getAttribute('data-copy')||(b.parentNode.querySelector('pre')||{}).textContent||'';
    function ok(){var o=b.textContent;b.textContent='Copied';setTimeout(function(){b.textContent=o},1800)}
    if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t.trim()).then(ok,function(){})}
  });
});

/* table of contents: highlight the section in view */
var links=[].slice.call(document.querySelectorAll('.toc a'));
if(links.length&&'IntersectionObserver' in window){
  var map={};links.forEach(function(a){map[a.getAttribute('href').slice(1)]=a});
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){links.forEach(function(l){l.classList.remove('on')});var a=map[e.target.id];a&&a.classList.add('on')}})},{rootMargin:'-20% 0px -70% 0px'});
  Object.keys(map).forEach(function(id){var el=document.getElementById(id);el&&io.observe(el)});
}

/* hero network (same system as the home page, quieter) */
var hero=document.querySelector('.phero'),cv=hero&&hero.querySelector('canvas');
if(!cv||!cv.getContext)return;
var ctx=cv.getContext('2d'),N=[],P=[],F=[],W=0,H=0;
function small(){return innerWidth<640}
function init(){var r=hero.getBoundingClientRect(),d=Math.min(2,devicePixelRatio||1);W=r.width;H=r.height;cv.width=W*d;cv.height=H*d;ctx.setTransform(d,0,0,d,0,0);
  var n=Math.min(small()?18:44,Math.round(W*H/14000));N=[];for(var i=0;i<n;i++)N.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.14,vy:(Math.random()-.5)*.14,s:1.4+Math.random()*2,a:Math.random()*6.28,va:(Math.random()-.5)*.008,z:.4+Math.random()*.6})}
function D(){return small()?110:150}
function spawn(){var d=D();for(var t=0;t<10;t++){var a=N[Math.random()*N.length|0],b=null,bd=1e9;for(var j=0;j<N.length;j++){var c=N[j];if(c===a)continue;var q=Math.hypot(a.x-c.x,a.y-c.y);if(q<d&&q<bd&&Math.random()>.3){bd=q;b=c}}if(b){P.push({a:a,b:b,t:0,sp:.008+Math.random()*.008,h:1+(Math.random()*2|0)});return}}}
function draw(){var d=D(),i,j;ctx.clearRect(0,0,W,H);
  for(i=0;i<N.length;i++){var n=N[i];if(!reduce){n.x+=n.vx;n.y+=n.vy;n.a+=n.va}if(n.x<-20)n.x=W+20;if(n.x>W+20)n.x=-20;if(n.y<-20)n.y=H+20;if(n.y>H+20)n.y=-20}
  ctx.lineWidth=1;for(i=0;i<N.length;i++)for(j=i+1;j<N.length;j++){var a=N[i],b=N[j],dx=a.x-b.x,dy=a.y-b.y,q=dx*dx+dy*dy;if(q<d*d){ctx.strokeStyle='rgba(200,206,216,'+((1-Math.sqrt(q)/d)*.14*Math.min(a.z,b.z))+')';ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke()}}
  for(i=0;i<N.length;i++){n=N[i];ctx.save();ctx.translate(n.x,n.y);ctx.rotate(n.a);ctx.fillStyle='rgba(226,230,236,'+(.18*n.z+.06)+')';ctx.fillRect(-n.s,-n.s,n.s*2,n.s*2);ctx.strokeStyle='rgba(242,173,60,'+(.22*n.z)+')';ctx.strokeRect(-n.s-1.5,-n.s-1.5,n.s*2+3,n.s*2+3);ctx.restore()}
  if(reduce)return;
  for(i=P.length-1;i>=0;i--){var p=P[i];p.t+=p.sp;var e=p.t<.5?2*p.t*p.t:1-Math.pow(-2*p.t+2,2)/2,x=p.a.x+(p.b.x-p.a.x)*e,y=p.a.y+(p.b.y-p.a.y)*e;
    ctx.shadowColor='#f2ad3c';ctx.shadowBlur=10;ctx.fillStyle='#ffd48c';ctx.beginPath();ctx.arc(x,y,1.9,0,6.283);ctx.fill();ctx.shadowBlur=0;
    if(p.t>=1){F.push({n:p.b,r:0,l:1});if(--p.h>0){var bb=null,bd=1e9;for(j=0;j<N.length;j++){var c2=N[j];if(c2===p.b||c2===p.a)continue;var q2=Math.hypot(c2.x-p.b.x,c2.y-p.b.y);if(q2<d&&q2<bd){bd=q2;bb=c2}}if(bb){p.a=p.b;p.b=bb;p.t=0;continue}}P.splice(i,1)}}
  for(i=F.length-1;i>=0;i--){var f=F[i];f.r+=.8;f.l-=.024;ctx.strokeStyle='rgba(242,173,60,'+(f.l*.6)+')';ctx.strokeRect(f.n.x-f.r/2-3,f.n.y-f.r/2-3,f.r+6,f.r+6);if(f.l<=0)F.splice(i,1)}
  if(P.length<(small()?2:4)&&Math.random()<.03)spawn();
  if(!document.hidden)requestAnimationFrame(draw)}
document.addEventListener('visibilitychange',function(){if(!document.hidden&&!reduce)requestAnimationFrame(draw)});
var rt;addEventListener('resize',function(){clearTimeout(rt);rt=setTimeout(function(){init();if(reduce)draw()},150)});
init();requestAnimationFrame(draw);
})();
