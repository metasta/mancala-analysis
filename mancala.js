let game = {
 fields: document.getElementById("fields").children,
 msg_area: (function(){
  const f = document.getElementById("first").children;
  const s = document.getElementById("second").children;
  return [f[0], f[1], f[2], 0, s[0], s[1], s[2], 0];
 })(),
 button_back: document.getElementById("back"),
 button_reset: document.getElementById("reset"),
 current_pos: [3,3,3,0,3,3,3,0,0],
 his: [ [3,3,3,0,3,3,3,0,0] ]
}

function calc_sow(pos, i){
 let p = pos.slice();
 const o = p[8]<<2;
 const j = i + o;
 const pj = p[j];
 p[j] = 0;
 for (let c = 1; c <= pj; c++){
  p[(j+c)&7] += 1;
 }
 if ((p[o]|p[o+1]|p[o+2]) == 0 || ((j+pj+1)&3) != 0){
  p[8] = 1 - p[8];
 }
 return p;
}

function enc(pos){
 const p = pos.slice(0,3).concat(pos.slice(4,7)).concat([pos[8]]);
 return p.map(c => String.fromCharCode(c+48)).join("");
}

function is_gameover(pos){
 return ((pos[0]|pos[1]|pos[2]) == 0) || ((pos[4]|pos[5]|pos[6]) == 0);
}

function is_valid_move(pos, i){
 return (! is_gameover(pos) ) && ( (i>>2) == pos[8] ) && ( pos[i] );
}

function sow(side, i){
 if (! is_valid_move( game.current_pos, (side<<2)+i) ){
  return false;
 }
 const p = calc_sow(game.current_pos, i);
 game.his.push(p.slice());
 game.current_pos = p;
 update_fields();
}

function wayback(){
 if(game.his.length == 1){
  return false;
 }
 game.his.pop();
 game.current_pos = game.his.slice(-1)[0];
 update_fields();
 return false;
}

function update_fields(){
 for( let i = 0; i < 8; i++ ){
  game.fields[i].innerText = (game.current_pos[i] || "");
  if( is_valid_move(game.current_pos, i) ){
   game.fields[i].classList.remove("disabled");
  } else {
   game.fields[i].classList.add("disabled");
  }
 }
 update_msg();
 if (game.his.length == 1){
  game.button_back.classList.add("disabled");
  game.button_reset.classList.add("disabled");
 } else {
  game.button_back.classList.remove("disabled");
  game.button_reset.classList.remove("disabled");
 }
}

function update_msg(){
 for( let i = 0; i < 7; i++ ){
  if(i == 3){ continue; }
  if( is_valid_move(game.current_pos, i) ){
   const prophecy = db[enc(calc_sow(game.current_pos, (i&3)))];
   const result = ((prophecy&1) == (i>>2)) ? "WIN" : "LOSE";
   const count = (prophecy>>1) + 1;
   game.msg_area[i].innerText = result + " (" + count + ") ";
  } else {
   game.msg_area[i].innerText = "";
  }
 }
}

function reset(){
 game.current_pos = [3,3,3,0,3,3,3,0,0];
 game.his = [ [3,3,3,0,3,3,3,0,0] ];
 update_fields();
 return false;
}

window.onload = function(){
 update_fields();
}