(function(e){function t(t){for(var a,s,o=t[0],l=t[1],c=t[2],u=0,p=[];u<o.length;u++)s=o[u],Object.prototype.hasOwnProperty.call(i,s)&&i[s]&&p.push(i[s][0]),i[s]=0;for(a in l)Object.prototype.hasOwnProperty.call(l,a)&&(e[a]=l[a]);h&&h(t);while(p.length)p.shift()();return r.push.apply(r,c||[]),n()}function n(){for(var e,t=0;t<r.length;t++){for(var n=r[t],a=!0,s=1;s<n.length;s++){var l=n[s];0!==i[l]&&(a=!1)}a&&(r.splice(t--,1),e=o(o.s=n[0]))}return e}var a={},i={app:0},r=[];function s(e){return o.p+"js/"+({}[e]||e)+"."+{"chunk-2d22d746":"e6126094"}[e]+".js"}function o(t){if(a[t])return a[t].exports;var n=a[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,o),n.l=!0,n.exports}o.e=function(e){var t=[],n=i[e];if(0!==n)if(n)t.push(n[2]);else{var a=new Promise((function(t,a){n=i[e]=[t,a]}));t.push(n[2]=a);var r,l=document.createElement("script");l.charset="utf-8",l.timeout=120,o.nc&&l.setAttribute("nonce",o.nc),l.src=s(e);var c=new Error;r=function(t){l.onerror=l.onload=null,clearTimeout(u);var n=i[e];if(0!==n){if(n){var a=t&&("load"===t.type?"missing":t.type),r=t&&t.target&&t.target.src;c.message="Loading chunk "+e+" failed.\n("+a+": "+r+")",c.name="ChunkLoadError",c.type=a,c.request=r,n[1](c)}i[e]=void 0}};var u=setTimeout((function(){r({type:"timeout",target:l})}),12e4);l.onerror=l.onload=r,document.head.appendChild(l)}return Promise.all(t)},o.m=e,o.c=a,o.d=function(e,t,n){o.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},o.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},o.t=function(e,t){if(1&t&&(e=o(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(o.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var a in e)o.d(n,a,function(t){return e[t]}.bind(null,a));return n},o.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return o.d(t,"a",t),t},o.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},o.p="/",o.oe=function(e){throw console.error(e),e};var l=window["webpackJsonp"]=window["webpackJsonp"]||[],c=l.push.bind(l);l.push=t,l=l.slice();for(var u=0;u<l.length;u++)t(l[u]);var h=c;r.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("cd49")},"034f":function(e,t,n){"use strict";n("85ec")},"1fd1":function(e,t,n){e.exports={spectro:"SingleElement_spectro_8bYiQ"}},"73d1":function(e,t,n){"use strict";var a=n("ebb4"),i=n.n(a);n.d(t,"default",(function(){return i.a}))},"85ec":function(e,t,n){},"97b9":function(e,t,n){e.exports={map:"SingleElementDetail_map_2KVO2",player:"SingleElementDetail_player_32IT7",image_container:"SingleElementDetail_image_container_3EQyS"}},"99ef":function(e,t,n){"use strict";var a=n("97b9"),i=n.n(a);n.d(t,"default",(function(){return i.a}))},"9a51":function(e,t,n){"use strict";var a=n("1fd1"),i=n.n(a);n.d(t,"default",(function(){return i.a}))},cd49:function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var a=n("2b0e"),i=function(){var e=this,t=e.$createElement,a=e._self._c||t;return a("div",{attrs:{id:"app"}},[a("img",{attrs:{src:n("cf05"),alt:"logo"}}),a("router-view"),a("router-link",{attrs:{to:"/"}},[e._v("Home")]),e._v(" - "),a("router-link",{attrs:{to:"/about"}},[e._v("About")])],1)},r=[],s=n("d4ec"),o=n("262e"),l=n("2caf"),c=n("9ab4"),u=n("60a3"),h=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(s["a"])(this,n),t.apply(this,arguments)}return n}(u["c"]);h=Object(c["a"])([Object(u["a"])({components:{}})],h);var p=h,d=p,f=(n("034f"),n("2877")),m=Object(f["a"])(d,i,r,!1,null,null,null),v=m.exports,_=n("e0ec"),g=n.n(_),b=(n("d3b7"),n("8c4f")),y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"home"},[n("h1",[e._v("New Spectrogram ?")]),n("NewSpectralForm",{on:{finished:e.update_list}}),n("h1",[e._v("Last spectrograms")]),n("SpectralAnalysisFlowList",{attrs:{"element-list":e.last_elements},on:{click:e.onClick}})],1)},O=[],w=n("bee2"),j=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ul",e._l(e.elementList,(function(t){return n("li",{key:t.id},["finished"==t.status?n("div",[n("SingleElement",{attrs:{element:t},on:{click:e.onClick}})],1):e._e()])})),0)},k=[],x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.element},[n("h2",{on:{click:function(t){return e.$emit("click",e.element)}}},[n("a",[e._v(e._s(e.element.title))])]),n("img",{attrs:{src:e.thumbnail_url(),alt:e.element.parameters.youtube_url}}),"finished"==e.element.status?n("div",[n("img",{class:e.$style.spectro,attrs:{src:e.first_tile_url()}})]):e._e()])},C=[],S=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.image_container},[n("canvas",{ref:"theCanvas",class:e.$style.spectrogram})])},$=[],E=(n("4ec9"),n("3ca3"),n("ddb0"),n("96cf"),n("1da1")),q=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(s["a"])(this,n),e=t.apply(this,arguments),e.images=new Array,e.loadingImages=new Map,e}return Object(w["a"])(n,[{key:"mounted",value:function(){var e=this.$refs.theCanvas;e.width=this.width,e.height=this.height,this.context=e.getContext("2d"),this.canvas=e,this.scrollTo(0)}},{key:"drawLineAt",value:function(e){this.context.moveTo(e,0),this.context.lineTo(e,this.canvas.height),this.context.strokeStyle="red",this.context.stroke()}},{key:"requestFullScreen",value:function(){var e=this,t=this.canvas.width,n=this.canvas.height;this.canvas.style.width=window.innerWidth+"px",this.canvas.style.height=window.innerHeight+"px",this.canvas.width=window.innerWidth,this.canvas.height=window.innerHeight,this.canvas.requestFullscreen({}),this.canvas.addEventListener("fullscreenchange",(function(){null==document.fullscreenElement&&(e.canvas.height=n,e.canvas.width=t,e.canvas.style.width=e.canvas.width+"px",e.canvas.style.height=e.canvas.height+"px")}))}},{key:"clear",value:function(){this.loadingImages.clear(),this.images=[]}},{key:"scrollTo",value:function(e){for(var t=this,n=Math.floor(e/this.tile_width),a=Math.floor((e+this.canvas.width)/this.tile_width),i=function(n){null!=t.images[n]||t.loadingImages.has(n)||(t.loadingImages.set(n,!1),t.getImage(n).then((function(a){t.images[n]=a,t.loadingImages.set(n,!0),t.scrollTo(e)})))},r=n;r<=a;++r)i(r);1==this.loadingImages.get(n)&&this.context.drawImage(this.images[n],0,this.tile_height-this.canvas.height,this.tile_width,this.canvas.height,-e%this.tile_width+this.canvas.width/2,0,this.tile_width,this.canvas.height);for(var s=1,o=n+1;o<=a;o++)this.loadingImages.get(o)&&this.context.drawImage(this.images[o],0,this.tile_height-this.canvas.height,this.tile_width,this.canvas.height,-e%this.tile_width+this.canvas.width/2+s*this.tile_width,0,this.tile_width,this.canvas.height),s++;this.drawLineAt(this.canvas.width/2)}},{key:"getImage",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(t){var n=this;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return e.abrupt("return",new Promise((function(e,a){var i=new Image;i.onload=function(){console.log("loaded tile ",t),e(i)},i.onerror=a,i.src=n.image_url_base+t+".png"})));case 1:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()}]),n}(u["c"]);Object(c["a"])([Object(u["b"])({required:!0})],q.prototype,"image_url_base",void 0),Object(c["a"])([Object(u["b"])({required:!0})],q.prototype,"width",void 0),Object(c["a"])([Object(u["b"])({required:!0})],q.prototype,"height",void 0),Object(c["a"])([Object(u["b"])({required:!0})],q.prototype,"tile_width",void 0),Object(c["a"])([Object(u["b"])({required:!0})],q.prototype,"tile_height",void 0),q=Object(c["a"])([Object(u["a"])({})],q);var P=q,T=P,L=n("73d1");function I(e){this["$style"]=L["default"].locals||L["default"]}var A=Object(f["a"])(T,S,$,!1,I,null,null),F=A.exports,z=n("9fab"),M=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(s["a"])(this,n),t.apply(this,arguments)}return Object(w["a"])(n,[{key:"thumbnail_url",value:function(){var e=z(this.element.parameters.youtube_url);return"https://img.youtube.com/vi/"+e+"/0.jpg"}},{key:"first_tile_url",value:function(){return this.make_url("http://kimsufi.luc-leonard.fr:5000/")+"/0.png"}},{key:"make_url",value:function(e){return e+"/tiles/"+this.element.id+"/"}}]),n}(u["c"]);Object(c["a"])([Object(u["b"])({required:!0})],M.prototype,"element",void 0),M=Object(c["a"])([Object(u["a"])({components:{ScrollingCanvas:F}})],M);var N=M,R=N,D=n("9a51");function H(e){this["$style"]=D["default"].locals||D["default"]}var J=Object(f["a"])(R,x,C,!1,H,null,null),U=J.exports,Q=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(s["a"])(this,n),t.apply(this,arguments)}return Object(w["a"])(n,[{key:"onClick",value:function(e){this.$emit("click",e)}}]),n}(u["c"]);Object(c["a"])([Object(u["b"])({required:!0})],Q.prototype,"elementList",void 0),Q=Object(c["a"])([Object(u["a"])({components:{SingleElement:U}})],Q);var W=Q,K=W,V=Object(f["a"])(K,j,k,!1,null,"bcd33830",null),X=V.exports,Y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"new-spectral-form"},[n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("URL")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.url,expression:"url"}],staticClass:"form-control",attrs:{type:"text"},domProps:{value:e.url},on:{input:function(t){t.target.composing||(e.url=t.target.value)}}})]),n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("frame size")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.frame_size,expression:"frame_size"}],staticClass:"form-control",domProps:{value:e.frame_size},on:{input:function(t){t.target.composing||(e.frame_size=t.target.value)}}})]),n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("overlap factor")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.overlap_factor,expression:"overlap_factor"}],staticClass:"form-control",domProps:{value:e.overlap_factor},on:{input:function(t){t.target.composing||(e.overlap_factor=t.target.value)}}})]),n("button",{on:{click:e.compute}},[e._v("COMPUTE")]),n("div",{staticClass:"well"},[e._v(e._s(e.compute_result))])])},B=[],G=n("bc3a"),Z=n.n(G),ee=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(s["a"])(this,n),e=t.apply(this,arguments),e.url="https://youtube.com/...",e.frame_size=12,e.overlap_factor=.8,e.compute_result="",e}return Object(w["a"])(n,[{key:"compute",value:function(){var e=this;console.log(this),Z.a.post("http://kimsufi.luc-leonard.fr:5000//requests/",{youtube_url:this.url,frame_size_power:this.frame_size,overlap_factor:this.overlap_factor}).then((function(t){e.current_result_id=t.data.id,e.poll_result()}))}},{key:"poll_result",value:function(){var e=this;setTimeout((function(){Z.a.get("http://kimsufi.luc-leonard.fr:5000//result/"+e.current_result_id).then((function(t){"finished"==t.data.status?e.$emit("finished",{new_result:t.data}):(e.compute_result=JSON.stringify(t.data),e.poll_result())}))}),150)}}]),n}(u["c"]);ee=Object(c["a"])([Object(u["a"])({components:{}})],ee);var te=ee,ne=te,ae=Object(f["a"])(ne,Y,B,!1,null,"69ae02a0",null),ie=ae.exports,re=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(s["a"])(this,n),e=t.apply(this,arguments),e.last_elements=[],e}return Object(w["a"])(n,[{key:"onClick",value:function(e){console.log(e),this.$router.push({name:"render",params:{result_id:e.id}})}},{key:"update_list",value:function(){var e=this;Z.a.get("http://kimsufi.luc-leonard.fr:5000//requests/").then((function(t){e.last_elements=t.data}))}},{key:"mounted",value:function(){this.update_list()}}]),n}(a["a"]);re=Object(c["a"])([Object(u["a"])({components:{SpectralAnalysisFlowList:X,NewSpectralForm:ie}})],re);var se=re,oe=se,le=Object(f["a"])(oe,y,O,!1,null,null,null),ce=le.exports,ue=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"home"},[n("h1",[e._v("Last spectrograms")]),e._v(" "),n("div",{on:{click:e.close}},[e._v("X")]),null!=e.element?n("SingleElementDetail",{attrs:{element:e.element}}):e._e()],1)},he=[],pe=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.element},[n("youtube",{ref:"youtube",class:e.$style.player,attrs:{"video-id":e.get_youtube_id(),"player-vars":e.players_vars},on:{paused:e.onPause,playing:e.playing}}),n("div",[e._v(e._s(e.fps))]),n("div",{on:{click:e.full_screen}},[e._v("[F U L L S C R E E N]")]),n("ScrollingCanvas",{ref:"spectro",staticClass:"image_container",attrs:{width:"2000",height:e.element.result.height/8,tile_width:e.element.result.tile_width,tile_height:e.element.result.height,image_url_base:e.make_url()}})],1)},de=[],fe=n("9fab"),me=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(s["a"])(this,n),e=t.apply(this,arguments),e.players_vars={origin:window.location},e.player_start_time=0,e.current_time_when_starting_to_play=0,e.current_position=0,e.pixel_per_sec=-1,e.is_playing=!1,e.last_called_time=0,e.fps=0,e}return Object(w["a"])(n,[{key:"mounted",value:function(){this.spectro=this.$refs.spectro,this.current_position=0,this.pixel_per_sec=this.element.result.width/this.element.duration*1e3,this.spectro.clear(),this.spectro.scrollTo(0)}},{key:"playing",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(){var t=this;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return console.log("play"),this.is_playing=!0,this.current_time_when_starting_to_play=performance.now(),e.next=5,this.player().getCurrentTime().then((function(e){t.player_start_time=1e3*e}));case 5:requestAnimationFrame(this.update_position);case 6:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}()},{key:"onPause",value:function(){console.log("pause"),this.is_playing=!1}},{key:"update_position",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(t){var n,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:n=(t-this.last_called_time)/1e3,this.last_called_time=t,this.fps=1/n,this.is_playing&&(a=t-this.current_time_when_starting_to_play,this.current_position=(a+this.player_start_time)/1e3,this.spectro.scrollTo(this.current_position*(this.pixel_per_sec/1e3)),requestAnimationFrame(this.update_position));case 4:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"full_screen",value:function(){this.spectro.requestFullScreen()}},{key:"get_youtube_id",value:function(){return fe(this.element.parameters.youtube_url)}},{key:"make_url",value:function(){return"http://kimsufi.luc-leonard.fr:5000//tiles/"+this.element.id+"/"}},{key:"player",value:function(){if(!this.youtube_player){var e=this.$refs.youtube;this.youtube_player=e.player}return this.youtube_player}}]),n}(u["c"]);Object(c["a"])([Object(u["b"])({required:!0})],me.prototype,"element",void 0),me=Object(c["a"])([Object(u["a"])({components:{ScrollingCanvas:F}})],me);var ve=me,_e=ve,ge=n("99ef");function be(e){this["$style"]=ge["default"].locals||ge["default"]}var ye=Object(f["a"])(_e,pe,de,!1,be,null,null),Oe=ye.exports,we=function(e){Object(o["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(s["a"])(this,n),e=t.apply(this,arguments),e.element=null,e}return Object(w["a"])(n,[{key:"close",value:function(){this.$router.push({path:"/"})}},{key:"mounted",value:function(){var e=this;console.log(this.$route),Z.a.get("http://kimsufi.luc-leonard.fr:5000//request/"+this.$route.params["result_id"]).then((function(t){e.element=t.data}))}}]),n}(a["a"]);we=Object(c["a"])([Object(u["a"])({components:{SingleElementDetail:Oe}})],we);var je=we,ke=je,xe=Object(f["a"])(ke,ue,he,!1,null,null,null),Ce=xe.exports;a["a"].use(b["a"]);var Se=[{path:"/",name:"Home",component:ce},{name:"render",path:"/render/:result_id",component:Ce},{path:"/about",name:"About",component:function(){return n.e("chunk-2d22d746").then(n.bind(null,"f820"))}}],$e=new b["a"]({mode:"history",base:"/",routes:Se}),Ee=$e;a["a"].config.productionTip=!1,a["a"].use(g.a);new a["a"]({render:function(e){return e(v)},router:Ee}).$mount("#app")},cf05:function(e,t,n){e.exports=n.p+"img/logo.82b9c7a5.png"},ebb4:function(e,t,n){e.exports={image_container:"ScrollingCanvas_image_container_eSwc5",spectrogram:"ScrollingCanvas_spectrogram_25_Et"}}});
//# sourceMappingURL=app.c4b75113.js.map