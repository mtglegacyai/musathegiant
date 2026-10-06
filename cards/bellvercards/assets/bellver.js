/* Bellver Cards by MTG | shared behaviour (menu, reveals, 3D tilt, videos, calculators) */
(function(){
  'use strict';
  var d=document, root=d.documentElement;
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia('(pointer: fine)').matches;
  var $=function(s,c){return (c||d).querySelector(s)}, $$=function(s,c){return Array.prototype.slice.call((c||d).querySelectorAll(s))};
  var money=function(n){return '$'+Math.round(n).toLocaleString('en-US')};

  /* header, progress, back to top, mobile CTA */
  var hdr=$('.hdr'), bar=$('.progress'), top=$('.totop'), mcta=$('.mobile-cta'), heroEnd=$('[data-hero-end]');
  var ticking=false;
  function onScroll(){
    var y=window.scrollY, h=root.scrollHeight-window.innerHeight, p=h>0?Math.min(1,y/h):0;
    if(hdr) hdr.classList.toggle('scrolled',y>12);
    if(bar) bar.style.setProperty('--p',p.toFixed(4));
    if(top){top.classList.toggle('on',y>700);top.style.setProperty('--p',p.toFixed(4));}
    if(mcta){var past=heroEnd?heroEnd.getBoundingClientRect().top<0:y>500;var nearEnd=h-y<260;mcta.classList.toggle('on',past&&!nearEnd&&!menuOpen);}
    ticking=false;
  }
  window.addEventListener('scroll',function(){if(!ticking){ticking=true;requestAnimationFrame(onScroll);}},{passive:true});
  if(top) top.addEventListener('click',function(){window.scrollTo({top:0,behavior:reduce?'auto':'smooth'});});

  /* pull-down menu */
  var btn=$('.menu-btn'), menu=$('#bv-menu'), scrim=$('.scrim'), menuOpen=false;
  function setMenu(open){
    menuOpen=open;
    if(!btn||!menu) return;
    btn.setAttribute('aria-expanded',open?'true':'false');
    btn.querySelector('.lbl').textContent=open?'Close':'Menu';
    menu.classList.toggle('open',open);
    if(scrim) scrim.classList.toggle('on',open);
    if(hdr) hdr.classList.toggle('scrolled',open||window.scrollY>12);
    if(open){var first=menu.querySelector('a');if(first) setTimeout(function(){first.focus({preventScroll:true});},60);}
    onScroll();
  }
  if(btn) btn.addEventListener('click',function(){setMenu(!menuOpen);});
  if(scrim) scrim.addEventListener('click',function(){setMenu(false);});
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&menuOpen){setMenu(false);btn.focus();}});
  if(menu) $$('a',menu).forEach(function(a){a.addEventListener('click',function(){if(a.getAttribute('href').charAt(0)==='#') setMenu(false);});});

  /* reveal on scroll */
  var rvs=$$('.rv');
  if('IntersectionObserver' in window && !reduce){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    rvs.forEach(function(el){io.observe(el);});
  } else rvs.forEach(function(el){el.classList.add('in');});

  /* count up */
  var counters=$$('[data-count]');
  function runCount(el){
    var end=parseFloat(el.getAttribute('data-count')), pre=el.getAttribute('data-pre')||'', suf=el.getAttribute('data-suf')||'';
    if(reduce){el.textContent=pre+end.toLocaleString('en-US')+suf;return;}
    var t0=null,dur=1400;
    function step(t){if(!t0)t0=t;var k=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-k,4);el.textContent=pre+Math.round(end*e).toLocaleString('en-US')+suf;if(k<1)requestAnimationFrame(step);}
    requestAnimationFrame(step);
  }
  if('IntersectionObserver' in window){
    var co=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){runCount(e.target);co.unobserve(e.target);}});},{threshold:.6});
    counters.forEach(function(el){co.observe(el);});
  } else counters.forEach(runCount);

  /* 3D tilt (hero card, special edition) */
  if(fine && !reduce){
    $$('[data-tilt]').forEach(function(zone){
      var target=$(zone.getAttribute('data-tilt'),zone)||zone, max=parseFloat(zone.getAttribute('data-max')||'14'), glare=$('.glare',target), raf=null;
      zone.addEventListener('pointermove',function(e){
        var r=zone.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
        if(raf) cancelAnimationFrame(raf);
        raf=requestAnimationFrame(function(){
          target.style.transform='rotateY('+(x*max).toFixed(2)+'deg) rotateX('+(-y*max*.8).toFixed(2)+'deg) translateZ(20px)';
          if(glare){glare.style.setProperty('--gx',(50+x*90)+'%');glare.style.setProperty('--gy',(50+y*90)+'%');glare.style.setProperty('--go','1');}
        });
      });
      zone.addEventListener('pointerleave',function(){target.style.transform='';if(glare) glare.style.setProperty('--go','0');});
    });
  }

  /* video players: click-to-load (mp4 or YouTube) */
  $$('.player[data-src],.player[data-yt]').forEach(function(p){
    function play(){
      if(p.classList.contains('playing')) return;
      p.classList.add('playing');
      var yt=p.getAttribute('data-yt'), title=p.getAttribute('data-title')||'Video';
      if(yt){
        var f=d.createElement('iframe');
        f.src='https://www.youtube-nocookie.com/embed/'+yt+'?autoplay=1&rel=0&modestbranding=1&playsinline=1';
        f.title=title; f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'; f.allowFullscreen=true; f.referrerPolicy='strict-origin-when-cross-origin';
        p.appendChild(f);
      } else {
        var v=d.createElement('video');
        v.src=p.getAttribute('data-src'); v.controls=true; v.playsInline=true; v.preload='auto'; v.setAttribute('title',title);
        var poster=p.querySelector('img'); if(poster) v.poster=poster.currentSrc||poster.src;
        p.appendChild(v); var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){});
      }
      p.removeAttribute('role'); p.removeAttribute('tabindex');
    }
    p.addEventListener('click',play);
    p.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();play();}});
  });
  $$('[data-play]').forEach(function(a){a.addEventListener('click',function(e){var t=$(a.getAttribute('data-play'));if(!t)return;e.preventDefault();t.scrollIntoView({behavior:reduce?'auto':'smooth',block:'center'});setTimeout(function(){t.click();},reduce?0:650);});});

  /* card-pays-for-itself calculator */
  var calc=$('[data-calc="payback"]');
  if(calc){
    var PRICE={basic:99,premium:270,business:490,gold:990}, COM={basic:10,premium:100,business:200,gold:400}, COMSE={basic:10,premium:150,business:300,gold:500};
    var mine=$('[name=mine]',calc), theirs=$('[name=theirs]',calc), se=$('[name=se]',calc), out=$('output',calc), n=2;
    function upd(){
      var price=PRICE[mine.value], per=(se.checked?COMSE:COM)[theirs.value], earned=per*n, left=price-earned;
      $('[data-o=earned]',calc).textContent=money(earned);
      $('[data-o=price]',calc).textContent=money(price);
      var lb=$('[data-o=left]',calc), box=lb.parentNode;
      if(left<=0){lb.textContent=left===0?'Covered':'+'+money(-left);box.className='ok';box.querySelector('span').textContent=left===0?'Your card is':'Covered, plus';}
      else {lb.textContent=money(left);box.className='warn';box.querySelector('span').textContent='Still to cover';}
      $('.meter i',calc).style.width=Math.min(100,earned/price*100)+'%';
      out.textContent=n;
      var need=Math.ceil(price/per), hint=$('[data-o=hint]',calc);
      if(hint) hint.textContent=need<=n?'Your card is fully covered by these referrals.':'You need '+need+' referrals at this level to cover your card.';
    }
    $$('[data-step]',calc).forEach(function(b){b.addEventListener('click',function(){n=Math.max(0,Math.min(50,n+parseInt(b.getAttribute('data-step'),10)));upd();});});
    [mine,theirs,se].forEach(function(el){el.addEventListener('change',upd);});
    upd();
  }

  /* monthly rewards estimator */
  var est=$('[data-calc="rewards"]');
  if(est){
    var people=$('[name=people]',est), avg=$('[name=avg]',est), pv=$('[data-o=pv]',est), av=$('[data-o=av]',est);
    function upd2(){
      var p=parseInt(people.value,10), a=parseInt(avg.value,10), vol=p*a, r=vol*0.001;
      pv.textContent=p.toLocaleString('en-US'); av.textContent=money(a);
      $('[data-o=vol]',est).textContent=money(vol);
      $('[data-o=rew]',est).textContent=money(r);
      $('[data-o=year]',est).textContent=money(r*12);
      [people,avg].forEach(function(s){var k=(s.value-s.min)/(s.max-s.min)*100;s.style.setProperty('--k',k+'%');});
    }
    [people,avg].forEach(function(s){s.addEventListener('input',upd2);});
    upd2();
  }

  onScroll();
  var y=d.querySelector('[data-year]'); if(y) y.textContent=new Date().getFullYear();
})();
