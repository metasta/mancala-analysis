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

function calc_sow(pos, i){
 let p = pos.slice();
 const o = i&4;
 const pi = p[i];
 p[i] = 0;
 for (let c = 1; c <= pi; c++){
  p[(i+c)&7] += 1;
 }
 if ((p[o]|p[o+1]|p[o+2]) == 0 || ((i+pi+1)&3) != 0){
  p[8] = 1 - p[8];
 }
 return p;
}

function update_msg(){
 for( let i = 0; i < 7; i++ ){
  if(i == 3){ continue; }
  if( is_valid_move(game.current_pos, i) ){
   const prophecy = db[enc(calc_sow(game.current_pos, i))];
   const result = ((prophecy&1) == (i>>2)) ? "WIN" : "LOSE";
   const count = (prophecy>>1) + 1;
   game.msg_area[i].innerText = result + " (" + count + ") ";
  } else {
   game.msg_area[i].innerText = "";
  }
 }
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

function set_pos(pos){
 game.current_pos = pos;
 game.his.push(pos.slice());
 update_fields();
}

function sow(i){
 if( is_valid_move(game.current_pos, i) ){
  set_pos(calc_sow(game.current_pos, i));
 } else {
  return false;
 }
}

function wayback(){
 if(game.his.length == 1){
  return false;
 }
 game.his.pop();
 game.current_pos = game.his.slice(-1)[0];
 update_fields();
}

function reset(){
 game.current_pos = [3,3,3,0,3,3,3,0,0];
 game.his = [ [3,3,3,0,3,3,3,0,0] ];
 update_fields();
}

function set_his(his){
 game.current_pos = his[his.length-1];
 game.his = his;
 update_fields();
}

window.onload = function(){
 update_fields();
}