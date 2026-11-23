/* Gallery, songs, and videos for the homepage. */
const ART = [["the-shining","The Shining: Heeere's Munchkin!","horror","Overlook Hotel tribute"],["korea-1","Breakfast Around the World: South Korea","comics","Day 8 · page 1"],["scuba","Deep Dive with Munchkin","munchkin","Good-night adventure series"],["alien","In Space No One Can Hear You Meow","horror","Alien (1979) tribute poster"],["the-ring","The Ring: Seven Days, Nine Lives","horror","J-horror tribute"],["starship","Starship Munchkin","munchkin","Launch-day trend art"],["resident-evil","Resident Evil: Nine Lives of the Dead","horror","Survival-horror fan poster"],["dracula","Dracula: Fangs for the Night-Meows","horror","Gothic classic"],["creative-mode","Full Creative Mode","characters","Signature chibi character"],["friday13","Friday the 13th: Nine Lives","horror","Camp Crystal Lake, cat edition"],["jaws","Jaws: We're Gonna Need a Bigger Track","horror","Jaws x Mini 4WD crossover"],["pit-crew","Munchkin Pit Crew: Tune-Up","comics","4-panel comic"],["bay-area-boy","Bay Area Boy","covers","Single cover art"],["pet-sematary","Pet Sematary: Sometimes Dead Is Purr-ter","horror","Stephen King tribute"],["caturday","Caturday","munchkin","Munchkin and friends"],["childs-play","Child's Play: Meow's Your Friend","horror","Killer-doll classic"],["different-light-art","A Different Kind of Light","covers","Charity single key art"],["japan-cup","Good Morning! Japan Cup Breakfast","comics","Manga-style daily comic"],["mind-blown","Mind = Blown","characters","Working with AI collaborators"],["cuddle","Best Friends","munchkin","Kyle and Munchkin"],["bay-area-boy-club","Bay Area Boy (club cover)","covers","Alternate cover"],["pit-crew-2","Munchkin Pit Crew: Day 2","comics","Mini 4WD comic strip"],["neon-studio","Neon Studio","characters","Chibi studio series"],["autumn","Autumn Portrait","munchkin","Anime-style portrait"],["footprints-cover","足跡が途切れる場所でも","covers","Memorial song cover"],["england","Breakfast Around the World: England","comics","Manga-style daily comic"],["korea-2","Breakfast Around the World: South Korea (p.2)","comics","Day 8 · page 2"],["japan-cup-poster","Japan Cup Breakfast: Start Your Engines","munchkin","Movie-poster style"],["turkey","Breakfast Around the World: Turkey","comics","Day 5 · manga-style comic"],["france-1","Breakfast Around the World: France (p.1)","comics","Day 6 · page 1"],["france-2","Breakfast Around the World: France (p.2)","comics","Day 6 · page 2"],["chibi-sticker","Chibi Kyle Sticker","characters","Character sticker design"],["india-1","Breakfast Around the World: India (p.1)","comics","Day 7 · page 1"],["india-2","Breakfast Around the World: India (p.2)","comics","Day 7 · page 2"],["england-2","Breakfast Around the World: England (p.2)","comics","Day 4 · page 2"],["mexico","Breakfast Around the World: Mexico","comics","Day 3 · manga-style comic"],["japan-cup-2","Japan Cup Breakfast Grand Prix (p.2)","comics","Manga-style daily comic"],["pit-crew-2b","Munchkin Pit Crew: Day 2 (p.2)","comics","Mini 4WD comic strip"]];
const CATS = [["all","All"],["horror","Horror Tributes"],["munchkin","Munchkin"],["comics","Comics"],["covers","Cover Art"],["characters","Characters"]];
const SONGS = [["weight-she-carries","THE WEIGHT SHE CARRIES","彼女が背負うもの","Japanese female-vocal metalcore about the invisible pain women carry every month. Has a video.","4327924f-189f-4be5-8a09-c95d8c919df1",["Metalcore","日本語","Video"],["jp","metal"]],["footprints","足跡が途切れる場所でも","Even Where the Footprints End","A Japanese post-hardcore ballad in memory of Kyle's late dog Buttons.","47bd3b5f-7fa6-4c32-b035-b2d88f10e56e",["Metalcore","日本語"],["jp","metal","life"]],["beyond-the-stars","Beyond the Stars","星の向こうへ","Atmospheric electronic metalcore about an astronaut calling home.","2c699a9a-bf3e-402a-9207-6ca25650f03d",["Metalcore","日本語","Video"],["jp","metal"]],["silent-scream","Silent Scream","Shadows of Stone","Jagged industrial hardstyle with dual heavy drops.","7843e4dc-d790-4cbc-8cb7-adc7c4ce708a",["Hardstyle","Video"],["album","edm"],"poster/silent-scream"],["forgotten-ones","The Forgotten Ones","忘れられた人々","A Japanese metalcore ballad for the elderly people the world walks past.","95e26a2e-838e-4a6c-9d33-e89000c6788a",["Metalcore","日本語","Video"],["jp","metal"]],["mayhem","Mayhem on the Peninsula","Battlefield metalcore","Relentless double-kick metalcore with radio chatter and explosions.","13887b34-bf14-4fd6-af62-7240b66ee22f",["Metalcore","Video"],["metal","gaming"]],["requiem","Requiem for the Dead","Resident Evil fan song","Industrial metal with a horror orchestra, written for Resident Evil Requiem.","5e11cdf3-b6b1-4333-ade4-5c02e3f94af0",["Industrial metal","Horror"],["metal","gaming","horror"]],["boogie-man","Boogie Man","Horror","A children's horror waltz: detuned music box and pounding piano.","60feab2c-52fb-42de-82fb-d6f4c7cb5c86",["Horror","Orchestral"],["horror"]],["letter-front","前線からの手紙","Letter from the Front","A soldier's letter home to his little brother, in Japanese deathcore.","661ee057-bc6a-4aad-9ab1-f4f0594985c3",["Deathcore","日本語","Video"],["jp","metal"]],["eternal-voice","Eternal Voice","Shadows of Stone","Dark hardstyle with ethereal, otherworldly vocals.","86d863dd-3956-4223-8911-f3a0c83987e2",["Hardstyle","Lyric video"],["album","edm"],"poster/eternal-voice"],["son-to-father","Son To Father Legacy","For my dad","Bay Area thrash for Kyle's dad, written in the style of Testament.","6c2168b1-70ff-4117-ae10-acd0bf44f1f5",["Thrash metal"],["metal","life"]],["rip-and-stream","Rip and Stream","DOOM stream anthem","Fast thrash metal written for a DOOM livestream.","80be5c66-0a46-4d35-acf9-3e98ed898fb0",["Thrash metal","Gaming"],["metal","gaming"]],["f-the-rescue","F**k The Rescue","Delivery-driver anthem","Brutal hardcore about Amazon delivery: 190 stops, 400 packages, and one more rescue.","8f6375dd-7e43-49e6-bbf1-c253d28631d0",["Hardcore","Explicit"],["metal","life"]],["darkness-inside","Darkness Inside (Intro)","Shadows of Stone, track 1","Opens a 15-track cinematic techno-hardstyle concept album.","17fe4f71-5ced-4385-971d-3211e7e2ac02",["Hardstyle","Concept album"],["album","edm"]],["good-night-children","Good Night, Children of the World","Nursery x metal","A sweet lullaby that turns into extreme metal screams.","25355328-7250-4a0e-8b81-815b5e132a30",["Experimental","Metal"],["metal","horror"]],["zero-viewers","ZERO VIEWERS","視聴者ゼロ","Bilingual hardstyle about streaming into the void.","2305492e-e317-41d5-922d-dc66a6d4f63f",["Hardstyle","日本語 / EN"],["jp","edm","gaming"]],["mini4wd-friends","Mini 4WD Friends","ミニ四駆","Bilingual racing-game electropop for Mini 4WD fans.","6ff49468-9a69-4c68-8d70-5bc31121e2e2",["Electropop","日本語 / EN"],["jp","edm","gaming"]],["tigers-roar","Tigers Roar Through the Night","阪神タイガース","A Japanese rock and synthwave chant for the Hanshin Tigers.","e143b275-d84c-4980-a7d6-d66320e06445",["Rock","日本語"],["jp","edm"]],["universe-war","Universe War","Human vs Alien","Gothic industrial rock: a hypnotic war anthem for humanity.","3a126b69-e5d0-4e52-9ed2-a7878a25dd49",["Industrial rock"],["metal"]],["open-beta","Open Beta Slaughter","Call of Duty beta","Thrash and metalcore about streaming the CoD open beta.","fefe96b0-cabd-4b11-b851-7f67e0e5d9c6",["Thrash","Metalcore"],["metal","gaming"]],["bedtime-apocalypse","Bedtime Apocalypse","Parenting metalcore","Comedy metalcore about bedtime with a toddler: raise the sippy cup!","fec0fd4c-014f-44bc-94be-9198082aebf1",["Metalcore","Comedy"],["metal","life"]],["unicorn-charge","Hiro's Unicorn Charge","For my son","Synthwave monster-truck racing anthem made for Kyle's son.","7f691770-f071-4c45-b7a0-cf39df4aa9c2",["Synthwave"],["edm","life"]],["pine-open-sky","Pine And Open Sky","Camping song","High-energy country-techno about camping trips.","cf2fa1ef-ff75-43e4-9fdb-02db3b68428f",["Country","Techno"],["edm","life"]],["black-lilies","Black Lilies Blooming","Thank you, X","Indie-pop thank-you to everyone who supports Kyle on X.","def7f421-c189-458a-911d-b7cb9c54b226",["Indie pop"],["life"]],["cat-sniff","Cat SniFF","I LOVE CATS","Silly surf-punk shout-along for cat people.","fe7d84f2-0fa4-4dc7-b806-b7715a7db1a6",["Surf punk","Comedy"],["life"]],["beyond-the-stone","Beyond the Stone","Shadows of Stone","Hopeful techno-hardstyle: light leaking through the cracks.","4a160b08-2b22-4ac9-889d-7378673c6da0",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["rough-with-the-wolves","Rough With the Wolves","Shadows of Stone","Heavy hardstyle about turning to run beside your fears.","0edd12da-235a-4fab-a3f9-7abdc8594807",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["pandemonium","Pandemonium","Shadows of Stone","Raw hardstyle with extreme distorted kicks: everything breaks loose.","4c3aebea-c06e-4f44-9221-74f39744fb47",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["state-of-stone","State of Stone","Shadows of Stone","Calm, grounded techno-hardstyle about learning to carry the weight.","412b7ea7-e03c-4936-bd0b-1459174c7503",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["beat-the-shadow","Beat the Shadow","Shadows of Stone","Hardstyle fight song: face the shadow down, even if it breaks your hands.","aa2e2a4c-bf4f-4a9f-a61e-4ac7b5a0583e",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["deepest-wave","Deepest Wave","Shadows of Stone","Melodic techno-hardstyle: the wave that breaks the stone open.","d46dc7f1-d9a4-4f88-bb79-f5b4f42c0bc3",["Hardstyle"],["album","edm"],"covers/shadows-of-stone"],["the-stone-stays","The Stone Stays (Outro)","Shadows of Stone, outro","The album closer: “I carry what remains, and I keep moving.”","8eacf5dd-8c54-4479-97e3-bb9f29fa3011",["Hardstyle","Outro"],["album","edm"],"covers/shadows-of-stone"]];
const SCATS = [["all","All"],["album","Shadows of Stone"],["jp","日本語 Japanese"],["metal","Metal"],["edm","Hardstyle & Electronic"],["gaming","Gaming"],["life","Life & Family"],["horror","Horror"]];
const SHOW = 12;
const VIDS = [["weight-she-carries","THE WEIGHT SHE CARRIES 彼女が背負うもの","Japanese metalcore video","4327924f-189f-4be5-8a09-c95d8c919df1","2114880163540602990"],["world-we-left-behind","The World We Left Behind 僕たちが残した世界","Environmental anime video",null,"2114295594676318247"],["different-light","A Different Kind of Light 違う光","Charity single video","025d9200-f3dc-4bb0-976a-91af5b84df49"],["price-tribute","Captain John Price Tribute","Call of Duty fan tribute with an original score (full 35 s)",null,"2112480433602802019"],["beyond-the-stars","Beyond the Stars","Anime sci-fi video","2c699a9a-bf3e-402a-9207-6ca25650f03d"],["eternal-voice","Eternal Voice","Shadows of Stone lyric video","86d863dd-3956-4223-8911-f3a0c83987e2","2111762165409718341"],["tamiya-ad","Tamiya Delivery 「押しても負けない」","Japanese TV-commercial comedy parody (full 30 s)",null],["bay-area-boy","Bay Area Boy","Club anthem video",null],["forgotten-ones","The Forgotten Ones 忘れられた人々","Anime drama video","95e26a2e-838e-4a6c-9d33-e89000c6788a"],["letter-front","前線からの手紙","War-story video","661ee057-bc6a-4aad-9ab1-f4f0594985c3"],["footprints","足跡が途切れる場所でも","Memorial video for Buttons","47bd3b5f-7fa6-4c32-b035-b2d88f10e56e"],["silent-scream","Silent Scream","Lyric video","7843e4dc-d790-4cbc-8cb7-adc7c4ce708a"],["mayhem","Mayhem on the Peninsula","Cinematic war video","13887b34-bf14-4fd6-af62-7240b66ee22f"]];
const WORK = [["bots-lineup","Meet the Team: My AI Bots","10 AI bots that help make the videos, art, and daily posts",null,"2113209664775356663"],["creative-bot","Creative Bot: The Hub","Animated map of how the bots connect",null],["stream-graphics","Stream Overlay Pack","Welcome, Live Now, Be Right Back, and Thank You screens for @HellaBayArea streams",null]];
const BOARDS = [["tamiya-board","Tamiya Delivery: full commercial storyboard","Storyboard",1],["ta1","Rain or wind… (frame 1)","Tamiya ad storyboard"],["ta2","The push (frame 2)","Tamiya ad storyboard"],["ta3","The argument (frame 3)","Tamiya ad storyboard"],["ta4","Tamiya power (frame 4)","Tamiya ad storyboard"],["ta5","The rescue (frame 5)","Tamiya ad storyboard"],["ta6","End card (frame 6)","Tamiya ad storyboard"],["light-board","A Different Kind of Light: video storyboard","Storyboard",1],["bab-board","Bay Area Boy: video storyboard","Storyboard",1],["weight-board","The Weight She Carries: video storyboard","Storyboard",1],["earth-board","The World We Left Behind: video storyboard","Storyboard",1],["stars-board","Beyond the Stars: video storyboard","Storyboard",1],["elder-board","The Forgotten Ones: video storyboard","Storyboard",1],["letter-board","前線からの手紙 Letter from the Front: storyboard","Storyboard",1]];
const AKARI = [
  {slug:'akari-character-sheet', title:'Akari 明里: character reference', cap:'Turnaround, expressions, outfits, details', src:'assets/akari/akari-character-sheet.jpg'},
  {slug:'akari-outfits', title:'Akari: outfit styles', cap:'Gothic Cyberpunk, Tokyo Streetwear, Cyberpunk Soldier, Fusion', src:'assets/akari/akari-outfits.jpg'},
  {slug:'akari-angel-demon', title:'Akari: Angel and Demon', cap:'Two winged forms, dark and light', src:'assets/akari/akari-angel-demon.jpg'}
];
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s).replace(/&/g,'&amp;').replace(/"/g,'&quot;').replace(/</g,'&lt;');

let current = [];
let artAll = false, artCat = 'all';
const ART_SHOW = 10;
function renderGallery(cat) {
  artCat = cat;
  const g = $('#gallery');
  g.innerHTML = '';
  current = ART.filter(a => cat === 'all' || a[2] === cat).map(a => ({slug:a[0], title:a[1], cap:a[3]}));
  const lim = (cat === 'all' && !artAll) ? ART_SHOW : current.length;
  const mb = $('#art-more');
  mb.parentNode.style.display = lim < current.length ? '' : 'none';
  mb.textContent = 'Show all ' + current.length + ' images';
  current.slice(0, lim).forEach((a, i) => {
    const f = document.createElement('figure');
    f.className = 'tile';
    f.tabIndex = 0;
    f.innerHTML = '<img src="assets/thumb/' + a.slug + '.webp" alt="' + esc(a.title) + '" loading="lazy" decoding="async"><figcaption>' + esc(a.title) + '<span>' + esc(a.cap) + '</span></figcaption>';
    f.onclick = () => openLb(current, i);
    f.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(current, i); } };
    g.appendChild(f);
  });
}
const fl = $('#filters');
CATS.forEach(([k, l], i) => {
  const b = document.createElement('button');
  b.type = 'button';
  b.textContent = l;
  b.setAttribute('aria-pressed', i ? 'false' : 'true');
  if (!i) b.className = 'on';
  b.onclick = () => {
    fl.querySelectorAll('button').forEach(x => { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
    b.classList.add('on');
    b.setAttribute('aria-pressed', 'true');
    renderGallery(k);
  };
  fl.appendChild(b);
});
renderGallery('all');
$('#art-more').onclick = () => { artAll = true; renderGallery(artCat); };

const play = '<svg width="16" height="16" viewBox="0 0 24 24" fill="#000" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>';
let songAll = false, songCat = 'all';
function renderSongs() {
  const list = SONGS.filter(s => songCat === 'all' || s[6].includes(songCat));
  $('#songs').innerHTML = list.map((s, k) => {
    const cover = s[7] || ('covers/' + s[0]);
    const tags = s[5].map(t => '<i class="' + (/日本語/.test(t) ? 'jpt' : '') + '">' + esc(t) + '</i>').join('');
    return '<a class="song' + (songCat === 'all' && !songAll && k >= SHOW ? ' hide' : '') + '" href="https://suno.com/song/' + s[4] + '" target="_blank" rel="noopener noreferrer">' +
      '<div class="art"><img src="assets/' + cover + '.webp" alt="' + esc(s[1]) + ' cover" loading="lazy" decoding="async" width="600" height="600"><span class="play">' + play + '</span></div>' +
      '<div class="meta"><h3>' + esc(s[1]) + '</h3><p class="jp">' + esc(s[2]) + '</p><p>' + esc(s[3]) + '</p><div class="tags">' + tags + '</div></div></a>';
  }).join('');
  $('#song-count').textContent = list.length + (songCat === 'all' ? ' songs featured here, plus the charity single above' : ' songs');
  const b = $('#song-more');
  const more = songCat === 'all' && !songAll && list.length > SHOW;
  b.style.display = more ? '' : 'none';
  b.textContent = 'Show all ' + list.length + ' songs';
}
const sf = $('#song-filters');
SCATS.forEach(([k, l], i) => {
  const b = document.createElement('button');
  b.type = 'button';
  b.textContent = l;
  b.setAttribute('aria-pressed', i ? 'false' : 'true');
  if (!i) b.className = 'on';
  b.onclick = () => {
    sf.querySelectorAll('button').forEach(x => { x.classList.remove('on'); x.setAttribute('aria-pressed', 'false'); });
    b.classList.add('on');
    b.setAttribute('aria-pressed', 'true');
    songCat = k;
    renderSongs();
  };
  sf.appendChild(b);
});
$('#song-more').onclick = () => { songAll = true; renderSongs(); };
renderSongs();

function vcard(v) {
  const bits = [esc(v[2])];
  if (v[3]) bits.push('<a href="https://suno.com/song/' + v[3] + '" target="_blank" rel="noopener noreferrer">Song on Suno</a>');
  if (v[4]) bits.push('<a href="https://x.com/HellaBayArea/status/' + v[4] + '" target="_blank" rel="noopener noreferrer">Post on X</a>');
  return '<article class="vcard"><video controls preload="none" playsinline data-poster="assets/poster/' + v[0] + '.webp" src="assets/video/' + v[0] + '.mp4" aria-label="' + esc(v[1]) + '"></video><div class="meta"><h3>' + esc(v[1]) + '</h3><p>' + bits.join(' · ') + '</p></div></article>';
}
$('#videos-grid').innerHTML = VIDS.map(vcard).join('');
$('#work-grid').innerHTML = WORK.map(vcard).join('');

const bItems = BOARDS.map(b => ({slug:b[0], title:b[1], cap:b[2]}));
const boards = $('#boards');
BOARDS.forEach((b, i) => {
  const f = document.createElement('figure');
  f.className = 'tile' + (b[3] ? ' wide' : '');
  f.tabIndex = 0;
  f.innerHTML = '<img src="assets/thumb/' + b[0] + '.webp" alt="' + esc(b[1]) + '" loading="lazy" decoding="async"><figcaption>' + esc(b[1]) + '<span>' + esc(b[2]) + '</span></figcaption>';
  f.onclick = () => openLb(bItems, i);
  f.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(bItems, i); } };
  boards.appendChild(f);
});

AKARI.forEach((a, i) => {
  const f = document.createElement('figure');
  f.className = 'tile';
  f.tabIndex = 0;
  f.innerHTML = '<img src="assets/akari/' + a.slug + '-thumb.jpg" alt="' + esc(a.title) + '" loading="lazy" decoding="async" width="800" height="533"><figcaption>' + esc(a.title) + '<span>' + esc(a.cap) + '</span></figcaption>';
  f.onclick = () => openLb(AKARI, i);
  f.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLb(AKARI, i); } };
  $('#akari-sheets').appendChild(f);
});

let lbSet = [], lbI = 0, lastFocus = null;
const lb = $('#lb');
function show() {
  const a = lbSet[lbI];
  const img = $('#lb-img');
  img.src = a.src || ('assets/img/' + a.slug + '.webp');
  img.alt = a.title;
  $('#lb-cap').innerHTML = esc(a.title) + '<span>' + esc(a.cap) + ' · ' + (lbI + 1) + ' / ' + lbSet.length + '</span>';
}
function openLb(set, i) {
  lastFocus = document.activeElement;
  lbSet = set;
  lbI = i;
  show();
  lb.classList.add('open');
  document.body.style.overflow = 'hidden';
  lb.querySelector('.x').focus();
}
function closeLb() {
  lb.classList.remove('open');
  document.body.style.overflow = '';
  if (lastFocus && lastFocus.focus) lastFocus.focus();
}
function step(d) { lbI = (lbI + d + lbSet.length) % lbSet.length; show(); }
lb.querySelector('.x').onclick = closeLb;
lb.querySelector('.prev').onclick = (e) => { e.stopPropagation(); step(-1); };
lb.querySelector('.next').onclick = (e) => { e.stopPropagation(); step(1); };
lb.onclick = (e) => { if (e.target === lb) closeLb(); };
document.addEventListener('keydown', (e) => {
  if (!lb.classList.contains('open')) return;
  if (e.key === 'Escape') closeLb();
  if (e.key === 'ArrowLeft') step(-1);
  if (e.key === 'ArrowRight') step(1);
});
let tx = 0;
lb.addEventListener('touchstart', (e) => { tx = e.touches[0].clientX; }, {passive:true});
lb.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].clientX - tx;
  if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
});
if (window.studioRefresh) window.studioRefresh(document);
