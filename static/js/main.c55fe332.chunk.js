(this["webpackJsonpbjj-predictor"]=this["webpackJsonpbjj-predictor"]||[]).push([[0],{11:function(e,t,a){e.exports=a(20)},19:function(e,t,a){},20:function(e,t,a){"use strict";a.r(t);var n=a(0),r=a.n(n),l=a(5),i=a.n(l),c=a(2),o=a(1),s=a.n(o),h=a(3),m=a(6),u=a(7),d=a(10),g=a(9),f=function(e){var t=e.value,a=e.onClick;return r.a.createElement("button",{className:"btn btn-primary btn-lg",type:"button",onClick:function(e){e.target.blur(),a()}},t)},E=function(e){var t=e.fighters,a=e.onChange,n=e.id;return r.a.createElement("select",{style:{width:"100%"},onChange:a,id:n},t.map((function(e){var t=e.id,a=e.first_name,n=e.nickname,l=e.last_name,i=e.team;return r.a.createElement("option",{key:t},a,n?' "'+n+'"':""," "+l,i?", "+i:"")})))};E.defaultProps={fighters:[]};var p=E,b=a(8),w=a.n(b),v="https://bjj-predictor.herokuapp.com",F=function(e){Object(d.a)(a,e);var t=Object(g.a)(a);function a(e){var n;return Object(m.a)(this,a),(n=t.call(this,e)).componentDidMount=function(){n.getFighters()},n.getFighters=Object(h.a)(s.a.mark((function e(){var t;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t="".concat(v,"/fighters"),e.next=3,fetch(t);case 3:e.sent.json().then((function(e){e.sort((function(e,t){return e.first_name.localeCompare(t.first_name)})),n.setState({fighters:e,fighter1:e[0],fighter2:e[0]})}));case 5:case"end":return e.stop()}}),e)}))),n.handleSelect=function(e){var t;n.setState((t={},Object(c.a)(t,e.target.id,n.state.fighters[e.target.selectedIndex]),Object(c.a)(t,"shouldShowPrediction",!1),t))},n.predict=Object(h.a)(s.a.mark((function e(){var t;return s.a.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return t="".concat(v,"/predict?id_1=").concat(n.state.fighter1.id,"&id_2=").concat(n.state.fighter2.id),e.next=3,fetch(t);case 3:e.sent.json().then((function(e){n.setState({prediction:e,shouldShowPrediction:!0})}));case 5:case"end":return e.stop()}}),e)}))),n.getFighterInfo=function(e){if(null===e)return r.a.createElement(r.a.Fragment,null);var t=e.first_name,a=e.nickname,n=e.last_name,l=e.team,i=e.wins,c=e.wins_by_sub,o=e.losses,s=e.losses_by_sub,h=i>0?(c/i*100).toFixed(1):0,m=o>0?(s/o*100).toFixed(1):0,u=(100*i/(i+o)).toFixed(1);return r.a.createElement("div",{className:"pt-3"},r.a.createElement("a",{rel:"noopener noreferrer",target:"_blank",href:"https://www.bjjheroes.com/bjj-fighters/?p="+e.id},r.a.createElement("h4",{className:"font-weight-bold"},t,a?' "'+a+'"':""," "+n)),r.a.createElement("h5",null,l||""),r.a.createElement("h5",null,i," wins, ",c," by submission (",h,"%)"),r.a.createElement("h5",null,o," losses, ",s," by submission (",m,"%)"),r.a.createElement("h5",null,u,"% win rate"))},n.getFighterNameStr=function(e){return e.first_name+(e.nickname?' "'+e.nickname+'"':"")+" "+e.last_name},n.getFighterLink=function(e){return r.a.createElement("a",{rel:"noopener noreferrer",target:"_blank",href:"https://www.bjjheroes.com/bjj-fighters/?p="+e.id},n.getFighterNameStr(e))},n.getPredictionInfo=function(){if(!n.state.shouldShowPrediction)return r.a.createElement(r.a.Fragment,null);var e,t=n.state.prediction.vs_history,a=parseFloat(n.state.prediction.win_by_sub),l=parseFloat(n.state.prediction.win_by_other),i=a+l,c=parseFloat(n.state.prediction.loss_by_sub),o=parseFloat(n.state.prediction.loss_by_other),s=c+o,h=parseFloat(n.state.prediction.draw);if(h>=i&&h>=s)e=r.a.createElement(r.a.Fragment,null,"DRAW (the following probabilities are for"," ",n.getFighterLink(n.state.fighter1),")");else if(i>s)e=n.getFighterLink(n.state.fighter1);else{e=n.getFighterLink(n.state.fighter2);var m=i;i=s,s=m,m=a,a=c,c=m,m=l,l=o,o=m}i=(100*i).toFixed(1),a=(100*a).toFixed(1),l=(100*l).toFixed(1),s=(100*s).toFixed(1),c=(100*c).toFixed(1),o=(100*o).toFixed(1),h=(100*h).toFixed(1);var u,d=0,g=0,f=0,E=r.a.createElement(r.a.Fragment,null);return t.length>0&&(t.sort((function(e,t){return e.year.localeCompare(t.year)})),E=t.map((function(e){var t;return"W"===e.win_loss?(t=n.getFighterLink(n.state.fighter1),d++):"L"===e.win_loss?(t=n.getFighterLink(n.state.fighter2),g++):(t="DRAW",f++),r.a.createElement("tr",{key:e.competition+e.year},r.a.createElement("td",null,t),r.a.createElement("td",null,e.method),r.a.createElement("td",null,e.competition),r.a.createElement("td",null,e.weight),r.a.createElement("td",null,e.stage),r.a.createElement("td",null,e.year))}))),u=0===t.length?"No VS history":d===g?"Fighters are tied "+d+"-"+g+"-"+f+" (W-L-D)":r.a.createElement("span",null,n.getFighterLink(d>g?n.state.fighter1:n.state.fighter2)," ","leads"," ",n.getFighterLink(d>g?n.state.fighter2:n.state.fighter1)," ",d>g?d:g,"-",d>g?g:d,"-",f," (W-L-D)"),r.a.createElement(r.a.Fragment,null,r.a.createElement("div",{className:"row justify-content-center pt-5"},r.a.createElement("div",{className:"col"},r.a.createElement("h4",{className:"font-weight-bold"},"Winner: ",e))),r.a.createElement("div",{className:"row justify-content-center pt-3"},r.a.createElement("div",{className:"col col-lg-6 col-12"},r.a.createElement("h5",null,"P(win): ",i,"%"),r.a.createElement("h5",null,"P(win by submission): ",a,"%"),r.a.createElement("h5",null,"P(win by other): ",l,"%")),r.a.createElement("div",{className:"col col-lg-6 col-12"},r.a.createElement("h5",null,"P(lose): ",s,"%"),r.a.createElement("h5",null,"P(lose by submission): ",c,"%"),r.a.createElement("h5",null,"P(lose by other): ",o,"%"))),r.a.createElement("div",{className:"row justify-content-center"},r.a.createElement("div",{className:"col"},r.a.createElement("h5",null,"P(draw): ",h,"%"))),r.a.createElement("div",{className:"row justify-content-center pt-5 pb-3"},r.a.createElement("div",{className:"col"},r.a.createElement("h5",null,u))),r.a.createElement("div",{className:"row justify-content-center"},r.a.createElement("div",{className:"col"},r.a.createElement("div",{className:"table-responsive"},r.a.createElement("table",{className:"table table-striped table-hover text-left"},r.a.createElement("thead",null,r.a.createElement("tr",null,r.a.createElement("th",null,"Winner"),r.a.createElement("th",null,"Method"),r.a.createElement("th",null,"Competition"),r.a.createElement("th",null,"Weight"),r.a.createElement("th",null,"Stage"),r.a.createElement("th",null,"Year"))),r.a.createElement("tbody",null,E))))))},n.state={fighters:[],fighter1:null,fighter2:null,prediction:null,shouldShowPrediction:!1},n}return Object(u.a)(a,[{key:"render",value:function(){return r.a.createElement("div",{className:"App container text-center py-5"},r.a.createElement("div",{className:"row"},r.a.createElement("div",{className:"col"},r.a.createElement("h1",{className:"font-weight-bold"},"BJJ Predictor"),r.a.createElement("h5",null,"Predicts the winner of Brazilian Jiu-Jitsu matches using deep neural networks.",r.a.createElement("br",null),"Choose two fighters and predict who would win in a BJJ match!"),r.a.createElement("div",{className:"row justify-content-center pt-5 pb-3"},r.a.createElement("div",{className:"col col-lg-4 col-12"},r.a.createElement(p,{fighters:this.state.fighters,onChange:this.handleSelect,id:"fighter1"}),this.getFighterInfo(this.state.fighter1)),r.a.createElement("div",{className:"col col-lg-1 col-12 align-self-center"},r.a.createElement("h1",{className:"font-weight-bold"},"VS")),r.a.createElement("div",{className:"col col-lg-4 col-12"},r.a.createElement(p,{fighters:this.state.fighters,onChange:this.handleSelect,id:"fighter2"}),this.getFighterInfo(this.state.fighter2))),r.a.createElement(f,{value:"Predict",onClick:this.predict}),this.getPredictionInfo())),r.a.createElement(w.a,{href:"https://github.com/ryantran2165/bjj-predictor",bannerColor:"#222",octoColor:"#7fffd4",target:"_blank"}))}}]),a}(n.Component);Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));a(18),a(19);i.a.render(r.a.createElement(r.a.StrictMode,null,r.a.createElement(F,null)),document.getElementById("root")),"serviceWorker"in navigator&&navigator.serviceWorker.ready.then((function(e){e.unregister()})).catch((function(e){console.error(e.message)}))}},[[11,1,2]]]);
//# sourceMappingURL=main.c55fe332.chunk.js.map