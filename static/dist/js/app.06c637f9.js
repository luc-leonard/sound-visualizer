(function(e){function t(t){for(var r,o,s=t[0],l=t[1],u=t[2],c=0,h=[];c<s.length;c++)o=s[c],Object.prototype.hasOwnProperty.call(a,o)&&a[o]&&h.push(a[o][0]),a[o]=0;for(r in l)Object.prototype.hasOwnProperty.call(l,r)&&(e[r]=l[r]);p&&p(t);while(h.length)h.shift()();return i.push.apply(i,u||[]),n()}function n(){for(var e,t=0;t<i.length;t++){for(var n=i[t],r=!0,o=1;o<n.length;o++){var l=n[o];0!==a[l]&&(r=!1)}r&&(i.splice(t--,1),e=s(s.s=n[0]))}return e}var r={},a={app:0},i=[];function o(e){return s.p+"js/"+({}[e]||e)+"."+{"chunk-2d22d746":"e6126094"}[e]+".js"}function s(t){if(r[t])return r[t].exports;var n=r[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,s),n.l=!0,n.exports}s.e=function(e){var t=[],n=a[e];if(0!==n)if(n)t.push(n[2]);else{var r=new Promise((function(t,r){n=a[e]=[t,r]}));t.push(n[2]=r);var i,l=document.createElement("script");l.charset="utf-8",l.timeout=120,s.nc&&l.setAttribute("nonce",s.nc),l.src=o(e);var u=new Error;i=function(t){l.onerror=l.onload=null,clearTimeout(c);var n=a[e];if(0!==n){if(n){var r=t&&("load"===t.type?"missing":t.type),i=t&&t.target&&t.target.src;u.message="Loading chunk "+e+" failed.\n("+r+": "+i+")",u.name="ChunkLoadError",u.type=r,u.request=i,n[1](u)}a[e]=void 0}};var c=setTimeout((function(){i({type:"timeout",target:l})}),12e4);l.onerror=l.onload=i,document.head.appendChild(l)}return Promise.all(t)},s.m=e,s.c=r,s.d=function(e,t,n){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(s.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var r in e)s.d(n,r,function(t){return e[t]}.bind(null,r));return n},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/www/dist/",s.oe=function(e){throw console.error(e),e};var l=window["webpackJsonp"]=window["webpackJsonp"]||[],u=l.push.bind(l);l.push=t,l=l.slice();for(var c=0;c<l.length;c++)t(l[c]);var p=u;i.push([0,"chunk-vendors"]),n()})({0:function(e,t,n){e.exports=n("cd49")},"034f":function(e,t,n){"use strict";n("85ec")},"1fd1":function(e,t,n){e.exports={spectro:"SingleElement_spectro_8bYiQ"}},"73d1":function(e,t,n){"use strict";var r=n("ebb4"),a=n.n(r);n.d(t,"default",(function(){return a.a}))},"85ec":function(e,t,n){},"97b9":function(e,t,n){e.exports={map:"SingleElementDetail_map_2KVO2",player:"SingleElementDetail_player_32IT7",image_container:"SingleElementDetail_image_container_3EQyS"}},"99ef":function(e,t,n){"use strict";var r=n("97b9"),a=n.n(r);n.d(t,"default",(function(){return a.a}))},"9a51":function(e,t,n){"use strict";var r=n("1fd1"),a=n.n(r);n.d(t,"default",(function(){return a.a}))},cd49:function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var r=n("2b0e"),a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[r("img",{attrs:{src:n("cf05"),alt:"logo"}}),r("router-view"),r("router-link",{attrs:{to:"/"}},[e._v("Home")]),e._v(" - "),r("router-link",{attrs:{to:"/about"}},[e._v("About")])],1)},i=[],o=n("d4ec"),s=n("262e"),l=n("2caf"),u=n("9ab4"),c=n("60a3"),p=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(o["a"])(this,n),t.apply(this,arguments)}return n}(c["c"]);p=Object(u["a"])([Object(c["a"])({components:{}})],p);var h=p,m=h,d=(n("034f"),n("2877")),f=Object(d["a"])(m,a,i,!1,null,null,null),v=f.exports,_=n("e0ec"),g=n.n(_),b=(n("d3b7"),n("8c4f")),y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"home"},[n("h1",[e._v("New Spectrogram ?")]),n("NewSpectralForm",{on:{finished:e.update_list}}),n("h1",[e._v("Last spectrograms")]),n("SpectralAnalysisFlowList",{attrs:{"element-list":e.last_elements},on:{click:e.onClick}})],1)},O=[],j=n("bee2"),w=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ul",e._l(e.elementList,(function(t){return n("li",{key:t.id},["finished"==t.status?n("div",[n("SingleElement",{attrs:{element:t},on:{click:e.onClick}})],1):e._e()])})),0)},k=[],x=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.element},[n("h2",{on:{click:function(t){return e.$emit("click",e.element)}}},[n("a",[e._v(e._s(e.element.title))])]),n("img",{attrs:{src:e.thumbnail_url(),alt:e.element.parameters.youtube_url}}),"finished"==e.element.status?n("div",[n("img",{class:e.$style.spectro,attrs:{src:e.first_tile_url()}})]):e._e()])},C=[],$=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.image_container},[n("canvas",{ref:"theCanvas",class:e.$style.spectrogram})])},S=[],E=(n("4ec9"),n("3ca3"),n("ddb0"),n("96cf"),n("1da1")),P=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(o["a"])(this,n),e=t.apply(this,arguments),e.images=new Array,e.loadingImages=new Map,e}return Object(j["a"])(n,[{key:"mounted",value:function(){var e=this.$refs.theCanvas;e.width=this.width,e.height=this.height,this.context=e.getContext("2d"),this.scrollTo(0)}},{key:"drawLineAt",value:function(e){this.context.moveTo(e,0),this.context.lineTo(e,this.height),this.context.strokeStyle="red",this.context.stroke()}},{key:"clear",value:function(){this.loadingImages.clear(),this.images=[]}},{key:"scrollTo",value:function(e){for(var t=this,n=Math.floor(e/this.tile_width),r=Math.floor((e+this.context.canvas.width)/this.tile_width),a=function(n){null!=t.images[n]||t.loadingImages.has(n)||(t.loadingImages.set(n,!1),t.getImage(n).then((function(r){t.images[n]=r,t.loadingImages.set(n,!0),t.scrollTo(e)})))},i=n;i<=r;++i)a(i);1==this.loadingImages.get(n)&&this.context.drawImage(this.images[n],-e%this.tile_width+this.width/2,this.height-this.tile_height),this.drawLineAt(this.width/2)}},{key:"getImage",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(t){var n=this;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return console.log("loading tile",t),e.abrupt("return",new Promise((function(e,r){var a=new Image;a.onload=function(){console.log("loaded tile ",t),e(a)},a.onerror=r,a.src=n.image_url_base+t+".png"})));case 2:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}()}]),n}(c["c"]);Object(u["a"])([Object(c["b"])({required:!0})],P.prototype,"image_url_base",void 0),Object(u["a"])([Object(c["b"])({required:!0})],P.prototype,"width",void 0),Object(u["a"])([Object(c["b"])({required:!0})],P.prototype,"height",void 0),Object(u["a"])([Object(c["b"])({required:!0})],P.prototype,"tile_width",void 0),Object(u["a"])([Object(c["b"])({required:!0})],P.prototype,"tile_height",void 0),P=Object(u["a"])([Object(c["a"])({})],P);var T=P,q=T,z=n("73d1");function A(e){this["$style"]=z["default"].locals||z["default"]}var I=Object(d["a"])(q,$,S,!1,A,null,null),L=I.exports,M=n("9fab"),R=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(o["a"])(this,n),t.apply(this,arguments)}return Object(j["a"])(n,[{key:"thumbnail_url",value:function(){var e=M(this.element.parameters.youtube_url);return"https://img.youtube.com/vi/"+e+"/0.jpg"}},{key:"first_tile_url",value:function(){return this.make_url("https://sound-visualizer-staging.herokuapp.com/")+"/0.png"}},{key:"make_url",value:function(e){return e+"/tiles/"+this.element.id+"/"}}]),n}(c["c"]);Object(u["a"])([Object(c["b"])({required:!0})],R.prototype,"element",void 0),R=Object(u["a"])([Object(c["a"])({components:{ScrollingCanvas:L}})],R);var N=R,F=N,D=n("9a51");function U(e){this["$style"]=D["default"].locals||D["default"]}var J=Object(d["a"])(F,x,C,!1,U,null,null),H=J.exports,Q=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){return Object(o["a"])(this,n),t.apply(this,arguments)}return Object(j["a"])(n,[{key:"onClick",value:function(e){this.$emit("click",e)}}]),n}(c["c"]);Object(u["a"])([Object(c["b"])({required:!0})],Q.prototype,"elementList",void 0),Q=Object(u["a"])([Object(c["a"])({components:{SingleElement:H}})],Q);var B=Q,K=B,V=Object(d["a"])(K,w,k,!1,null,"bcd33830",null),X=V.exports,Y=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"new-spectral-form"},[n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("URL")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.url,expression:"url"}],staticClass:"form-control",attrs:{type:"text"},domProps:{value:e.url},on:{input:function(t){t.target.composing||(e.url=t.target.value)}}})]),n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("frame size")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.frame_size,expression:"frame_size"}],staticClass:"form-control",domProps:{value:e.frame_size},on:{input:function(t){t.target.composing||(e.frame_size=t.target.value)}}})]),n("div",{staticClass:"input-group"},[n("span",{staticClass:"input-group-addon",attrs:{id:"basic-addon1"}},[e._v("overlap factor")]),n("input",{directives:[{name:"model",rawName:"v-model",value:e.overlap_factor,expression:"overlap_factor"}],staticClass:"form-control",domProps:{value:e.overlap_factor},on:{input:function(t){t.target.composing||(e.overlap_factor=t.target.value)}}})]),n("button",{nativeOn:{click:function(t){return e.compute(t)}}},[e._v(" COMPUTE")]),n("div",{staticClass:"well"},[e._v(e._s(e.compute_result))])])},G=[],W=n("bc3a"),Z=n.n(W),ee=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(o["a"])(this,n),e=t.apply(this,arguments),e.url="https://youtube.com/...",e.frame_size=12,e.overlap_factor=.8,e.compute_result="",e}return Object(j["a"])(n,[{key:"compute",value:function(){var e=this;console.log(this),Z.a.post("https://sound-visualizer-staging.herokuapp.com//requests/",{youtube_url:this.url,frame_size_power:this.frame_size,overlap_factor:this.overlap_factor}).then((function(t){e.current_result_id=t.data.id,e.poll_result()}))}},{key:"poll_result",value:function(){var e=this;setTimeout((function(){Z.a.get(e.$data.API_BASE_URL+"/result/"+e.current_result_id).then((function(t){"finished"==t.data.status?e.$emit("finished",{new_result:t.data}):(e.compute_result=JSON.stringify(t.data),e.poll_result())}))}),150)}}]),n}(r["a"]),te=ee,ne=Object(d["a"])(te,Y,G,!1,null,"4889a6ba",null),re=ne.exports,ae=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(o["a"])(this,n),e=t.apply(this,arguments),e.last_elements=[],e}return Object(j["a"])(n,[{key:"onClick",value:function(e){console.log(e),this.$router.push({name:"render",params:{result_id:e.id}})}},{key:"update_list",value:function(){var e=this;Z.a.get("https://sound-visualizer-staging.herokuapp.com//requests/").then((function(t){e.last_elements=t.data}))}},{key:"mounted",value:function(){this.update_list()}}]),n}(r["a"]);ae=Object(u["a"])([Object(c["a"])({components:{SpectralAnalysisFlowList:X,NewSpectralForm:re}})],ae);var ie=ae,oe=ie,se=Object(d["a"])(oe,y,O,!1,null,null,null),le=se.exports,ue=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"home"},[n("h1",[e._v("Last spectrograms")]),e._v(" "),n("div",{on:{click:e.close}},[e._v("X")]),null!=e.element?n("SingleElementDetail",{attrs:{element:e.element}}):e._e()],1)},ce=[],pe=function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{class:e.$style.element},[n("youtube",{ref:"youtube",class:e.$style.player,attrs:{"video-id":e.get_youtube_id(),"player-vars":e.players_vars},on:{paused:e.onPause,playing:e.playing}}),n("div",[e._v(e._s(e.fps))]),n("ScrollingCanvas",{ref:"spectro",staticClass:"image_container",attrs:{width:"2000",height:e.element.result.height/4,tile_width:e.element.result.tile_width,tile_height:e.element.result.height,image_url_base:e.make_url()}})],1)},he=[],me=n("9fab"),de=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(o["a"])(this,n),e=t.apply(this,arguments),e.players_vars={origin:window.location},e.player_start_time=0,e.current_time_when_starting_to_play=0,e.current_position=0,e.pixel_per_sec=-1,e.is_playing=!1,e.last_called_time=0,e.fps=0,e}return Object(j["a"])(n,[{key:"onElementChanged",value:function(){console.log("element changed on ",this),this.spectro.image_url_base=this.make_url(),this.spectro.clear(),this.spectro.$forceUpdate(),this.spectro.scrollTo(0)}},{key:"mounted",value:function(){this.spectro=this.$refs.spectro,this.current_position=0,this.pixel_per_sec=this.element.result.width/this.element.duration*1e3,this.spectro.clear(),this.spectro.scrollTo(0)}},{key:"playing",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(){var t=this;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return console.log("play"),this.is_playing=!0,this.current_time_when_starting_to_play=performance.now(),e.next=5,this.player().getCurrentTime().then((function(e){t.player_start_time=1e3*e}));case 5:requestAnimationFrame(this.update_position);case 6:case"end":return e.stop()}}),e,this)})));function t(){return e.apply(this,arguments)}return t}()},{key:"onPause",value:function(){console.log("pause"),this.is_playing=!1}},{key:"update_position",value:function(){var e=Object(E["a"])(regeneratorRuntime.mark((function e(t){var n,r;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:n=(t-this.last_called_time)/1e3,this.last_called_time=t,this.fps=1/n,this.is_playing&&(r=t-this.current_time_when_starting_to_play,this.current_position=(r+this.player_start_time)/1e3,this.spectro.scrollTo(this.current_position*(this.pixel_per_sec/1e3)),requestAnimationFrame(this.update_position));case 4:case"end":return e.stop()}}),e,this)})));function t(t){return e.apply(this,arguments)}return t}()},{key:"get_youtube_id",value:function(){return me(this.element.parameters.youtube_url)}},{key:"make_url",value:function(){return"https://sound-visualizer-staging.herokuapp.com//tiles/"+this.element.id+"/"}},{key:"player",value:function(){if(!this.youtube_player){var e=this.$refs.youtube;this.youtube_player=e.player}return this.youtube_player}}]),n}(c["c"]);Object(u["a"])([Object(c["b"])({required:!0})],de.prototype,"element",void 0),Object(u["a"])([Object(c["d"])("element")],de.prototype,"onElementChanged",null),de=Object(u["a"])([Object(c["a"])({components:{ScrollingCanvas:L}})],de);var fe=de,ve=fe,_e=n("99ef");function ge(e){this["$style"]=_e["default"].locals||_e["default"]}var be=Object(d["a"])(ve,pe,he,!1,ge,null,null),ye=be.exports,Oe=function(e){Object(s["a"])(n,e);var t=Object(l["a"])(n);function n(){var e;return Object(o["a"])(this,n),e=t.apply(this,arguments),e.element=null,e}return Object(j["a"])(n,[{key:"close",value:function(){this.$router.push({path:"/"})}},{key:"mounted",value:function(){var e=this;console.log(this.$route),Z.a.get("https://sound-visualizer-staging.herokuapp.com//request/"+this.$route.params["result_id"]).then((function(t){e.element=t.data}))}}]),n}(r["a"]);Oe=Object(u["a"])([Object(c["a"])({components:{SingleElementDetail:ye}})],Oe);var je=Oe,we=je,ke=Object(d["a"])(we,ue,ce,!1,null,null,null),xe=ke.exports;r["a"].use(b["a"]);var Ce=[{path:"/",name:"Home",component:le},{name:"render",path:"/render/:result_id",component:xe},{path:"/about",name:"About",component:function(){return n.e("chunk-2d22d746").then(n.bind(null,"f820"))}}],$e=new b["a"]({mode:"history",base:"/www/dist/",routes:Ce}),Se=$e;r["a"].config.productionTip=!1,r["a"].use(g.a);new r["a"]({render:function(e){return e(v)},router:Se}).$mount("#app")},cf05:function(e,t,n){e.exports=n.p+"img/logo.82b9c7a5.png"},ebb4:function(e,t,n){e.exports={image_container:"ScrollingCanvas_image_container_eSwc5",spectrogram:"ScrollingCanvas_spectrogram_25_Et"}}});
//# sourceMappingURL=app.06c637f9.js.map