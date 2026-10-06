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

  /* video players: click-to-load. YouTube runs through the IFrame API so that
     YouTube's pause and end screens (suggested videos) are covered by our own screens */
  var ytQ=[], ytReady=false;
  function withYT(cb){
    if(window.YT&&window.YT.Player){cb();return;}
    ytQ.push(cb);
    if(ytReady) return; ytReady=true;
    var prev=window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady=function(){if(prev)prev();var q=ytQ;ytQ=[];q.forEach(function(f){f();});};
    var s=d.createElement('script'); s.src='https://www.youtube.com/iframe_api'; s.async=true; d.head.appendChild(s);
  }
  var orderHref=(function(){var a=$('a[rel~="sponsored"]');return a?a.href:'#';})();
  var canFS=!!(d.fullscreenEnabled||d.webkitFullscreenEnabled);
  function fsToggle(el){
    if(d.fullscreenElement||d.webkitFullscreenElement){(d.exitFullscreen||d.webkitExitFullscreen).call(d);}
    else {var r=el.requestFullscreen||el.webkitRequestFullscreen; if(r) r.call(el);}
  }
  /* Focused ("theater") video: the player lifts out of the page, zooms to the centre over a dim
     backdrop, gets a close button, and turns landscape on phones. It returns to its place when the
     video ends or the visitor closes it. */
  var mqRotate=window.matchMedia('(orientation: portrait) and (max-width: 640px)');
  var coarse=window.matchMedia('(pointer: coarse)').matches;
  var openTheater=null;
  d.addEventListener('keydown',function(e){if(e.key==='Escape'&&openTheater) openTheater(true);});
  function bindPlayer(p){
    if(p.bvBound) return; p.bvBound=true;
    var yt=p.getAttribute('data-yt'), title=p.getAttribute('data-title')||'Video', more=p.getAttribute('data-more'), player=null, media=null, T=null, endL=null;
    function layer(cls,html){var l=d.createElement('div');l.className='vlayer '+cls;l.innerHTML=html;l.hidden=true;p.appendChild(l);return l;}
    function enterTheater(){
      var r=p.getBoundingClientRect();
      var sp=d.createElement('div'); sp.className='pspacer'; sp.style.height=r.height+'px'; p.parentNode.insertBefore(sp,p);
      var th=d.createElement('div'); th.className='vtheater'; th.setAttribute('role','dialog'); th.setAttribute('aria-modal','true'); th.setAttribute('aria-label',title);
      th.innerHTML='<div class="vback"></div><button type="button" class="vclose" aria-label="Close video"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button><div class="vbox"><div class="vlid"><i class="vcam" aria-hidden="true"></i><div class="vscr"></div></div><div class="vbase" aria-hidden="true"><i></i></div></div>';
      var box=th.querySelector('.vscr'); box.insertBefore(p,box.firstChild);
      if(canFS&&!coarse){var fb=d.createElement('button');fb.type='button';fb.className='vfs';fb.setAttribute('aria-label','Full screen');fb.innerHTML='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/></svg>';fb.addEventListener('click',function(e){e.stopPropagation();th.classList.add('ufs');fsToggle(th);});th.appendChild(fb);}
      d.body.appendChild(th); root.classList.add('vt-open');
      requestAnimationFrame(function(){th.classList.add('on');});
      th.querySelector('.vback').addEventListener('click',function(){closeT(true);});
      th.querySelector('.vclose').addEventListener('click',function(e){e.stopPropagation();closeT(true);});
      T={th:th,sp:sp,back:d.activeElement,fs:false,top:r.top,y:window.scrollY};
      openTheater=closeT;
      setTimeout(function(){var c=th.querySelector('.vclose');if(c)c.focus({preventScroll:true});},60);
      /* phones: try real full screen + landscape (Android); otherwise CSS turns the video sideways */
      if(coarse&&mqRotate.matches&&th.requestFullscreen&&screen.orientation&&screen.orientation.lock){
        th.requestFullscreen({navigationUI:'hide'}).then(function(){
          T&&(T.fs=true);
          return screen.orientation.lock('landscape').then(function(){th.classList.add('locked');setTimeout(function(){if(innerWidth<innerHeight) th.classList.remove('locked');},450);});
        }).catch(function(){if(d.fullscreenElement===th) d.exitFullscreen().catch(function(){}); if(T) T.fs=false;});
      }
    }
    function closeT(reset){
      if(!T) return;
      var t=T; T=null; openTheater=null;
      try{if(screen.orientation&&screen.orientation.unlock) screen.orientation.unlock();}catch(_){}
      if(d.fullscreenElement) d.exitFullscreen().catch(function(){});
      if(reset) reset_();
      t.sp.parentNode.insertBefore(p,t.sp); t.sp.remove();
      /* put the visitor back exactly where the video was: same spot on the page, same distance from the top of the screen */
      var htmlEl=d.documentElement, prevSB=htmlEl.style.scrollBehavior; htmlEl.style.scrollBehavior='auto';
      function backToVideo(){var dy=p.getBoundingClientRect().top-t.top; if(Math.abs(dy)>1) window.scrollTo(0,Math.max(0,window.scrollY+dy));}
      backToVideo();
      requestAnimationFrame(backToVideo);
      setTimeout(backToVideo,120); setTimeout(backToVideo,380);
      setTimeout(function(){backToVideo();htmlEl.style.scrollBehavior=prevSB;},700);
      t.th.classList.remove('on'); setTimeout(function(){t.th.remove();},260);
      root.classList.remove('vt-open');
      if(t.back&&t.back.focus) try{t.back.focus({preventScroll:true});}catch(_){}
    }
    d.addEventListener('fullscreenchange',function(){if(!d.fullscreenElement){var u=d.querySelector('.vtheater.ufs');if(u)u.classList.remove('ufs');}if(T&&T.fs&&!d.fullscreenElement){T.fs=false;closeT(true);}});
    function finished(){
      closeT(true);
      if(endL) endL.remove();
      endL=d.createElement('div'); endL.className='vlayer vend';
      endL.innerHTML='<div class="vend-in"><p class="vend-k">Thanks for watching</p><h3>Ready to get your card?</h3><div class="vend-b"><a class="btn btn-go btn-sm" href="'+orderHref+'" target="_blank" rel="sponsored noopener">Order your card</a><button type="button" class="btn btn-ghost btn-sm" data-replay>Watch again</button>'+(more?'<a class="btn btn-ghost btn-sm" href="'+more+'">Read the summary</a>':'')+'</div></div>';
      endL.addEventListener('click',function(e){e.stopPropagation();});
      endL.querySelector('[data-replay]').addEventListener('click',function(){endL.remove();endL=null;play();});
      p.appendChild(endL);
    }
    function play(){
      if(p.classList.contains('playing')) return;
      if(endL){endL.remove();endL=null;}
      enterTheater();
      p.classList.add('playing');
      p.removeAttribute('role'); p.removeAttribute('tabindex');
      var pause=layer('vpause','<button type="button" class="vresume" aria-label="Resume video"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12.5-7.5L7 4.5z" fill="currentColor"/></svg></button><span>Paused</span>');
      pause.addEventListener('click',function(e){e.stopPropagation();if(player) player.playVideo();});
      if(yt){
        var mount=d.createElement('div'); mount.className='ytmount'; p.insertBefore(mount,pause);
        withYT(function(){
          if(!p.classList.contains('playing')) return;
          player=new YT.Player(mount,{host:'https://www.youtube-nocookie.com',videoId:yt,width:'100%',height:'100%',
            playerVars:{autoplay:1,rel:0,iv_load_policy:3,playsinline:1,modestbranding:1,fs:0,disablekb:0,cc_load_policy:0,origin:location.origin},
            events:{
              onReady:function(e){try{e.target.getIframe().title=title;}catch(_){} e.target.playVideo();},
              onStateChange:function(e){var st=e.data; pause.hidden=(st!==2); if(st===0) finished();}
            }});
        });
      } else {
        var v=d.createElement('video'); media=v;
        v.src=p.getAttribute('data-src'); v.controls=true; v.playsInline=true; v.setAttribute('playsinline',''); v.setAttribute('webkit-playsinline',''); v.preload='auto'; v.setAttribute('title',title);
        v.setAttribute('controlsList','nodownload noremoteplayback'); v.disablePictureInPicture=false;
        var poster=p.querySelector('img'); if(poster) v.poster=poster.currentSrc||poster.src;
        v.addEventListener('ended',finished);
        p.insertBefore(v,pause); var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){});
      }
    }
    function reset_(){
      try{if(player&&player.destroy) player.destroy();}catch(_){}
      try{if(media){media.pause();media.removeAttribute('src');media.load();}}catch(_){}
      player=null; media=null;
      $$('video,iframe,.ytmount,.vpause',p).forEach(function(n){n.remove();});
      p.classList.remove('playing'); p.setAttribute('role','button'); p.setAttribute('tabindex','0');
    }
    p.addEventListener('click',function(){if(!p.classList.contains('playing')) play();});
    p.addEventListener('keydown',function(e){if(!p.classList.contains('playing')&&(e.key==='Enter'||e.key===' ')){e.preventDefault();play();}});
    p.bvReset=function(){ if(T) closeT(true); else if(p.classList.contains('playing')) reset_(); if(endL){endL.remove();endL=null;} };
  }
  $$('.player[data-src],.player[data-yt]').forEach(bindPlayer);

  /* tutorial tiles: become playable as soon as the MP4 exists in videos/tutorials/ */
  $$('.player[data-wait]').forEach(function(p){
    var url=p.getAttribute('data-wait');
    if(!window.fetch) return;
    fetch(url,{method:'HEAD',cache:'no-store'}).then(function(r){
      if(!r.ok) return;
      p.setAttribute('data-src',url); p.classList.remove('soon'); p.classList.add('ready');
      p.setAttribute('role','button'); p.setAttribute('tabindex','0'); p.setAttribute('aria-label','Play: '+(p.getAttribute('data-title')||'tutorial'));
      var lb=$('.plabel',p); if(lb) lb.textContent='Watch now';
      bindPlayer(p);
    }).catch(function(){});
  });

  /* presentation playlist */
  var lib=$('.vlib');
  if(lib){
    var panels=$$('.vpanel',lib), btns=$$('.vitem',lib);
    function show(id,scroll){
      if(!$('#'+id,lib)) id=panels[0].id;
      panels.forEach(function(pn){var on=pn.id===id;if(!on){var pl=$('.player',pn);if(pl&&pl.bvReset)pl.bvReset();}pn.classList.toggle('off',!on);});
      btns.forEach(function(b){b.setAttribute('aria-current',b.getAttribute('data-show')===id?'true':'false');});
      if(scroll){var st=$('.vstage',lib);var y=st.getBoundingClientRect().top+window.scrollY-90;window.scrollTo({top:y,behavior:reduce?'auto':'smooth'});}
    }
    btns.forEach(function(b){b.addEventListener('click',function(){var id=b.getAttribute('data-show');show(id,window.innerWidth<861||$('.vstage',lib).getBoundingClientRect().top<0);try{history.replaceState(null,'','#'+id);}catch(_){}});});
    show((location.hash||'').slice(1)||panels[0].id,false);
    window.addEventListener('hashchange',function(){show(location.hash.slice(1),true);});
  }
  $$('[data-play]').forEach(function(a){a.addEventListener('click',function(e){var t=$(a.getAttribute('data-play'));if(!t)return;e.preventDefault();t.click();});});

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

  /* =====================================================================
     PROGRESSIVE PAGES: a page opens short (top sections plus a peek of the
     next one). Scrolling down opens the next section by itself; the Up next
     bar, the section navigator, links and find-in-page all open it too.
     ===================================================================== */
  (function(){
    var main=$('#main'); if(!main) return;
    var open=parseInt(main.getAttribute('data-open')||'2',10);
    var secs=$$(':scope > section',main).filter(function(s){return !s.classList.contains('pager-sec');});
    function titleOf(s){var t=s.getAttribute('data-title');if(t)return t;var h=$('h2',s);return h?h.textContent.replace(/\s+/g,' ').trim():'';}
    var rest=secs.slice(open), chapters=[];
    rest.forEach(function(s){var t=titleOf(s);if(t||!chapters.length)chapters.push({els:[s],title:t||'More'});else chapters[chapters.length-1].els.push(s);});
    var titled=secs.filter(function(s){return titleOf(s);});
    var isDash=d.body.classList.contains('is-dash');
    var done=0, busy=false, bar=null, lastY=window.scrollY, dirDown=true, cool=0, nav=null, items=[];
    var progressive=chapters.length>=2;

    if(progressive){
      chapters.forEach(function(c,i){c.els.forEach(function(el){if(i>0||el!==c.els[0]) el.setAttribute('hidden','until-found');});});
      chapters[0].els[0].classList.add('chap-peek');
      bar=d.createElement('div'); bar.className='upnext';
      bar.innerHTML='<button type="button" class="un-go" aria-label="Open the next section" title="Open this section"><span class="un-ring" aria-hidden="true"><svg viewBox="0 0 36 36"><circle class="bg" cx="18" cy="18" r="15.5"/><circle class="fg" cx="18" cy="18" r="15.5"/></svg><i></i></span><span class="un-tx"><small></small><b></b></span><span class="un-chev" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></span></button><button type="button" class="un-all">Show All</button>';
      placeBar();
      $('.un-go',bar).addEventListener('click',function(){revealNext(true);});
      $('.un-all',bar).addEventListener('click',function(){revealUpTo(chapters.length-1,true);});
      d.addEventListener('beforematch',function(e){var i=indexOf(e.target);if(i>=0) revealUpTo(i,false);},true);
      /* sections open only when the visitor asks: the Up next bar, Show all, the section navigator or a link */

    }

    function placeBar(){
      if(!bar) return;
      if(done>=chapters.length){bar.remove();bar=null;updateNav();return;}
      var c=chapters[done], anchorEl=c.els[0];
      anchorEl.parentNode.insertBefore(bar,anchorEl.nextSibling);
      $('small',bar).textContent='Tap to open, '+(done+1)+' of '+chapters.length;
      $('b',bar).textContent=c.title;
      bar.style.setProperty('--p',(done/chapters.length).toFixed(3));
      bar.classList.remove('un-pop'); void bar.offsetWidth; bar.classList.add('un-pop');
      updateNav();
    }
    function indexOf(el){for(var i=0;i<chapters.length;i++){for(var j=0;j<chapters[i].els.length;j++){if(chapters[i].els[j]===el||chapters[i].els[j].contains(el))return i;}}return -1;}
    function openChapter(i,animate){
      var c=chapters[i];
      c.els.forEach(function(el,k){
        el.removeAttribute('hidden');
        if(k===0&&el.classList.contains('chap-peek')&&animate&&!reduce){
          var from=el.getBoundingClientRect().height; el.style.maxHeight=from+'px'; el.classList.add('chap-opening'); el.classList.remove('chap-peek');
          requestAnimationFrame(function(){el.style.maxHeight=el.scrollHeight+'px';});
          setTimeout(function(){el.style.maxHeight='';el.classList.remove('chap-opening');},900);
        } else { el.classList.remove('chap-peek'); if(animate&&!reduce){el.classList.add('chap-in');setTimeout(function(){el.classList.remove('chap-in');},900);} }
      });
    }
    function peekNext(animate){
      if(done<chapters.length){var el=chapters[done].els[0];el.removeAttribute('hidden');el.classList.add('chap-peek');if(animate&&!reduce){el.classList.add('peek-in');setTimeout(function(){el.classList.remove('peek-in');},700);}}
    }
    function revealNext(user){
      if(!progressive||busy||done>=chapters.length) return;
      busy=true; cool=Date.now()+1100;
      openChapter(done,true); done++;
      peekNext(true); placeBar();
      setTimeout(function(){busy=false;},700);
    }
    function revealUpTo(i,animate){
      if(!progressive) return;
      while(done<=i&&done<chapters.length){openChapter(done,animate);done++;}
      peekNext(animate); placeBar();
    }
    function goTo(el){
      if(!el) return;
      var i=indexOf(el); if(i>=0&&i>=done) revealUpTo(i,false);
      setTimeout(function(){var y=el.getBoundingClientRect().top+window.scrollY-(isDash?120:90);window.scrollTo({top:y,behavior:reduce?'auto':'smooth'});},30);
    }
    /* links to a spot on this page */
    d.addEventListener('click',function(e){
      if(e.defaultPrevented) return; var a=e.target.closest&&e.target.closest('a[href*="#"]'); if(!a) return;
      var u; try{u=new URL(a.href,location.href);}catch(_){return;}
      if(u.pathname!==location.pathname||!u.hash||u.hash.length<2) return;
      var t=d.getElementById(decodeURIComponent(u.hash.slice(1))); if(!t||$('.vlib')) return;
      e.preventDefault(); goTo(t); try{history.replaceState(null,'',u.hash);}catch(_){}
    });
    if(location.hash.length>1){var t0=d.getElementById(decodeURIComponent(location.hash.slice(1)));if(t0&&indexOf(t0)>=0){revealUpTo(indexOf(t0),false);setTimeout(function(){goTo(t0);},120);}}

    /* section navigator */
    if(titled.length>=3){
      nav=d.createElement('nav'); nav.className=isDash?'secnav':'secrail'; nav.setAttribute('aria-label','Sections on this page');
      var html=isDash?'<button type="button" class="sn-toggle" aria-expanded="false"><span class="sn-k">On this page</span><b></b><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></button><div class="sn-list">':'<div class="sn-list">';
      titled.forEach(function(s,i){if(!s.id) s.id='s-'+(i+1); html+='<a class="sn-i" href="#'+s.id+'"><i></i><span>'+titleOf(s).replace(/</g,'&lt;')+'</span></a>';});
      nav.innerHTML=html+'</div>';
      if(isDash){var top2=$('.dtop');top2.parentNode.insertBefore(nav,top2.nextSibling);} else d.body.appendChild(nav);
      items=$$('.sn-i',nav);
      var tg=$('.sn-toggle',nav);
      if(tg) tg.addEventListener('click',function(){var o=nav.classList.toggle('open');tg.setAttribute('aria-expanded',o?'true':'false');});
      items.forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');if(tg)tg.setAttribute('aria-expanded','false');});});
      if('IntersectionObserver' in window){
        var cur=null;
        var sio=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){cur=e.target.id;mark();}});},{rootMargin:'-35% 0px -60% 0px'});
        titled.forEach(function(s){sio.observe(s);});
        function mark(){items.forEach(function(a){var on=a.getAttribute('href')==='#'+cur;a.classList.toggle('on',on);if(on&&tg)$('b',tg).textContent=a.textContent;});}
      }
      if(tg) $('b',tg).textContent='Jump to a section';
      updateNav();
    }
    function updateNav(){
      if(!items.length) return;
      items.forEach(function(a){var t=d.getElementById(a.getAttribute('href').slice(1));var i=indexOf(t);a.classList.toggle('locked',i>=0&&i>=done&&progressive);});
      if(!isDash&&nav){nav.classList.toggle('show',window.scrollY>innerHeight*.6);}
    }
    if(nav&&!isDash) window.addEventListener('scroll',function(){nav.classList.toggle('show',window.scrollY>innerHeight*.6);},{passive:true});
  })();

  /* card levels on phones: one level at a time with a level picker (like the video playlist) */
  (function(){
    var mq=window.matchMedia('(max-width: 640px)');
    $$('.tiers').forEach(function(box){
      var tiers=$$('.tier',box); if(tiers.length<2) return;
      var bar=d.createElement('div'); bar.className='tierpick'; bar.setAttribute('role','tablist'); bar.setAttribute('aria-label','Choose a card level');
      tiers.forEach(function(t,i){var n=$('.name',t);var pr=$('.price',t);var b=d.createElement('button');b.type='button';b.setAttribute('role','tab');b.className='tp '+(t.className.match(/\b(basic|prem|biz|gold)\b/)||['',''])[1];b.innerHTML='<b>'+(n?n.textContent:'Level')+'</b><small>'+(pr?pr.childNodes[0].textContent.trim():'')+'</small>';b.addEventListener('click',function(){pick(i,true);});bar.appendChild(b);});
      box.parentNode.insertBefore(bar,box);
      var cur=Math.max(0,tiers.findIndex(function(t){return t.classList.contains('pop');}));
      function pick(i,anim){cur=i;$$('.tp',bar).forEach(function(b,k){b.setAttribute('aria-selected',k===i?'true':'false');});
        tiers.forEach(function(t,k){var on=!mq.matches||k===i;t.classList.toggle('tp-off',!on);if(on&&anim&&mq.matches){t.classList.remove('tp-in');void t.offsetWidth;t.classList.add('tp-in');}});}
      pick(cur,false);
      (mq.addEventListener?mq.addEventListener('change',function(){pick(cur,false);}):mq.addListener(function(){pick(cur,false);}));
    });
  })();
  /* keep the back-to-top button off the Up next bar */
  (function(){var tb=$('.totop');if(!tb||!('IntersectionObserver' in window))return;
    var watch=new MutationObserver(function(){var u=$('.upnext');if(u&&!u.bvWatched){u.bvWatched=true;io2.observe(u);}});
    var io2=new IntersectionObserver(function(es){es.forEach(function(e){root.classList.toggle('un-vis',e.isIntersecting);});});
    var u0=$('.upnext');if(u0){u0.bvWatched=true;io2.observe(u0);}
    watch.observe(d.body,{childList:true,subtree:true});
  })();

  onScroll();
  var y=d.querySelector('[data-year]'); if(y) y.textContent=new Date().getFullYear();
})();
